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
        return [key for key, value in self.all(**kwargs)]

    def related(self):
        return [
            (name, field)
            for name, field in self.all()
            if isinstance(field, RELATED_MODEL_FIELDS)
        ]

    def m2m(self):
        return [
            (name, field)
            for name, field in self.all()
            if isinstance(field, M2M_MODEL_FIELDS)
        ]


class AutoMutation:
    def test(self):
        pass
