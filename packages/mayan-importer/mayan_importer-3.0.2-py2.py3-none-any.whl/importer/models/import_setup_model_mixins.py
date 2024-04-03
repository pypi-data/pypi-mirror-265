from datetime import datetime, timedelta

from django.apps import apps
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import gettext_lazy as _

from ..events import (
    event_import_setup_populate_finished, event_import_setup_populate_started,
    event_import_setup_process_finished, event_import_setup_process_started
)
from ..literals import (
    ENABLE_STATE_CHANGE, SETUP_ITEM_STATE_COMPLETE, SETUP_STATE_ERROR,
    SETUP_STATE_EXECUTING, SETUP_STATE_NONE, SETUP_STATE_POPULATING
)
from ..tasks import task_import_setup_item_process_apply_async


class ImportSetupBusinessLogicMixin:
    def clear(self):
        self.items.all().delete()

    def get_state_label(self):
        return self.get_state_display()
    get_state_label.short_description = _(message='State')
    get_state_label.help_text = _(
        message='The last recorded state of the setup item. The field will '
        'be sorted by the numeric value of the state and not the actual '
        'text.'
    )

    def item_count_all(self):
        return self.items.count()

    item_count_all.short_description = _(message='Items')

    def item_count_complete(self):
        return self.items.filter(state=SETUP_ITEM_STATE_COMPLETE).count()

    item_count_complete.short_description = _(message='Items complete')

    def item_count_percent(self):
        items_complete = self.item_count_complete()
        items_all = self.item_count_all()

        if items_all == 0:
            percent = 0
        else:
            percent = items_complete / items_all * 100.0

        return '{} of {} ({:.0f}%)'.format(
            intcomma(value=items_complete), intcomma(value=items_all),
            percent
        )

    item_count_percent.short_description = _(message='Progress')

    def populate(self, user=None):
        event_import_setup_populate_started.commit(
            actor=user, target=self
        )

        if ENABLE_STATE_CHANGE:
            self.state = SETUP_STATE_POPULATING
            self.save()

        try:
            backend_instance = self.get_backend_instance()

            for item in backend_instance.get_item_list():

                identifer_field = backend_instance.item_identifier
                try:
                    # Try as an attribute.
                    identifier = getattr(item, identifer_field)
                except (AttributeError, TypeError):
                    # Try as dictionary.
                    identifier = item[identifer_field]

                setup_item, created = self.items.get_or_create(
                    identifier=identifier
                )
                if created:
                    setup_item.dump_data(
                        obj=item
                    )
                    setup_item.save()
        except Exception as exception:
            if ENABLE_STATE_CHANGE:
                self.state = SETUP_STATE_ERROR
                self.save()

            self.error_log.create(
                text='{}; {}'.format(
                    exception.__class__.__name__, exception
                )
            )

            if settings.DEBUG:
                raise
        else:
            if ENABLE_STATE_CHANGE:
                self.state = SETUP_STATE_NONE
                self.save()

            event_import_setup_populate_finished.commit(
                actor=user, target=self
            )

            queryset_logs = self.error_log.all()
            queryset_logs.delete()

    def process(self, user=None):
        """
        Iterate of the `ImportSetupItem` instances downloading and creating
        documents from them.
        """
        if ENABLE_STATE_CHANGE:
            self.state = SETUP_STATE_EXECUTING
            self.save()

        event_import_setup_process_started.commit(
            actor=user, target=self
        )

        try:
            count = 0
            eta = datetime.utcnow()
            # Only schedule items that have not succeeded in being imported.
            ImportSetupItem = apps.get_model(
                app_label='importer', model_name='ImportSetupItem'
            )
            queryset = self.items.exclude(
                state__in=ImportSetupItem.get_process_allowed_state_list()
            )
            iterator = queryset.iterator()

            while True:
                item = next(iterator)
                if item.check_valid():
                    count = count + 1
                    eta += timedelta(milliseconds=self.item_time_buffer)
                    task_import_setup_item_process_apply_async(
                        eta=eta, kwargs={
                            'import_setup_item_id': item.pk
                        }
                    )
                    if count >= self.process_size:
                        break
        except StopIteration:
            """
            Expected exception when iterator is exhausted before the process
            size is reached.
            """
        except Exception as exception:
            if ENABLE_STATE_CHANGE:
                self.state = SETUP_STATE_ERROR
                self.save()

            self.error_log.create(
                text=str(exception)
            )

            if settings.DEBUG:
                raise

            # Exit the method to avoid committing the ended event.
            return

        # This line is reached on `StopIteration` or from the break in the
        # loop.
        if ENABLE_STATE_CHANGE:
            self.state = SETUP_STATE_NONE
            self.save()

        queryset = self.error_log.all()
        queryset.delete()

        event_import_setup_process_finished.commit(actor=user, target=self)
