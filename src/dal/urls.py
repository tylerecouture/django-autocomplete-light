from django.urls import path


def urls(*form_or_model_classes):
    """
    Create a list of url patterns, to be called in url.py.

    Example::

        urlpatterns += autocomplete.urls(YourForm, YourOtherForm)

    Iterate over the fields to call the as_url() method for fields which define
    it.
    """
    from django import forms
    from django import urls
    result = []
    for cls in form_or_model_classes:
        if issubclass(cls, forms.BaseForm):
            for key, value in cls.declared_fields.items():
                if not hasattr(value, 'as_url'):
                    continue
                result.append(value.as_url(cls))
        else:  # let's hope it's a model :P
            for field in cls._meta.fields:
                if not hasattr(field, 'formfield_dal'):
                    continue
                result.append(urls.path(
                    field.formfield_dal['kwargs']['url'],
                    field.formfield_dal['kwargs']['view'].as_view(),
                    name=field.formfield_dal['kwargs']['url'],
                ))
    return result
