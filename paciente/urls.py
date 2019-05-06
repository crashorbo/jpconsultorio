from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import IndexView, PacienteRegistrar, PacienteEditar, TableAsJSON

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='paciente-index'),
    url(r'^as_json/$',login_required(TableAsJSON.as_view()), name='table-as-json'),
    path('registrar', login_required(PacienteRegistrar.as_view()), name='paciente-registrar'),
    path('editar/<int:pk>', login_required(PacienteEditar.as_view()), name='paciente-editar')
]