from django.db import models

class Stocks(models.Model):
    security_code = models.IntegerField()
    security_name = models.CharField(max_length=100)
    close = models.FloatField()
    market_cap = models.FloatField()
    
    def __str__(self):
        return self.security_name
    
class Queries(models.Model):
    security_code = models.IntegerField()
    security_name = models.CharField(max_length=100)
    close = models.FloatField()
    market_cap = models.FloatField()
    query = models.CharField(max_length=500)
    stock_id = models.IntegerField()
    
    def __str__(self):
        return self.query
# Create your models here.
