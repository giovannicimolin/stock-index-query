from rest_framework import serializers

from .models import IndexPrice, Ticker


class IndexPriceSerializer(serializers.ModelSerializer):
    """
    Serializer TBD
    """

    class Meta:
        model = IndexPrice
        fields = [
            "date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "adjusted_close_price",
            "volume",
        ]


class TickerSerializer(serializers.ModelSerializer):
    """
    Serializer for ticker and nested values
    """

    id = serializers.CharField()
    indexprice_set = IndexPriceSerializer(many=True)

    class Meta:
        model = IndexPrice
        fields = [
            "id",
            "indexprice_set",
        ]


class TickerAverageSerializer(serializers.ModelSerializer):
    """
    Serializer for ticker and nested values
    """

    id = serializers.CharField()
    avg_open_price = serializers.FloatField()
    avg_high_price = serializers.FloatField()
    avg_low_price = serializers.FloatField()
    avg_close_price = serializers.FloatField()
    avg_adjusted_close_price = serializers.FloatField()
    avg_volume = serializers.IntegerField()

    class Meta:
        model = Ticker
        fields = [
            "id",
            "avg_open_price",
            "avg_high_price",
            "avg_low_price",
            "avg_close_price",
            "avg_adjusted_close_price",
            "avg_volume",
        ]


class TickerYearlyResultSerializer(serializers.ModelSerializer):
    """
    Serializer for ticker and nested values
    """

    id = serializers.CharField()
    first_value_on_year = serializers.FloatField()
    last_value_on_year = serializers.FloatField()
    variation = serializers.FloatField()

    class Meta:
        model = Ticker
        fields = [
            "id",
            "first_value_on_year",
            "last_value_on_year",
            "variation",
        ]
