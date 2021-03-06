from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from factory import DjangoModelFactory, SubFactory, LazyFunction
from factory import LazyAttribute
from factory import post_generation

from foodsaving.groups.factories import GroupFactory
from foodsaving.stores.models import Store as StoreModel, PickupDate as PickupDateModel, \
    PickupDateSeries as PickupDateSeriesModel
from foodsaving.utils.tests.fake import faker


class StoreFactory(DjangoModelFactory):

    class Meta:
        model = StoreModel

    group = SubFactory(GroupFactory)
    name = LazyAttribute(lambda x: faker.sentence(nb_words=4))
    description = LazyAttribute(lambda x: faker.name())


def in_one_day():
    return timezone.now() + timedelta(days=1)


class PickupDateFactory(DjangoModelFactory):

    class Meta:
        model = PickupDateModel

    @post_generation
    def collectors(self, created, collectors, **kwargs):
        if not created:
            return
        if collectors:
            for _ in collectors:
                self.collectors.add(_)

    store = SubFactory(StoreFactory)
    date = LazyFunction(in_one_day)
    max_collectors = 5


class PickupDateSeriesFactory(DjangoModelFactory):

    class Meta:
        model = PickupDateSeriesModel

    store = SubFactory(StoreFactory)
    start_date = LazyAttribute(lambda _: timezone.now().replace(second=0, microsecond=0) + relativedelta(minutes=15))
    rule = 'FREQ=WEEKLY'
