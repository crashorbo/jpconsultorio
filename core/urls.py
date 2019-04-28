from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import IndexView, AjaxTiempoView


urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('ajax-tiempo', login_required(AjaxTiempoView.as_view()), name='ajax-tiempo')
]