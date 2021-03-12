$("button").click(function(){
    alert("Processing Image");
    $.ajax({dataType: "json", url: "/predictcolor", success: function(result){
      //test = JSON.parse(result); 
      red = Math.round(result[0].color[0]);
      green = Math.round(result[0].color[1]);
      blue = Math.round(result[0].color[2]);

      $.ajax({dataType: "json", url: "/matchfoundation/"+red+"/"+green+"/"+blue, success: function(result2){
        //test = JSON.parse(result); 
        if(!jQuery.isEmptyObject(result2))
        {
            alert("The closest shade match is: " + result2[0].brand + " " + result2[0].shade);

            var html = "Brand: " + result2[0].brand + "<br>"
            + "Product: " + result2[0].product + "<br>"
            + "Shade: " + result2[0].shade + "<br>";
        
            $('.panel2-body').html(html);
        }    
        else 
            alert("No Shades Found");
    
      }});
    }});
  });
  
