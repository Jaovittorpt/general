from django.db import models

class Campaign(models.Model):
    campaign_id = models.CharField(max_length=255, unique=True)
    campaign_name = models.CharField(max_length=255)
    objective = models.CharField(max_length=255)

    def __str__(self):
        return self.campaign_name

class AdSet(models.Model):
    adset_id = models.CharField(max_length=255, unique=True)
    adset_name = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='adsets')

    def __str__(self):
        return self.adset_name

class DailyInsight(models.Model):
    adset = models.ForeignKey(AdSet, on_delete=models.CASCADE, related_name='daily_insights')
    day = models.DateField()
    spend = models.FloatField()
    reach = models.IntegerField()
    impressions = models.IntegerField()
    frequency = models.FloatField()
    cpm = models.FloatField()
    total_messaging_connection = models.IntegerField()
    link_clicks = models.IntegerField()
    landing_page_views = models.IntegerField()
    leads = models.IntegerField()
    adds_to_cart = models.IntegerField()
    checkouts_initiated = models.IntegerField()
    purchases = models.IntegerField()
    purchases_conversion_value = models.FloatField()
    video_watches_25 = models.IntegerField()
    video_watches_50 = models.IntegerField()
    video_watches_75 = models.IntegerField()
    video_watches_95 = models.IntegerField()

    class Meta:
        unique_together = ('adset', 'day')

    def __str__(self):
        return f"{self.adset.adset_name} - {self.day}"
