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
  console.log(fecha)
  $.ajax({
    url: getUrl.protocol + "//" + getUrl.host+'/agenda/ajax-listar/',
    data: {'fecha': fecha}, 
    type: 'get',  
    success: function(data){
        $('#lista-pacientes').html(data)
    }
  })
});