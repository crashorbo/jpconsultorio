$(document).ready(function(){
  $('#myTable').DataTable({
    "language": {
      "sProcessing":     "Procesando...",
      "sLengthMenu":     "Mostrar _MENU_ registros",
      "sZeroRecords":    "No se encontraron resultados",
      "sEmptyTable":     "Ningún dato disponible en esta tabla",
      "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
      "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
      "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
      "sInfoPostFix":    "",
      "sSearch":         "Buscar:",
      "sUrl":            "",
      "sInfoThousands":  ",",
      "sLoadingRecords": "Cargando...",
      "oPaginate": {
        "sFirst":    "Primero",
        "sLast":     "Último",
        "sNext":     "Siguiente",
        "sPrevious": "Anterior"
      },
      "oAria": {
        "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
        "sSortDescending": ": Activar para ordenar la columna de manera descendente"
      }
    },
    "bServerSide": true,
    "sAjaxSource": "/paciente/as_json"
  });

  $('#myTable').on('click','.paciente-eliminar', function(e){
    e.preventDefault();
    $thisUrl = $(this).attr('data-url');
    $.ajax(({
      url: 'ajax/eliminar',
      type: 'get',
      data: {'id': $thisUrl},
      success: function(data){
        $('#myTable').DataTable().ajax.reload(null, false);
      }
    }));
  });
});

$("#registro-paciente").click(function(){
  $.ajax({
    url: 'registrar',
    type: 'get',  
    success: function(data){
        $('#contenido-modal').html(data);
    }
  })
});

$("#myTable").on('click','.paciente-editar',function(e){
  e.preventDefault();
  $this_url = $(this).attr('data-url');
  $.ajax({
    url: $this_url,
    type: 'get',  
    success: function(data){
      $('#contenido-modal').html(data);
      $('#responsive-modal').modal('show');

    }
  })
});

$('#mensaje-modal').on('hidden.bs.modal', function (e) {
  $('#myTable').DataTable().ajax.reload(null, false);
});

$('#myTable').on('click', '.paciente-historial',function(e){
  e.preventDefault();
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

$('#myTable').on('click', '.paciente-examen',function(e){
  e.preventDefault();
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