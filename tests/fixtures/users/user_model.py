import factory
from factory import fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.models import UserProfile

faker = FakerFactory.create()

@register (_name='user_profile')
class UserProfileFactory(factory.Factory):

    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
    google_access_token = factory.fuzzy.FuzzyText(length=20)
    yandex_access_token = factory.fuzzy.FuzzyText(length=20)
