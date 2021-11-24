from dal import autocomplete
from alight_modelform.models import TModel


def test_field():
    TForm = autocomplete.modelform_factory(TModel, fields='__all__')
    assert isinstance(TForm.base_fields['test'], autocomplete.ModelAlight)
    assert autocomplete.urls(TModel) == []
