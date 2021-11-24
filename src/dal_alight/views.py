from dal.views import BaseQuerySetView, ViewMixin


class AutocompleteView(BaseQuerySetView, ViewMixin):
    render_choice = lambda choice: f'<div data-value="{choice.pk}">{choice}</div>'

    def render_box(self):
        return '\n'.join([
            self.render_choice(choice)
            for choice in self.get_queryset()
        ])

    def get(self, request, *args, **kwargs):
        return http.HttpResponse(
            self.render_box().encode('utf8'),
            content_type='text/html',
        )
