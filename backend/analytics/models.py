from django.db import models

class DailyMetric(models.Model):
    date = models.DateField(unique=True)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    orders = models.PositiveIntegerField(default=0)
    customers = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return str(self.date)
