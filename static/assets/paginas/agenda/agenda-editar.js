$(document).ready(function(){
  $('#paciente-espera').on('click', function(e){
    $.ajax({
      url: Urls.agenda_espera(),
      type: 'get',  
      success: function(data){
        $('.chatonline').html(data);
      }
    })
  });
  selectipo();
});

$(document).keydown(function(e) { 
  if (e.keyCode == 38) {
    $(this).next('.form-control').focus();
    console.log('arriba')
  } 
  if (e.keyCode == 40) {
    $(this).prev('.form-control').focus();
    console.log('abajo')
  }
});

$('#historiac').on('click', function(e){
  $this_url = $(this).attr('data-url');
  $.ajax({
    url: $this_url,
    type: 'get',  
    success: function(data){
      $('#lmcontenido').html(data);
      $('#lmodal').modal('show');
    }
  })
});

$('#form-guardar').on('submit', function (e) {
  e.preventDefault();
  var $formData = $(this).serialize();
  var $formArray = $(this).serializeArray();
  var $formArray = {};
  $.each($(this).serializeArray(), function (i, field) {
    $formArray[field.name] = field.value; 
  });
  var $thisUrl = $(this).attr('action');
  var $thisMethod = $(this).attr('method');
  $.ajax({
      method: $thisMethod,
      url: $thisUrl,
      data: $formData,
      success: function(data){
        $.toast({
          heading: 'Administracion Consulta',
          text: 'Se ha Guardado el registro con exito.',
          position: 'top-right',
          loaderBg:'#ff6849',
          icon: 'success',
          hideAfter: 3500, 
          stack: 6
        });
      },
      error: function(xhr,errmsg,err) {
        // Show an error
        $('#results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  })
});

$('#diagform').on('submit', function (e) {
  e.preventDefault();
  var $formData = $(this).serialize();
  var $formArray = $(this).serializeArray();
  var $formArray = {};
  $.each($(this).serializeArray(), function (i, field) {
    $formArray[field.name] = field.value; 
  });
  var $thisUrl = $(this).attr('action');
  var $thisMethod = $(this).attr('method');
  $.ajax({
      method: $thisMethod,
      url: $thisUrl,
      data: $formData,
      success: function(data){
        $('.enviod').val('');
        $("#diagnosticos").html(data);
      },
      error: function(xhr,errmsg,err) {
        // Show an error
        $('#results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  })
});

var autoguardado = function(){
  var $formData = $("#form-guardar").serialize();
  var $formArray = $("#form-guardar").serializeArray();
  var $formArray = {};
  $.each($("#diagform").serializeArray(), function (i, field) {
    $formArray[field.name] = field.value; 
  });
  var $thisUrl = $("#form-guardar").attr('action');
  var $thisMethod = $("#form-guardar").attr('method');
  $.ajax({
      method: $thisMethod,
      url: $thisUrl,
      data: $formData,
      success: function(data){
        console.log("guardado");
      },
      error: function(xhr,errmsg,err) {
        // Show an error
        $('#results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  })
}

$('#tratform').on('submit', function (e) {
  e.preventDefault();
  var $formData = $(this).serialize();
  var $formArray = $(this).serializeArray();
  var $formArray = {};
  $.each($(this).serializeArray(), function (i, field) {
    $formArray[field.name] = field.value; 
  });
  var $thisUrl = $(this).attr('action');
  var $thisMethod = $(this).attr('method');
  $.ajax({
      method: $thisMethod,
      url: $thisUrl,
      data: $formData,
      success: function(data){
        $('.enviot').val('');
        $("#tratamientos").html(data);
      },
      error: function(xhr,errmsg,err) {
        // Show an error
        $('#results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  })
});

$('#diagnosticos').on('submit', '.form-eliminar-diag', function (e) {
  e.preventDefault();
  var $formData = $(this).serialize();
  var $formArray = $(this).serializeArray();
  var $formArray = {};
  $.each($(this).serializeArray(), function (i, field) {
    $formArray[field.name] = field.value; 
  });
  var $thisUrl = $(this).attr('action');
  var $thisMethod = $(this).attr('method');
  $.ajax({
      method: $thisMethod,
      url: $thisUrl,
      data: $formData,
      success: function(data){
        $('#diagnosticos').html(data);
      },
      error: function(xhr,errmsg,err) {
        // Show an error
        $('#results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  })
});

$('#tratamientos').on('submit', '.form-eliminar-trat', function (e) {
  e.preventDefault();
  var $formData = $(this).serialize();
  var $formArray = $(this).serializeArray();
  var $formArray = {};
  $.each($(this).serializeArray(), function (i, field) {
    $formArray[field.name] = field.value; 
  });
  var $thisUrl = $(this).attr('action');
  var $thisMethod = $(this).attr('method');
  $.ajax({
      method: $thisMethod,
      url: $thisUrl,
      data: $formData,
      success: function(data){
        $('#tratamientos').html(data);
      },
      error: function(xhr,errmsg,err) {
        // Show an error
        $('#results').html("<div class='alert-box alert radius' data-alert>"+
        "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  })
});
function imprimirlista(e, obj)
{
  e.preventDefault();
  this_url = $(obj).attr('href');
  window.open(this_url,"reporte","height=600,width=700,status=no, toolbar=no,menubar=no,location=no,scrollbars=yes");
}


$('#selectipo').on('change', function(){
  var aux = [];
  var valor = "";
  aux = $(this).val();
  aux.forEach(element => {
    if (valor == "")
      valor = element;
    else
      valor = valor+","+element;
  });
  $('#id_tipo_lente').val(valor);
  autoguardado()
});

function selectipo(){
  var valor = "";
  var aux = [];
  valor = $('#id_tipo_lente').val();
  aux = valor.split(",")
  $('#selectipo').selectpicker('val', aux);
}
$('.autoguardado').on('change', function(){
  autoguardado();
});
$('#id_dre1').on('change', function(){
  $('#id_drc1').val(transformador($(this).val()));
  autoguardado();
});
$('#id_dre2').on('change', function(){
  $('#id_drc2').val(transformador($(this).val()));
  autoguardado();
});
$('#id_dre3').on('change', function(){
  $('#id_drc3').val($(this).val());
  autoguardado();
});
$('#id_ddc2').on('change', function(){
  $('#id_adicion').val(transformador($(this).val()));
  autoguardado();
});
$('#id_ire1').on('change', function(){
  $('#id_irc1').val(transformador($(this).val()));
  autoguardado();
});
$('#id_ire2').on('change', function(){
  $('#id_irc2').val(transformador($(this).val()));
  autoguardado();
});
$('#id_ire3').on('change', function(){
  $('#id_irc3').val($(this).val());
  autoguardado();
});

function transformador(t){
  var dosdecimales = parseFloat(t).toFixed(2);
  if(isNaN(dosdecimales))
  {
    return "";
  }
  else{
    if(dosdecimales==0)
    {
      return "";
    }
    if(dosdecimales > 0)
    {
      dosdecimales = '+'+dosdecimales;
    }
  }
  return dosdecimales;
}