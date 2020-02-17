from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import IndexView, GeneralView, SeguroView, GeneralajaxView, GeneralformView

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='reporte-index'),
    path('general/', login_required(GeneralView.as_view()), name='reporte-general'),
    path('general-ajax/<pk>', login_required(GeneralajaxView.as_view()), name='reporte-general-ajax'),
    path('general-form/<pk>', login_required(GeneralformView.as_view()), name='reporte-form'),
    path('seguro/', login_required(SeguroView.as_view()), name='reporte-seguro'),
]
