from django.shortcuts import render
from django.views.generic import TemplateView, View
# Create your views here.


# Vista Inicial de la aplicacion
class IndexView(TemplateView):
    template_name = 'core/index.html'

class AjaxTiempoView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        data["ano"] = time.strftime("%Y")
        data["mes"] = time.strftime("%m")
        data["dia"] = time.strftime("%d")
        data["hora"] = time.strftime("%H")
        data["minuto"] = time.strftime("%M")
        data["segundo"] = time.strftime("%S")

        return JsonResponse(data)