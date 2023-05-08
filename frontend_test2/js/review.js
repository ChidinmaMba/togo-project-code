var closeBtn = document.getElementById("closeBtn");
var submitReviewBtn = document.getElementById("submitReviewBtn");
var ratingInput = document.getElementById("ratingInput");
var descriptionInput = document.getElementById("descriptionInput");
var businessEmailInput = document.getElementById("businessEmailInput");

var apigClient = apigClientFactory.newClient();

closeBtn.onclick = function() {
    location.href = "home.html";
};

submitReviewBtn.onclick = function() {
    body = {
        "user-email": sessionStorage["userEmail"],
        "business-email": businessEmailInput.value,
        "rating": ratingInput.value,
        "review": descriptionInput.value,
        "business-reply": ""
    };

    apigClient.reviewPut({}, body, {})
    .then((response) => {
        // Clear fields
        businessEmailInput.value = "";
        ratingInput.value = "";
        descriptionInput.value = "";
        // Open popup indicating success to user
        alert('Review was successfully submitted!');
        // Redirect to user home page
        location.href = "home.html";
    }).catch((error) => {
        console.log('an error occurred', error);
    });
};