from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import IndexView, PacienteAutocomplete, AgendaRegistrar, AgendaAjaxEditar, AgendaAjaxLista, AgendaListar, AgendaEditar, DiagnosticoCrear, DiagnosticoEliminar, TratamientoCrear, TratamientoEliminar, AgendaAjaxDelete, AgendaAjaxEspera


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='agenda-index'),
    url(r'^paciente-autocomplete/$', login_required(PacienteAutocomplete.as_view()), name='paciente-autocomplete'),
    path('registrar', login_required(AgendaRegistrar.as_view()), name='agenda-registrar'),
    path('ajax-lista', login_required(AgendaAjaxLista.as_view()), name='agenda-ajax-lista'),
    path('listar', login_required(AgendaListar.as_view()), name='agenda-listar'),
    path('espera', login_required(AgendaAjaxEspera.as_view()), name='agenda_espera'),
    path('editar/<pk>', login_required(AgendaEditar.as_view()), name='agenda-editar'),
    path('historia/<pk>', login_required(AgendaEditar.as_view()), name='agenda-editar'),
    path('eliminarajax/<pk>', login_required(AgendaAjaxDelete.as_view()), name='agenda-eliminarajax'),
    path('editarajax/<pk>', login_required(AgendaAjaxEditar.as_view()), name='agenda-editarajax'),
    path('diagnostico/crear', login_required(DiagnosticoCrear.as_view()), name='diagnostico-crear'), 
    path('diagnostico/<pk>/eliminar', login_required(DiagnosticoEliminar.as_view()), name='diagnostico-eliminar'),
    path('tratamiento/crear', login_required(TratamientoCrear.as_view()), name='tratamiento-crear'),
    path('tratamiento/<pk>/eliminar', login_required(TratamientoEliminar.as_view()), name='tratamiento-eliminar'), 
]