from django.db import models
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

    def all(self, **kwargs):
        model_fields = get_model_fields(self.model)
        exclude = kwargs.get('exclude', self.exclude)
        only = kwargs.get('only', self.only)
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


class AutoMutation:
    def test(self):
        pass
