import re
from abc import ABCMeta, abstractmethod

import graphene
from django.db import models
from django.db.models.base import ModelBase
from graphene_django.registry import get_global_registry
from graphene_django.types import construct_fields
from graphene_django.utils import get_model_fields

M2M_MODEL_FIELDS = (models.ManyToManyField,
                    models.ManyToManyRel,
                    models.ManyToOneRel,)
ONE2M_MODEL_FIELDS = (models.ForeignKey,)
RELATED_MODEL_FIELDS = ONE2M_MODEL_FIELDS + M2M_MODEL_FIELDS


class ModelFields:
    def __init__(self, *args, **kwargs):
        self.model = kwargs.get('model')
        self.exclude = kwargs.get('exclude', [])
        self.only = kwargs.get('only', [])
        assert self.model is not None, "model not defined"
        if self.exclude is None:
            self.exclude = []
        if self.only is None:
            self.only = []

    def all(self, **kwargs):
        model_fields = get_model_fields(self.model)
        exclude = kwargs.get('exclude', self.exclude)
        only = kwargs.get('only', self.only)
        if exclude is None:
            exclude = self.exclude
        if only is None:
            only = self.only
        all_fields = []
        for key, field in model_fields:
            is_excluded = key in exclude
            is_not_in_only = len(only) > 0 and key not in only
            if is_excluded or is_not_in_only:
                continue
            all_fields.append((key, field))
        return all_fields

    def all_names(self, **kwargs):
        return self._just_names(self.all(**kwargs))

    def related(self, **kwargs):
        return [
            (name, field)
            for name, field in self.all(**kwargs)
            if isinstance(field, RELATED_MODEL_FIELDS)
        ]

    def related_names(self, **kwargs):
        return self._just_names(self.related(**kwargs))

    def m2m(self, **kwargs):
        return [
            (name, field)
            for name, field in self.all(**kwargs)
            if isinstance(field, M2M_MODEL_FIELDS)
        ]

    def m2m_names(self, **kwargs):
        return self._just_names(self.m2m(**kwargs))

    def one2m(self, **kwargs):
        return [
            (name, field)
            for name, field in self.all(**kwargs)
            if isinstance(field, ONE2M_MODEL_FIELDS)
        ]

    def one2m_names(self, **kwargs):
        return self._just_names(self.one2m(**kwargs))

    def _just_names(self, fields):
        return list(map(lambda f: f[0], fields))


class BaseMutation:
    __metaclass__ = ABCMeta

    def __new__(cls, *args, **kwargs):
        model = kwargs.pop('model', None)
        node = kwargs.pop('node', None)
        assert model is not None, "'model' is required"
        assert node is not None, "'node' is not define"

    @classmethod
    @abstractmethod
    def action(cls) -> str:
        pass

    @classmethod
    def class_name(cls, model: ModelBase) -> str:
        return cls.action().capitalize() + model._meta.object_name

    @classmethod
    def property_name(cls, model: ModelBase):
        return to_snake_case(model._meta.object_name)

    @classmethod
    def arguments_class(cls, model):
        return type('Arguments', (object,), {})

    @classmethod
    def construct_fields(cls, model, **kwargs):
        exclude_fields = kwargs.get('exclude_fields', [])
        only_fields = kwargs.get('only_fields', [])
        model_fields = ModelFields(
            model=model,
            exclude=exclude_fields,
            only=only_fields
        )
        exclude_fields = exclude_fields + model_fields.related_names()
        fields = construct_fields(**{"model": model, "only_fields": only_fields,
                                     "exclude_fields": exclude_fields,
                                     "registry": get_global_registry()})
        related_fields = cls.related_fields(model=model, **kwargs)
        fields = {**fields, **related_fields}

        return fields

    @classmethod
    def related_fields(cls, model, **kwargs):
        model_fields = ModelFields(
            model=model,
            exclude=kwargs.get('exclude_fields'),
            only=kwargs.get('only_fields')
        )
        fields = {}
        for key, value in model_fields.one2m():
            fields[key + '_id'] = graphene.ID(required=not value.blank)
        for key, value in model_fields.m2m():
            fields[key] = graphene.List(graphene.ID, required=False)

        return fields


class AutoMutation:
    def test(self):
        pass


# From this response in Stackoverflow
# http://stackoverflow.com/a/1176023/1072990
def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
