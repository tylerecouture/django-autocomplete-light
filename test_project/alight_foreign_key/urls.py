from dal import autocomplete

from django.conf.urls import url

from .forms import TForm


urlpatterns = autocomplete.urls(TForm)
