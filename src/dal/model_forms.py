import types

from django.db import models
from django.forms import models as forms_models

from dal_alight.fields import ModelAlight

from . import urls


class Registry:
    registry = dict()

    def register(self, model_field, cls=None, **kwargs):
        if not cls:
            if isinstance(model_field.field, models.ForeignKey):
                cls = ModelAlight
            else:
                raise Exception('Field class required')

        model = model_field.field.model
        if model not in self.registry:
            self.registry[model] = dict()

        self.registry[model][model_field.field.name] = (cls, kwargs)

    def formfield(**kwargs):
        breakpoint()


registry = Registry()
register = registry.register


class ModelFormMetaclass(forms_models.ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        return super().__new__(mcs, name, bases, attrs)


class BaseModelForm(forms_models.BaseModelForm):
    pass
    #class Meta:
    #    formfield_callback = registry.formfield


class ModelForm(BaseModelForm, metaclass=ModelFormMetaclass):
    pass


def modelform_factory(*args, **kwargs):
    kwargs.setdefault('form', ModelForm)
    return forms_models.modelform_factory(*args, **kwargs)


def formfield(model_field, cls=None, **kwargs):
    if not cls:
        if isinstance(model_field.field, models.ForeignKey):
            cls = ModelAlight
        else:
            raise Exception('Field class required')

    def _formfield(self, *, using=None, **kw):
        if using:
            raise Exception('using not supported at this stage')

        formfield = self.formfield_dal['django'](**{
            'form_class': self.formfield_dal['cls'],
            'queryset': self.remote_field.model._default_manager.using(using),
            **self.formfield_dal['kwargs'],
            **kw,
        })
        return formfield

    if 'url' not in kwargs:
        kwargs['url'] = '.'.join([
            'autocomplete',
            model_field.field.model.__module__,
            model_field.field.model.__name__,
            model_field.field.name,
        ])

    if 'view' not in kwargs:
        kwargs['view'] = cls.view

    model_field.field.formfield_dal = dict(
        django=model_field.field.formfield,
        cls=cls,
        kwargs=kwargs,
    )

    urls.urlpatterns.append(
        urls.path(
            kwargs['url'],
            kwargs['view'].as_view(
                queryset=model_field.field.remote_field.model._default_manager.using(None),
            ),
            name=kwargs['url'],
        )
    )

    model_field.field.formfield = types.MethodType(_formfield, model_field.field)
