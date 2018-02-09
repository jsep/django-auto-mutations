from django.db import models
from django.test import TestCase

from django_auto_mutations.auto_mutation import ModelFields
from django_auto_mutations.tests.utils import create_model


class TestModelFields(TestCase):
    def setUp(self):
        self.all_fields = sorted(list(simple_model_fields.copy().items()))
        self.all_field_names = sorted(simple_model_fields_name.copy())

    def test_model_field_is_required(self):
        self.assertRaises(AssertionError, lambda: ModelFields())

    def test_set_all_properties(self):
        only = ['name']
        exclude = ['id']
        model_fields = ModelFields(
            model=SimpleModel,
            only=only,
            exclude=exclude
        )
        self.assertEqual(model_fields.model, SimpleModel)
        self.assertEqual(model_fields.exclude, exclude)
        self.assertEqual(model_fields.only, only)

    def test_get_all_fields(self):
        model_fields = ModelFields(model=SimpleModel)
        all_fields = model_fields.all()
        self.assertEqual(len(all_fields), len(self.all_fields))
        self.assertListEqual(sorted(all_fields), self.all_fields)

    def test_get_all_fields_names(self):
        model_fields = ModelFields(model=SimpleModel)
        all_fields = model_fields.all_names()
        self.assertEqual(len(all_fields), len(self.all_field_names))
        self.assertListEqual(sorted(all_fields), self.all_field_names)

    def test_get_all_but_excluded_fields(self):
        exclude = ['name']
        model_fields = ModelFields(model=SimpleModel, exclude=exclude)
        all_fields = model_fields.all()
        self.assertAllButField(all_fields, exclude)

    def test_get_all_but_excluded_fields_from_argument(self):
        exclude = ['name']
        model_fields = ModelFields(model=SimpleModel)
        all_fields = model_fields.all(exclude=exclude)
        self.assertAllButField(all_fields, exclude)

    def test_get_all_but_excluded_fields_names(self):
        exclude = ['name']
        model_fields = ModelFields(model=SimpleModel, exclude=exclude)
        all_fields = model_fields.all_names()
        self.assertAllButFieldName(all_fields, exclude)

    def test_get_all_but_excluded_fields_names_from_argument(self):
        exclude = ['name']
        model_fields = ModelFields(model=SimpleModel)
        all_fields = model_fields.all_names(exclude=exclude)
        self.assertAllButFieldName(all_fields, exclude)

    def test_get_all_only_fields(self):
        only = ['name']
        model_fields = ModelFields(model=SimpleModel, only=only)
        all_fields = model_fields.all()
        self.assertOnlyField(all_fields, only)

    def test_get_all_only_fields_names(self):
        only = ['name']
        model_fields = ModelFields(model=SimpleModel, only=only)
        all_fields = model_fields.all_names()
        self.assertOnlyFieldName(all_fields, only)

    def test_get_all_only_fields_from_argument(self):
        only = ['name']
        model_fields = ModelFields(model=SimpleModel, only=only)
        all_fields = model_fields.all()
        self.assertOnlyField(all_fields, only)

    def test_get_all_only_fields_names_from_argument(self):
        only = ['name']
        model_fields = ModelFields(model=SimpleModel)
        all_fields = model_fields.all_names(only=only)
        self.assertOnlyFieldName(all_fields, only)

    def assertAllButField(self, fields, field_names):
        expected_field_names = [
            (key, field) for key, field in
            self.all_fields if key not in field_names
        ]
        self.assertEqual(sorted(fields), sorted(expected_field_names))

    def assertAllButFieldName(self, fields, field_names):
        expected_fields = [
            field for field in self.all_field_names
            if field not in field_names
        ]
        self.assertEqual(sorted(fields), sorted(expected_fields))

    def assertOnlyField(self, fields, field_names):
        expected_field_names = [
            (key, field) for key, field in
            self.all_fields if key in field_names
        ]
        self.assertEqual(sorted(fields), sorted(expected_field_names))

    def assertOnlyFieldName(self, fields, field_names):
        expected_fields = [
            field for field in self.all_field_names
            if field in field_names
        ]
        self.assertEqual(sorted(fields), sorted(expected_fields))


simple_model_fields = {
    'name': models.CharField(max_length=20),
    'description': models.CharField(max_length=20)
}
simple_model_fields_name = [
    k for k, v in simple_model_fields.items()
]
simple_model_fields_name.append('id')
simple_model_fields_name = sorted(simple_model_fields_name)
SimpleModel = create_model(
    name='SimpleModel',
    app_label='model_fields',
    fields=simple_model_fields
)
simple_model_fields['id'] = SimpleModel._meta.fields[0]  # id field
