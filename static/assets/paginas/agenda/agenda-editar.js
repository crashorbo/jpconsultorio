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
});

$('#historiac').on('click', function(e){
  alert($(this).attr('data-paciente'));
  $('#lmodal').modal('show');
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
        $("#msj-modal").html(data);
        $("#responsive-modal").modal('hide');
        $("#mensaje-modal").modal('show');
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