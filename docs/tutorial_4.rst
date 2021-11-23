django-autocomplete-light experimental tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Welcome to secret django-autocomplete-light experiment!

.. image:: experienced.png
  :height: 300
  :align: center

- No? go ahead with the :ref:`select2 tutorial<select2-tutorial>`, it's a safe
  choice because it's maintained by a huge community and has all the features
- **Yes!!** read on to build the future together, we don't have much features
  yet over here, because we need time to curate them and stabilize an API, but
  we fix a lot of issues that won't be resolvable with select2.

Differences with select2
========================

This relies on the `autocomplete-light`_ Web Component that is heavily inspired
from the autocomplete script of the early versions of
django-autocomplete-light, which was designed from the ground up for Django
itself:

- delegates suggestion box rendering to the server, allowing templates for
  example
- rich rendering of options both in the widget and the autocomplete box
- no javascript dependency: no conflict with anything!
- extends HTMLElement: no need to bother with the element lifecycle because
  it's handled by the browser!
- material design by default, looks great everywhere
- also works to create non-form fields such as global navigation bars like in
  facebook header

The :ref:`test_project<demo-install>` already includes some examples, to try
out `autocomplete-light`_ itself you just have to clone its repo and run
``python serve.py``.

Foreign Key
===========

- Example source code: `test_project/alight_foreign_key
  <https://github.com/yourlabs/django-autocomplete-light/tree/master/test_project/alight_foreign_key>`_
- Live demo: `/admin/alight_foreign_key
  <http://localhost:8000/admin/alight_foreign_key/tmodel/add/>`_

Create a ModelForm with a ModelAlight field:

.. code-block:: py

    from dal import autocomplete
    from django import forms


    class YourForm(forms.ModelForm):
        test = autocomplete.ModelAlight(queryset=YourModel.objects.all())

        class Meta:
            model = YourModel
            fields = ('name', 'test')

Then, add the URLs to the autocomplete view:

.. code-block:: py

    from dal import autocomplete
    from django import urls

    from .forms import YourForm

    urlpatterns = autocomplete.urls(YourForm)

That's it!

Customize option rendering
==========================

To customize option rendering, at this point, you can override the
``render_choice`` method of the form field:

.. code-block:: py

    class YourModelField(autocomplete.ModelAlight):
        def render_choice(self, choice):
            return f'<div data-value="{choice.pk}">{choice}</div>'


    class YourForm(forms.ModelForm):
        test = YourModelField(queryset=YourModel.objects.all())

        class Meta:
            model = YourModel
            fields = ('name', 'test')

Choices will be rendered as specified in this function, both in autocomplete
box suggestions and on initial form rendering.

.. _autocomplete-light: https://yourlabs.io/oss/autocomplete-light
