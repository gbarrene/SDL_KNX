$(document).ready(function() {
    $('#slider-range-max').slider({
        range: 'max',
        min: 0,
        max: 100,
        value: 10, // Set actual value FOR TEST PURPOSE 10
        slide: function(event, ui) {
            $('#amount').val(ui.value);
        },
        change: skillLevel
    });
    
    $('#amount').val($('#slider-range-max').slider('value'));
    
    var script = $("<script />", {
    src: "http://192.168.1.11:5000/test",
    type: "application/json"
  }
);

$("head").append(script);
    
    // POST slider's value to Python
    function skillLevel() {
        // do something based upon slider value
        $('#test').append('#');  
        
        console.log($('#amount').val());

        // Create object with value and send it with AJAX
        var obj = {"testValue" : $('#amount').val()};
        
        console.log($('#amount').val());
        
        $.ajax({
            url: 'http://192.168.1.11:5000/test',
            type: 'POST',
            ContentType: 'application/json', 
            data: "{'data': 'test'}",
            //dataType: "html",   // Expect html to be returned                
            success: function(response){                    
                $("header div").html(response);
            }
            /*success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }*/
        });
    };
});