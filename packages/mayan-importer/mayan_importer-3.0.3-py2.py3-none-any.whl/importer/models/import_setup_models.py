from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.model_mixins import BackendModelMixin
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.events.decorators import method_event
from mayan.apps.events.event_managers import EventManagerSave

from ..events import event_import_setup_created, event_import_setup_edited
from ..literals import (
    DEFAULT_ITEM_TIME_BUFFER, DEFAULT_PROCESS_SIZE, SETUP_STATE_CHOICES,
    SETUP_STATE_NONE
)

from .import_setup_model_mixins import ImportSetupBusinessLogicMixin


class ImportSetup(
    BackendModelMixin, ImportSetupBusinessLogicMixin, models.Model
):
    _ordering_fields = ('label', 'process_size', 'state')

    label = models.CharField(
        help_text=_(message='Short description of this import setup.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=DocumentType, verbose_name=_(message='Document type')
    )
    process_size = models.PositiveIntegerField(
        default=DEFAULT_PROCESS_SIZE, help_text=_(
            'Number of items to process per execution.'
        ), verbose_name=_(message='Process size')
    )
    state = models.PositiveIntegerField(
        choices=SETUP_STATE_CHOICES, default=SETUP_STATE_NONE, help_text=_(
            'The last recorded state of the import setup.'
        ), verbose_name=_(message='State')
    )
    item_time_buffer = models.PositiveIntegerField(
        default=DEFAULT_ITEM_TIME_BUFFER, help_text=_(
            'Delay in milliseconds between item import tasks execution.'
        ), verbose_name=_(message='Item time buffer')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _(message='Import setup')
        verbose_name_plural = _(message='Import setups')

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse(viewname='importer:import_setup_list')

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_import_setup_created,
            'target': 'self'
        },
        edited={
            'event': event_import_setup_edited,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
