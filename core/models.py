from django.db import models
from django.contrib.auth.models import User

class ZakatCalculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    cash = models.DecimalField(max_digits=12, decimal_places=2)
    inventory = models.DecimalField(max_digits=12, decimal_places=2)
    receivables = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    liabilities = models.DecimalField(max_digits=12, decimal_places=2)
    zakat_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"{self.user.username} - {self.date.strftime('%Y-%m-%d')}"