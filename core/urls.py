from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, MovimientoCalculoView


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('movcalculo', login_required(MovimientoCalculoView.as_view()), name='ajaxmov_calculo'),
]