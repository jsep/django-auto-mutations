from unittest import TestCase
from unittest.mock import patch

import graphene

from django_auto_mutations.auto_mutation import BaseMutation
from django_auto_mutations.tests.test_model_fields import SimpleModel, Category, \
    Product
from django_auto_mutations.tests.utils import simple_model_fields_name, \
    dict_keys


class BaseMutationTest(TestCase):
    def test_model_and_node_are_required(self):
        self.assertRaises(AssertionError, lambda: BaseMutation())
        self.assertRaises(AssertionError, lambda: BaseMutation(model={}))
        self.assertRaises(AssertionError, lambda: BaseMutation(node={}))
        BaseMutation(node={}, model={})  # Should not fail

    @patch("django_auto_mutations.auto_mutation.BaseMutation.action")
    def test__mutation_class_name(self, action):
        action.return_value = 'action'
        class_name = BaseMutation.class_name(model=SimpleModel)
        self.assertEqual(class_name, 'ActionSimpleModel')

    def test_mutation_mutation_property_name(self):
        property_name = BaseMutation.property_name(model=SimpleModel)
        self.assertEqual(property_name, 'simple_model')

    def test_argument_class_return_class(self):
        arguments = BaseMutation.arguments_class(model=SimpleModel)
        self.assertEqual(arguments.__name__, 'Arguments')

    # def test_argument_class_has_same_properties_as_model(self):
    #     arguments = BaseMutation.arguments_class(model=SimpleModel)
    #     attr = class_attr_name(arguments)
    #     self.assertEqual(sorted(attr), sorted(simple_model_fields_name))

    def test_construct_fields(self):
        fields = BaseMutation.construct_fields(model=SimpleModel)
        self.assertListEqual(dict_keys(fields),
                             sorted(simple_model_fields_name))
        self.assertIsInstance(fields['id'], graphene.types.scalars.ID)
        self.assertIsInstance(fields['name'], graphene.types.scalars.String)
        self.assertIsInstance(fields['description'],
                              graphene.types.scalars.String)

    def test_construct_fields_exclude_fields(self):
        fields = BaseMutation.construct_fields(
            model=SimpleModel,
            exclude_fields=['name']
        )
        self.assertListEqual(dict_keys(fields), sorted(['id', 'description']))

    def test_construct_fields_only_fields(self):
        fields = BaseMutation.construct_fields(
            model=SimpleModel,
            only_fields=['description']
        )
        self.assertListEqual(dict_keys(fields), ['description'])

    def test_construct_fields_related_fields(self):
        fields = BaseMutation.construct_fields(model=Product)
        self.assertListEqual(
            dict_keys(fields),
            sorted(['category_id', 'id', 'many', 'one2many'])
        )

    def test_related_fields(self):
        fields = BaseMutation.related_fields(model=Product)
        self.assertListEqual(
            dict_keys(fields),
            sorted(['category_id', 'many', 'one2many'])
        )

        self.assertIsInstance(fields['category_id'], graphene.types.scalars.ID)
        self.assertIsInstance(fields['many'], graphene.types.List)
        self.assertIsInstance(fields['one2many'], graphene.types.List)

