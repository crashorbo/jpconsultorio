from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import AjaxListView, TableAsJSON, AjaxCrearView, AjaxEditarView, AjaxEliminarView


urlpatterns = [
  url(r'^as_json/$',login_required(TableAsJSON.as_view()), name='table-as-json'),
  path('ajax-lista/', login_required(AjaxListView.as_view()), name='seguro-ajax-lista'),
  path('ajax-registrar/', login_required(AjaxCrearView.as_view()), name='seguro-ajax-registrar'),
  path('ajax-editar/<pk>', login_required(AjaxEditarView.as_view()), name='seguro-ajax-editar'),
  path('ajax-eliminar', login_required(AjaxEliminarView.as_view()), name='seguro-ajax-eliminar'),
]