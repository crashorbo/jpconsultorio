from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import IndexView, GeneralView, SeguroView, GeneralajaxView, GeneralformView, SeguroajaxView, SeguroformView,\
    SeguroPdfView

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='reporte-index'),
    path('general/', login_required(GeneralView.as_view()), name='reporte-general'),
    path('general-ajax/<pk>', login_required(GeneralajaxView.as_view()), name='reporte-general-ajax'),
    path('general-form/<pk>', login_required(GeneralformView.as_view()), name='reporte-general-form'),
    path('seguro/', login_required(SeguroView.as_view()), name='reporte-seguro'),
    path('seguro-ajax/<pk>/<int:gestion>', login_required(SeguroajaxView.as_view()), name='reporte-seguro'),
    path('seguro-form/<pk>/<int:gestion>', login_required(SeguroformView.as_view()), name='reporte-seguro-form'),
    path('seguro-pdf/<pk>', login_required(SeguroPdfView.as_view()), name='reporte-seguro-pdf'),
]
