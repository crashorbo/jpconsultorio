from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AjaxListView, TableAsJSON, AjaxCrearView, AjaxEditarView, AjaxEliminarView, MedicamentoAutocomplete

urlpatterns = [
  url(r'^as_json/$',login_required(TableAsJSON.as_view()), name='table-as-json'),
  url(r'^medicamento-autocomplete/$', login_required(MedicamentoAutocomplete.as_view()), name='medicamento-autocomplete'),
  path('ajax-lista/', login_required(AjaxListView.as_view()), name='medicamento-ajax-lista'),
  path('ajax-registrar/', login_required(AjaxCrearView.as_view()), name='medicamento-ajax-registrar'),
  path('ajax-editar/<pk>', login_required(AjaxEditarView.as_view()), name='medicamento-ajax-editar'),
  path('ajax-eliminar', login_required(AjaxEliminarView.as_view()), name='medicamento-ajax-eliminar'),
]