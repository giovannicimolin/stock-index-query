from django.db import models


class Ticker(models.Model):
    """
    Model representing ticker.
    """

    id = models.CharField(primary_key=True, editable=False, max_length=10)

    def __str__(self):
        return self.id


class IndexPrice(models.Model):
    """
    Model that stores daily information for each index.
    """

    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    adjusted_close_price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return f"[{self.date}] Ticker: {self.ticker}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ticker", "date"], name="unique_date")
        ]
