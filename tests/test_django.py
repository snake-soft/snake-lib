from unittest import TestCase
from django_mock_queries.query import MockSet, MockModel
from snakelib.django.forms import field_queryset_exclude


class DjangoFormTestCase(TestCase):
    
    def test_field_queryset_exclude(self):
        class MockedField:
            queryset = MockSet(
                MockModel(pk=1, mock_name='one'),
                MockModel(pk=2, mock_name='two'),
                MockModel(pk=3, mock_name='three'),
                )

        field = MockedField()

        exclude_object = field.queryset[0]
        self.assertIn(exclude_object, field.queryset.all())
        field_queryset_exclude(field, exclude_object)
        self.assertNotIn(exclude_object, field.queryset.all())

        exclude_object = field.queryset[1]
        exclude_object_pk = field.queryset[1].pk
        self.assertIn(exclude_object, field.queryset.all())
        field_queryset_exclude(field, exclude_object)
        self.assertNotIn(exclude_object, field.queryset.all())
