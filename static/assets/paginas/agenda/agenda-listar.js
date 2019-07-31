$(document).ready(function(){
  $('.fecha').datepicker({
    autoclose: true,
    todayHighlight: true,
    format: "dd/mm/yyyy",
    language: 'es',
  });
});

$('.fecha').on('change', function(){
  var getUrl = window.location;
  var fecha = ($(this).val()).replace("/","-");
  fecha = fecha.replace("/","-")
  $.ajax({
    url: getUrl.protocol + "//" + getUrl.host+'/agenda/ajax-listar/',
    data: {'fecha': fecha}, 
    type: 'get',  
    success: function(data){
        $('#lista-pacientes').html(data)
    }
  })
});

function imprimirlista(e, obj)
{
  e.preventDefault();
  fecha = $("#fecharepor").val();
  this_url = '/agenda/movimiento/reportemovfecha/'+(fecha.replace("/","-")).replace("/","-");
  window.open(this_url,"reporte","height=600,width=700,status=no, toolbar=no,menubar=no,location=no,scrollbars=yes");
}