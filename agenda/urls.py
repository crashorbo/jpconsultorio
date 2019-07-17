from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import IndexView, PacienteAutocomplete, AgendaRegistrar, AgendaAjaxEditar, AgendaAjaxLista, AgendaListar, AgendaEditar, DiagnosticoCrear, DiagnosticoEliminar, TratamientoCrear, TratamientoEliminar, AgendaAjaxDelete, AgendaAjaxEspera, Reportemov, AgendaservUpdate, Reporterec, AgendaFechaListar, HistoriaListar, HistoriaVer, AgendaAjaxRegistrar, RecetaCrear, RecetaEliminar, ReporteRecmed


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='agenda-index'),
    url(r'^paciente-autocomplete/$', login_required(PacienteAutocomplete.as_view()), name='paciente-autocomplete'),
    url(r'^ajax-listar/$', login_required(AgendaFechaListar.as_view()), name='agenda-ajax-lista'),
    path('registrar', login_required(AgendaRegistrar.as_view()), name='agenda-registrar'),
    path('registrar-ajax', login_required(AgendaAjaxRegistrar.as_view()), name='agenda-ajax-registrar'),
    path('ajax-lista', login_required(AgendaAjaxLista.as_view()), name='agenda-ajax-lista'),
    path('listar', login_required(AgendaListar.as_view()), name='agenda-listar'),
    path('movimiento/reportmov', login_required(Reportemov.as_view()), name='reportemov'), 
    path('reporte-receta/<pk>',login_required(Reporterec.as_view()), name='reporterec'),
    path('reporte-receta-oftal/<pk>',login_required(ReporteRecmed.as_view()), name='reportereceta'),
    path('espera', login_required(AgendaAjaxEspera.as_view()), name='agenda_espera'),
    path('consulta/<pk>', login_required(AgendaEditar.as_view()), name='agenda-editar'),
    path('historias/<pk>', login_required(HistoriaListar.as_view()), name='historia-lista'),
    path('historiaver/<pk>', login_required(HistoriaVer.as_view()), name='historia-ver'),
    path('eliminarajax/<pk>', login_required(AgendaAjaxDelete.as_view()), name='agenda-eliminarajax'),
    path('editarajax/<pk>', login_required(AgendaAjaxEditar.as_view()), name='agenda-editarajax'),
    path('diagnostico/crear', login_required(DiagnosticoCrear.as_view()), name='diagnostico-crear'), 
    path('diagnostico/<pk>/eliminar', login_required(DiagnosticoEliminar.as_view()), name='diagnostico-eliminar'),
    path('tratamiento/crear', login_required(TratamientoCrear.as_view()), name='tratamiento-crear'),
    path('tratamiento/<pk>/eliminar', login_required(TratamientoEliminar.as_view()), name='tratamiento-eliminar'),
    path('receta/crear', login_required(RecetaCrear.as_view()), name='receta-crear'),
    path('receta/<pk>/eliminar', login_required(RecetaEliminar.as_view()), name='receta-eliminar'),
    path('agendaserv/<pk>/cobrar', login_required(AgendaservUpdate.as_view()), name='agendaserv-cobrar'),
]