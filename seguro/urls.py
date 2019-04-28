from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, SeguroRegistrar


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='seguro-index'),
    path('registrar', login_required(SeguroRegistrar.as_view()), name='seguro-registrar'),
    #path('editar/<int:pk>', login_required(PacienteEditar.as_view()), name='paciente-editar')
]