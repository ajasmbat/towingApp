console.log("Connected")

var locationData = {
        "long": 0,
        "lat": 0,
}

function sendData() {
    $.ajax({
        type: "POST",
        url: "/request/",  // Replace with the actual URL of your Django view
        data: JSON.stringify(locationData),
        contentType: "application/json",
        headers: {
            "X-CSRFToken": csrfToken,
            
        },
        success: function(response) {
          console.log(response);
          // Handle the response from the server
        },
        error: function(error) {
          console.log(error);
          // Handle any errors that occur during the request
        }
      });
}

function success(pos){

    console.log("Hello");


    locationData.lat = pos.coords.latitude;
    locationData.long = pos.coords.longitude;
    console.log(locationData.lattitude);
    sendData();

}




document.getElementById("getLocationBtn").addEventListener("click", function() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success);
      } else {
        console.log("Geolocation is not supported by this browser.");
      }
});
    


