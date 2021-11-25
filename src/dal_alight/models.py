from django.urls import path
from django.db import models

from . import urls
from . import fields

import djhacker


@djhacker.register(models.ForeignKey)
def foreign_key_autocomplete(model_field, cls=None, **kwargs):
    cls = cls or fields.ModelAlight

    if 'queryset' not in kwargs:
        qs = model_field.field.remote_field.model._default_manager.all()
        kwargs['queryset'] = qs

    if 'view' not in kwargs:
        kwargs['view'] = cls.view

    if 'url' not in kwargs:
        kwargs['url'] = '.'.join([
            'autocomplete',
            model_field.field.model.__module__,
            model_field.field.model.__name__,
            model_field.field.name,
        ])

    urls.urlpatterns.append(
        path(
            kwargs['url'],
            kwargs['view'].as_view(
                queryset=kwargs['queryset'],
            ),
            name=kwargs['url'],
        )
    )

    return cls, kwargs
