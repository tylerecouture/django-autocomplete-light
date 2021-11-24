from django import forms
from django import urls
from django import http
from django.utils.safestring import mark_safe

from dal.widgets import Select, SelectMultiple, QuerySetSelectMixin

from threadlocals.threadlocals import get_current_request

from .views import AutocompleteView
from .widgets import AlightWidgetMixin


class ModelAlightWidget(AlightWidgetMixin, QuerySetSelectMixin, Select):
    def render(self, name, value, attrs=None, renderer=None):
        deck = ''
        if value:
            choice = self.field.queryset.filter(pk=value).first()
            deck = self.field.view().render_choice(choice)
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
    view = AutocompleteView

    def __init__(self, *args, view=None, url=None, **kwargs):
        kwargs.setdefault('widget', ModelAlightWidget)
        super().__init__(*args, **kwargs)
        self.widget.field = self
        self.view = view or AutocompleteView
        if url:
            self.widget.url = url

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        request = get_current_request()
        result.queryset = result.view(request=request).secure_queryset(self.queryset)
        return result

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
        return urls.path(
            url_name,
            self.view.as_view(queryset=self.queryset),
            name=url_name
        )
