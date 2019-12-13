from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import IndexView, PacienteRegistrar, PacienteEditar, TableAsJSON, PacienteEliminar, \
    ArchivopdfListar, ArchivopdfCrear, ArchivoPdfEliminar, UltimaconPaciente

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='paciente-index'),
    url(r'^as_json/$',login_required(TableAsJSON.as_view()), name='table-as-json'),
    path('registrar', login_required(PacienteRegistrar.as_view()), name='paciente-registrar'),
    path('editar/<pk>', login_required(PacienteEditar.as_view()), name='paciente-editar'),
    path('ajax/eliminar', login_required(PacienteEliminar.as_view()), name='paciente-eliminar'),
    path('archivopdf/<pk>', login_required(ArchivopdfListar.as_view()), name='archivopdf-listar'),
    path('crear/archivopdf', login_required(ArchivopdfCrear.as_view()), name='archivopdf-crear'),
    path('eliminar/archivopdf/<pk>', login_required(ArchivoPdfEliminar.as_view()), name='archivopdf-eliminar'),
    url(r'^ultimacon/$', login_required(UltimaconPaciente.as_view()), name='paciente-ultimacon'),
]