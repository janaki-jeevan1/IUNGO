from .models import *
import django_filters


class SubcategoryFilter(django_filters.filterset):
    class Meta:
        model=Sub_category
        fields=['name']


class ExperienceFilter(django_filters.NumberFilter):
    class Meta:
        model=Portfolio
        fields=['experience']


class RatingFilter(django_filters.filterset):
    class Meta:
        model=FeedBackRating
        fileds=['rating']


class BudgetFilter(django_filters.RangeFilter):
    pass
