from django.db.models import Avg, F, OuterRef, Subquery
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import IndexPrice, Ticker
from .serializers import (
    TickerAverageSerializer,
    TickerSerializer,
    TickerYearlyResultSerializer,
)

ALLOWED_COLUMN_VALUES = [
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "adjusted_close_price",
]


class TickerViewset(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for index.
    """

    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    def get_queryset_by_performance(self, year, column):
        """
        Returns a ordered queryset based on the yearly
        perfomance of assets.
        """
        subquery = IndexPrice.objects.filter(
            ticker=OuterRef("pk"),
            date__year=year,
        )
        return (
            Ticker.objects.filter(indexprice__date__year=year)
            .annotate(
                first_value_on_year=Subquery(
                    subquery.values(column).order_by("date")[:1]
                ),
                last_value_on_year=Subquery(
                    subquery.values(column).order_by("-date")[:1]
                ),
            )
            .annotate(variation=F("last_value_on_year") - F("first_value_on_year"))
            .order_by("-variation")
            .distinct()
        )

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"best-performer/(?P<year>[0-9]{4})/(?P<column>[\w-]+)",
    )
    def best_performer(self, request, year, column):
        """
        Calculates the best performing index.
        """
        if column not in ALLOWED_COLUMN_VALUES:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            TickerYearlyResultSerializer(
                self.get_queryset_by_performance(year, column).first()
            ).data
        )

    @action(
        detail=False,
        methods=["GET"],
        url_path=r"worst-performer/(?P<year>[0-9]{4})/(?P<column>[\w-]+)",
    )
    def worst_performer(self, request, year, column):
        """
        Calculates the worst performing index.
        """
        if column not in ALLOWED_COLUMN_VALUES:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            TickerYearlyResultSerializer(
                self.get_queryset_by_performance(year, column).last()
            ).data
        )

    @action(
        detail=True,
        methods=["GET"],
        url_path=r"averages/(?P<year>[0-9]{4})",
    )
    def averages(self, request, year, pk=None):
        """
        Calculates the averages for a given ticker.

        Optionally takes in a `year` argument.
        """
        queryset = Ticker.objects.filter(pk=pk, indexprice__date__year=year).annotate(
            avg_open_price=Avg("indexprice__open_price"),
            avg_high_price=Avg("indexprice__high_price"),
            avg_low_price=Avg("indexprice__low_price"),
            avg_close_price=Avg("indexprice__close_price"),
            avg_adjusted_close_price=Avg("indexprice__adjusted_close_price"),
            avg_volume=Avg("indexprice__volume"),
        )

        return Response(TickerAverageSerializer(queryset.get()).data)
