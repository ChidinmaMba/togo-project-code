var logoutBtn = document.getElementById("logoutBtn");
var writeReviewBtn = document.getElementById("writeReviewBtn");
var listOfReviews = document.getElementById("listOfReviews");

var apigClient = apigClientFactory.newClient();

// var userEmail = "";
// sessionStorage['userEmail'] = "";

console.log(window.location.search);
var accessCode = window.location.search.substring(6);
console.log(accessCode);
  
if (sessionStorage["userEmail"] == null) {
    fetch('https://togoapp.auth.us-east-1.amazoncognito.com/oauth2/token', {
        method: 'POST',
        headers: {
            'Authorization': 'Basic M3M1aWxkNGhraHQyNWVsZ2szOHJhM3Z2OXE6MXBndmdpaGIzZjFhamZzazdhNmJnbDA2YXFsMDEybzc5dHJtbG83bmo1cnY1aGEydDcyNg==',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `grant_type=authorization_code&client_id=3s5ild4hkht25elgk38ra3vv9q&code=${accessCode}&redirect_uri=https://d21eulsh8uxgb2.cloudfront.net/home.html&client_secret=1pgvgihb3f1ajfsk7a6bgl06aql012o79trmlo7nj5rv5ha2t726`
    }).then(response => {
        response = response.json();
        console.log(response);
        response.then(function(result) {
            console.log(result);
            var accessToken = result["access_token"];
            console.log(accessToken);

            fetch('https://cognito-idp-fips.us-east-1.amazonaws.com', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-amz-json-1.1',
                    'X-Amz-Target': 'AWSCognitoIdentityProviderService.GetUser'
                },
                body: `{"AccessToken":"${accessToken}"}`
            }).then(userProfile => {
                console.log(userProfile);
                userProfile = userProfile.json();
                console.log(userProfile);
                userProfile.then(function(profile) {
                    console.log(profile);
                    profile["UserAttributes"].forEach(attr => {
                        if ("Name" in attr && attr["Name"] == "email") {
                            sessionStorage["userEmail"] = attr["Value"];
                            getReviews();
                            console.log(sessionStorage["userEmail"]);
                            return;
                        }
                    });
                });
            });
        });
    });
}

console.log("userEmail", sessionStorage["userEmail"])

logoutBtn.onclick = function() {logout()};
writeReviewBtn.onclick = function() {
    location.href = "review.html";
};

function logout() {
    console.log('Logged out')
    location.href = "index.html";
}

function getReviews() {
    params = {
        "useremail": sessionStorage["userEmail"],
        "businessemail": ""
    };

    if (sessionStorage["userEmail"] == null) {
        return;
    }

    apigClient.reviewsGet(params, {}, {})
    .then((response) => {
        console.log(response);

        reviews = response['data']['reviews'];
        console.log(reviews);

        reviews.forEach(review => {
            let business = review['business-email'];
            let rating = review['rating'];
            let description = review['review'];
            let reply = review['business-reply'];
            if (reply == null) {
                reply = "";
            }

            var templateReviewCard = '<div class="card"><div class="container"><h4><b>' + business + '</b></h4><p>' + rating + '</p><p>' + description + '</p><p>' + reply + '</p></div></div>';

            listOfReviews.insertAdjacentHTML('beforeend', templateReviewCard);
        });
    }).catch((error) => {
        console.log('an error occurred', error);
    });
}

async function getBusinesses() {
    var additionalParams = {latitiude:"40.8139", longitude:"-73.9624", radius:"15km"};
    // var params = {
    //     email: sessionStorage["businessemail"]
    // };
    var body = {};
    var params = {email:""};
    console.log("hereeee")
    await apigClient.businessGet(params, body, additionalParams)
        .then(function(result){
            var map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: 40.8139, lng: -73.9624},
                zoom: 12
                });
            console.log("result", result.data)
            var locations = []
            console.log(result.data.length)
            for(let i = 0; i < result.data.length; i++) {
                console.log(parseFloat(result.data[i]["location"]["M"]["longitude"]["S"]))
                locations.push({
                    lat:parseFloat(result.data[i]["location"]["M"]["longitude"]["S"]).toFixed(4), 
                    lng:parseFloat(result.data[i]["location"]["M"]["latitude"]["S"]).toFixed(4), 
                    name:result.data[i].name.S,
                    cuisine: result.data[i].cuisine["SS"][0],
                    email: result.data[i].email.S})
            }

            for (let i = 0; i < locations.length; i++) {
                var marker = new google.maps.Marker({
                    position: {lat: parseFloat(locations[i].lat), lng: parseFloat(locations[i].lng)},
                    map: map,
                    name: locations[i].name,
                    cuisine: locations[i].cuisine,
                    email: locations[i].email
                });
                console.log(locations[i].lat)
                // Add click event listener to marker
                marker.addListener('click', function() {
                    // Perform action on marker click
                    document.getElementById("business_name").innerHTML = this.name;
                    document.getElementById("cuisine").innerHTML = "Cuisine: " + this.cuisine;
                    document.getElementById("email").innerHTML = "Business Email: " + this.email;
                });
            }
        })  
        .catch( function(result){
            // This is where you would put an error callback
        }); 
}