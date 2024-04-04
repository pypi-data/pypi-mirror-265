import json

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.tasks.document_tasks import task_document_upload
from mayan.apps.events.decorators import method_event
from mayan.apps.events.event_managers import EventManagerMethodAfter

from ..events import event_import_setup_item_finished
from ..literals import (
    SETUP_ITEM_STATE_COMPLETE, SETUP_ITEM_STATE_ERROR, SETUP_ITEM_STATE_NONE,
    SETUP_ITEM_STATE_PROCESSING
)


class ImportSetupItemBusinessLogicMixin:
    @classmethod
    def get_process_allowed_state_list(self):
        return (
            SETUP_ITEM_STATE_COMPLETE, SETUP_ITEM_STATE_ERROR,
            SETUP_ITEM_STATE_NONE
        )

    def check_valid(self):
        backend_instance = self.import_setup.get_backend_instance()
        return backend_instance.check_valid(
            identifier=self.identifier, data=self.data
        )

    @property
    def data(self):
        return self.load_data()

    def load_data(self):
        return json.loads(s=self.serialized_data or '{}')

    def get_data_display(self):
        return ', '.join(
            [
                '"{}": "{}"'.format(key, value) for key, value in self.data.items()
            ]
        )
    get_data_display.short_description = _(message='Data')

    def dump_data(self, obj):
        self.serialized_data = json.dumps(obj=obj)

    def get_process_allowed(self):
        return self.state in self.get_process_allowed_state_list()

    def get_state_label(self):
        return self.get_state_display()
    get_state_label.help_text = _(
        message='The last recorded state of the item. The field will be '
        'sorted by the numeric value of the state and not the actual text.'
    )
    get_state_label.short_description = _(message='State')

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_item_finished,
        action_object='import_setup',
        target='self'
    )
    def process(self, force=False):
        shared_uploaded_file = None

        if force or self.get_process_allowed():
            self.state = SETUP_ITEM_STATE_PROCESSING
            self.save()

            backend_instance = self.import_setup.get_backend_instance()

            try:
                shared_uploaded_file = backend_instance.item_process(
                    identifier=self.identifier, data=self.data
                )
            except Exception as exception:
                self.state = SETUP_ITEM_STATE_ERROR
                self.save()

                self.error_log.create(
                    text=str(exception)
                )

                if settings.DEBUG:
                    raise
            else:
                source_metadata_dictionary = self.data.copy()
                source_metadata_dictionary.update(
                    {
                        'mayan_import_setup_id': self.import_setup.pk,
                        'mayan_import_setup_item_id': self.pk
                    }
                )

                callback_dict = {
                    'post_document_file_create': {
                        'dotted_path': 'importer.classes.ImportSetupBackend',
                        'function_name': 'callback_document_file',
                        'kwargs': {
                            'mayan_import_setup_item_id': self.pk,
                            'source_metadata': source_metadata_dictionary
                        }
                    }
                }

                backend_class = self.import_setup.get_backend_class()

                label = self.data.get(backend_class.item_label, self.id)

                task_document_upload.apply_async(
                    kwargs={
                        'document_type_id': self.import_setup.document_type.pk,
                        'shared_uploaded_file_id': shared_uploaded_file.pk,
                        'callback_dict': callback_dict,
                        'label': label
                    }
                )

                self.state = SETUP_ITEM_STATE_COMPLETE
                self.save()

                queryset = self.error_log.all()
                queryset.delete()
