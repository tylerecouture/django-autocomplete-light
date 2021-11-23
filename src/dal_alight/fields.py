from django import forms
from django import urls
from django import http
from django.utils.safestring import mark_safe

from dal.views import BaseQuerySetView, ViewMixin
from dal.widgets import Select, SelectMultiple, QuerySetSelectMixin

from .widgets import AlightWidgetMixin


class ModelAlightWidget(AlightWidgetMixin, QuerySetSelectMixin, Select):
    def render(self, name, value, attrs=None, renderer=None):
        deck = ''
        if value:
            choice = self.field.queryset.filter(pk=value).first()
            deck = self.field.render_choice(choice)
        attrs = attrs or dict()
        attrs['slot'] = 'select'
        return mark_safe(f'''
            <autocomplete-select>
                {super().render(name, value, attrs)}
                <div slot="deck" class="deck">{deck}</div>
                <autocomplete-light slot="input" url="{self.url}">
                  <input slot="input" type="text" class="vTextField" />
                </autocomplete-light>
            </autocomplete-select>
        ''')


class ModelAlight(forms.ModelChoiceField):
    class AutocompleteView(BaseQuerySetView, ViewMixin):
        field = None

        def get(self, request, *args, **kwargs):
            return http.HttpResponse(
                b'\n'.join([
                    self.field.render_choice(choice).encode('utf8')
                    for choice in self.get_queryset()
                ]),
                content_type='text/html',
            )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', ModelAlightWidget())
        super().__init__(*args, **kwargs)

    def as_url(self, form):
        """Return url."""
        for name, field in form.base_fields.items():
            if field == self:
                break

        url_name = '.'.join([
            form.__module__,
            form.__name__,
            name,
        ])
        self.widget.url = url_name
        self.widget.field = self
        return urls.path(
            url_name,
            self.AutocompleteView.as_view(field=self, queryset=self.queryset),
            name=url_name
        )

    def render_choice(self, choice):
        return f'<div data-value="{choice.pk}">{choice}</div>'
