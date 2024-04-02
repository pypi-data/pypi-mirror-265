import logging

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.views import (
    ViewSingleObjectDynamicFormModelBackendCreate,
    ViewSingleObjectDynamicFormModelBackendEdit
)
from mayan.apps.views.generics import (
    FormView, SingleObjectDeleteView, SingleObjectListView
)

from ..classes import ImportSetupBackend
from ..forms import (
    ImportSetupBackendSelectionForm, ImportSetupBackendDynamicForm
)
from ..icons import (
    icon_import_setup_backend_selection, icon_import_setup_delete,
    icon_import_setup_edit, icon_import_setup_list
)
from ..links import link_import_setup_backend_selection
from ..models import ImportSetup
from ..permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_view
)

logger = logging.getLogger(name=__name__)


class ImportSetupBackendSelectionView(FormView):
    extra_context = {
        'title': _('New import backend selection')
    }
    form_class = ImportSetupBackendSelectionForm
    view_icon = icon_import_setup_backend_selection
    view_permission = permission_import_setup_create

    def form_valid(self, form):
        backend = form.cleaned_data['backend']
        return HttpResponseRedirect(
            redirect_to=reverse(
                kwargs={'backend_path': backend},
                viewname='importer:import_setup_create'
            )
        )


class ImportSetupCreateView(ViewSingleObjectDynamicFormModelBackendCreate):
    backend_class = ImportSetupBackend
    form_class = ImportSetupBackendDynamicForm
    post_action_redirect = reverse_lazy(viewname='importer:import_setup_list')
    view_icon = icon_import_setup_backend_selection
    view_permission = permission_import_setup_create

    def get_extra_context(self):
        backend_class = self.get_backend_class()
        return {
            'title': _(
                'Create a "%s" import setup'
            ) % backend_class.label
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['backend_path']
        }


class ImportSetupDeleteView(SingleObjectDeleteView):
    model = ImportSetup
    object_permission = permission_import_setup_delete
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(viewname='importer:import_setup_list')
    view_icon = icon_import_setup_delete

    def get_extra_context(self):
        return {
            'import_setup': None,
            'object': self.object,
            'title': _('Delete the import setup: %s?') % self.object
        }


class ImportSetupEditView(ViewSingleObjectDynamicFormModelBackendEdit):
    form_class = ImportSetupBackendDynamicForm
    model = ImportSetup
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_id'
    view_icon = icon_import_setup_edit

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit import setup: %s') % self.object
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ImportSetupListView(SingleObjectListView):
    model = ImportSetup
    object_permission = permission_import_setup_view
    view_icon = icon_import_setup_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_import_setup_list,
            'no_results_main_link': link_import_setup_backend_selection.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Import setups are configuration units that will retrieve '
                'files for external locations and create documents from '
                'them.'
            ),
            'no_results_title': _('No import setups available'),
            'title': _('Import setups')
        }
