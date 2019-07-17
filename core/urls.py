from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, MovimientoCalculoView, ServicioCostoView


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('movcalculo', login_required(MovimientoCalculoView.as_view()), name='ajaxmov_calculo'),
    path('servicio-costo', login_required(ServicioCostoView.as_view()), name="servicio_costo")
]