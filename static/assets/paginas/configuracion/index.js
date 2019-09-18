var myChart = echarts.init(document.getElementById('bar-chart'));

$(document).ready(function(){
  $.get('/grafico').done(function(data){
    myChart.setOption({
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['Particular','Seguro']
        },
        toolbox: {
            show : true,
            feature : {
                
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
            }
        },
        color: ["#55ce63", "#009efb"],
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data : ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'Particular',
                type:'bar',
                data:data.particular,
                markPoint : {
                    data : [
                        {type : 'max', name: 'Max'},
                        {type : 'min', name: 'Min'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: 'Media'}
                    ]
                }
            },
            {
                name:'Seguro',
                type:'bar',
                data:data.seguro,
                markPoint : {
                    data : [
                        {type : 'average', name: 'Media'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name : 'Media'}
                    ]
                }
            }
        ]
    }), $(function() {
        function resize() {
            setTimeout(function() {
                myChart.resize();
            }, 100);
        }
        $(window).on("resize", resize), $(".sidebartoggler").on("click", resize)
    });
  });
  $('#inicio').on('click', function(e){
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
  $('#rptmensual').on('click', function(e){
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
  $('#rptseguros').on('click', function(e){
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

$(function() {
  
  // elementos de la lista
  var menues = $("ul li"); 
  var selector = $("ul li a"); 

  $(menues[0]).addClass("active");
  // manejador de click sobre todos los elementos
  menues.click(function() {
    // eliminamos active de todos los elementos
    menues.removeClass("active");
    selector.removeClass("active");
    // activamos el elemento clicado.
    $(this).addClass("active");
  });

});
$('#gestionsel').on('change', function (e) {
   $.get('/graficofecha/'+$(this).val()).done(function(data){
    myChart.setOption({
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['Particular','Seguro']
        },
        toolbox: {
            show : true,
            feature : {

                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
            }
        },
        color: ["#55ce63", "#009efb"],
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data : ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'Particular',
                type:'bar',
                data:data.particular,
                markPoint : {
                    data : [
                        {type : 'max', name: 'Max'},
                        {type : 'min', name: 'Min'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: 'Media'}
                    ]
                }
            },
            {
                name:'Seguro',
                type:'bar',
                data:data.seguro,
                markPoint : {
                    data : [
                        {type : 'average', name: 'Media'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name : 'Media'}
                    ]
                }
            }
        ]
    }), $(function() {
        function resize() {
            setTimeout(function() {
                myChart.resize();
            }, 100);
        }
        $(window).on("resize", resize), $(".sidebartoggler").on("click", resize)
    });
  });
});