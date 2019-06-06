import factory
import factory.fuzzy


class ItemFactory(factory.django.DjangoModelFactory):

    title = factory.Sequence(lambda n: 'Тестовый товар №{}'.format(n))
    description = factory.Sequence(
        lambda n: 'Описание тестового товара №{}'.format(n)
    )
    price = factory.fuzzy.FuzzyInteger(1, 100000)

    class Meta:
        model = 'somemart.Item'


class ReviewFactory(factory.django.DjangoModelFactory):

    grade = factory.fuzzy.FuzzyInteger(1, 10)
    text = factory.Sequence(lambda n: 'Тестовый отзыв №{}'.format(n))
    item = factory.SubFactory(ItemFactory)

    class Meta:
        model = 'somemart.Review'
