import requests
import pandas as pd
from datetime import datetime, timedelta
from .models import Campaign, AdSet, DailyInsight

class GraphAPI:
    def __init__(self, access_token, ad_account_id):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.base_url = "https://graph.facebook.com/v20.0/"
    
    def get_insights(self, date_start=None, date_stop=None):
        # Convert date_start and date_stop to datetime objects
        date_start = datetime.strptime(date_start, '%Y-%m-%d')
        date_stop = datetime.strptime(date_stop, '%Y-%m-%d')
        
        all_data = []

        while date_start < date_stop:
            # Define the next end date for the request
            date_end = date_start + timedelta(days=60)
            if date_end > date_stop:
                date_end = date_stop
            
            url = f"{self.base_url}act_{self.ad_account_id}/insights"
            params = {
                'time_increment': 1,
                'level': 'adset',
                'fields': 'campaign_id,campaign_name,objective,adset_id,adset_name,spend,reach,impressions,frequency,cpm,actions,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p95_watched_actions,date_start,date_stop',
                'limit': 10000,
                'access_token': self.access_token,
                'date_start': date_start.strftime('%Y-%m-%d'),
                'date_stop': date_end.strftime('%Y-%m-%d')
            }

            response = requests.get(url, params=params)
            data = response.json()
            
            campaign_data = self.process_data(data)
            all_data.extend(campaign_data)

            # Move to the next date range
            date_start = date_end + timedelta(days=1)
        
        df = pd.DataFrame(all_data)
        self.save_to_db(df)
        return df

    def process_data(self, data):
        campaign_data = []

        action_types = [
            "onsite_conversion.total_messaging_connection",
            "onsite_conversion.messaging_first_reply",
            "link_click",
            "landing_page_view",
            "purchase",
            "add_to_cart",
            "initiate_checkout"
        ]

        for campaign in data.get('data', []):
            campaign_id = campaign.get('campaign_id')
            campaign_name = campaign.get('campaign_name')
            objective = campaign.get('objective')
            adset_id = campaign.get('adset_id')
            adset_name = campaign.get('adset_name')
            spend = float(campaign.get('spend', 0))
            reach = int(campaign.get('reach', 0))
            impressions = int(campaign.get('impressions', 0))
            frequency = float(campaign.get('frequency', 0))
            cpm = campaign.get('cpm', 0)
            try:
                cpm = float(cpm)
            except ValueError:
                cpm = 0
            day = campaign.get('date_stop')
            actions = campaign.get('actions', [])
            video_p25_watched = sum(int(action['value']) for action in campaign.get('video_p25_watched_actions', []))
            video_p50_watched = sum(int(action['value']) for action in campaign.get('video_p50_watched_actions', []))
            video_p75_watched = sum(int(action['value']) for action in campaign.get('video_p75_watched_actions', []))
            video_p95_watched = sum(int(action['value']) for action in campaign.get('video_p95_watched_actions', []))

            action_values = {action_type: 0 for action_type in action_types}
            for action in actions:
                if action['action_type'] in action_types:
                    action_values[action['action_type']] = int(action['value'])
            
            campaign_info = {
                'Campaign ID': campaign_id,
                'Campaign Name': campaign_name,
                'Objective': objective,
                'Ad Set ID': adset_id,
                'Ad Set Name': adset_name,
                'Spend': spend,
                'Reach': reach,
                'Impressions': impressions,
                'Frequency': frequency,
                'CPM (Cost per 1,000 Impressions)': cpm,
                'onsite_conversion.total_messaging_connection': action_values["onsite_conversion.total_messaging_connection"],
                'Link Clicks': action_values["link_click"],
                'Landing Page Views': action_values["landing_page_view"],
                'Leads': action_values["onsite_conversion.messaging_first_reply"],
                'Adds to Cart': action_values["add_to_cart"],
                'Checkouts Initiated': action_values["initiate_checkout"],
                'Purchases': action_values["purchase"],
                'Purchases Conversion Value': action_values["purchase"],
                'Video Watches at 25%': video_p25_watched,
                'Video Watches at 50%': video_p50_watched,
                'Video Watches at 75%': video_p75_watched,
                'Video Watches at 95%': video_p95_watched,
                'Day': day
            }
            
            campaign_data.append(campaign_info)
        
        return campaign_data

    def save_to_db(self, df):
        for _, row in df.iterrows():
            campaign, created = Campaign.objects.get_or_create(
                campaign_id=row['Campaign ID'],
                defaults={
                    'campaign_name': row['Campaign Name'],
                    'objective': row['Objective']
                }
            )
            
            adset, created = AdSet.objects.get_or_create(
                adset_id=row['Ad Set ID'],
                defaults={
                    'adset_name': row['Ad Set Name'],
                    'campaign': campaign
                }
            )

            DailyInsight.objects.update_or_create(
                adset=adset,
                day=row['Day'],
                defaults={
                    'spend': row['Spend'],
                    'reach': row['Reach'],
                    'impressions': row['Impressions'],
                    'frequency': row['Frequency'],
                    'cpm': row['CPM (Cost per 1,000 Impressions)'],
                    'total_messaging_connection': row['onsite_conversion.total_messaging_connection'],
                    'link_clicks': row['Link Clicks'],
                    'landing_page_views': row['Landing Page Views'],
                    'leads': row['Leads'],
                    'adds_to_cart': row['Adds to Cart'],
                    'checkouts_initiated': row['Checkouts Initiated'],
                    'purchases': row['Purchases'],
                    'purchases_conversion_value': row['Purchases Conversion Value'],
                    'video_watches_25': row['Video Watches at 25%'],
                    'video_watches_50': row['Video Watches at 50%'],
                    'video_watches_75': row['Video Watches at 75%'],
                    'video_watches_95': row['Video Watches at 95%']
                }
            )
