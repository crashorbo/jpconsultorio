$(document).ready(function(){
  $('#seguros').on('click', function(e){
    e.preventDefault();
    $thisUrl = $(this).attr("href");
    $.ajax({
      method: "get",
      url: $thisUrl,
      success: function(data){
        $("#mainbody").html(data);
      }  
    })
  });
  $('#servicios').on('click', function(e){
    e.preventDefault();
    $thisUrl = $(this).attr("href");
    $.ajax({
      method: "get",
      url: $thisUrl,
      success: function(data){
        $("#mainbody").html(data);
      }  
    })
  })
  $('#tipolentes').on('click', function(e){
    e.preventDefault();
    $thisUrl = $(this).attr("href");
    $.ajax({
      method: "get",
      url: $thisUrl,
      success: function(data){
        $("#mainbody").html(data);
      }  
    })
  })
  $('#medicamentos').on('click', function(e){
    e.preventDefault();
    $thisUrl = $(this).attr("href");
    $.ajax({
      method: "get",
      url: $thisUrl,
      success: function(data){
        $("#mainbody").html(data);
      }  
    })
  })
});