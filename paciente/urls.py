from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, PacienteRegistrar, PacienteEditar


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='paciente-index'),
    path('registrar', login_required(PacienteRegistrar.as_view()), name='paciente-registrar'),
    path('editar/<int:pk>', login_required(PacienteEditar.as_view()), name='paciente-editar')
]