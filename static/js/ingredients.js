
    document.getElementById('ethical-issues-btn').addEventListener("click", function(){
        
        console.log("anything")
        displayInfo()
    })
    
    function displayInfo(){
        $.ajax({
          url:"/display_info" ,
          type: "POST",
          dataType: "json" ,
          success: function(data){
            let displayDiv = document.getElementById();
            alert("worked twice")
            displayDiv.style.display = "block";
            $(info_display_test).replaceWith(data);
          }
        })
    }

    document.onload(console.log('anything'))
    document.getElementById("demo").addEventListener("click", myFunction);
    
    function myFunction() {
      document.getElementById("demo").innerHTML = "YOU CLICKED ME!";
    }

