from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.forms import FormDynamicModelBackend

from .classes import ImportSetupBackend
from .models import ImportSetup


class ImportSetupBackendSelectionForm(forms.Form):
    backend = forms.ChoiceField(
        choices=(), label=_(message='Backend'), help_text=_(
            message='The backend to use for the import setup.'
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['backend'].choices = ImportSetupBackend.get_choices()


class ImportSetupBackendDynamicForm(FormDynamicModelBackend):
    class Meta:
        fields = (
            'label', 'document_type', 'process_size', 'item_time_buffer'
        )
        model = ImportSetup


class ModelFilerUpload(forms.Form):
    uploaded_file = forms.FileField(
        help_text=_(message='CSV file that contain rows of model data'),
        label=_(message='File')
    )
