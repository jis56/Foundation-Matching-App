function findmatch() {
    $.getJSON('/predictcolor', {
    }, function(data) {
      ulta_data = data;
      createChart();
    })
    .fail(function() { alert("error"); })
    //.always(function() { alert("complete"); });
    return false;
}; 