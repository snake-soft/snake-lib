from unittest import TestCase
from django_mock_queries.query import MockSet, MockModel
from snakelib.django.forms import field_queryset_exclude


class DjangoFormTestCase(TestCase):
    
    def test_field_queryset_exclude(self):
        class MockedField:
            queryset = MockSet(
                MockModel(mock_name='one'),
                MockModel(mock_name='two'),
                MockModel(mock_name='three'),
                )

        field = MockedField()
        exclude_object = field.queryset[0]
        
        self.assertIn(exclude_object, field.queryset.all())
        field_queryset_exclude(field, exclude_object)
        self.assertNotIn(exclude_object, field.queryset.all())
