var loginAsUserBtn = document.getElementById("loginAsUserBtn");
var loginAsBusinessBtn = document.getElementById("loginAsBusinessBtn");

loginAsUserBtn.onclick = function() {userLogin()};
loginAsBusinessBtn.onclick = function() {businessLogin()};

function userLogin() {
    console.log('Open Amazon Cognito as user');
    location.href = "https://togoapp.auth.us-east-1.amazoncognito.com/login?client_id=3s5ild4hkht25elgk38ra3vv9q&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+profile&redirect_uri=https%3A%2F%2Fd21eulsh8uxgb2.cloudfront.net%2Fhome.html";
}

function businessLogin() {
    console.log('Open Amazon Cognito as business');
    location.href = "https://togoapp-businesses.auth.us-east-1.amazoncognito.com/login?client_id=5fu191vd265c8tme5vfh843dh1&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone&redirect_uri=https%3A%2F%2Fd21eulsh8uxgb2.cloudfront.net%2Fbusiness.html";
}
Alt+Q