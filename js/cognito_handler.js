var username;
var password;
var personalname;
var poolData;
var otp;


// Register a user
function registerButton() {
    personalnamename = document.getElementById("personalnameRegister").value;
    username = document.getElementById("preferredUsernameRegister").value;
    email = document.getElementById("emailInputRegister").value;
    phonenumber = document.getElementById("phoneInputRegister").value;

    if (document.getElementById("passwordInputRegister").value != document.getElementById("confirmationpassword").value) {
        alert("Passwords Do Not Match!")
        throw "Passwords Do Not Match!"
    } else {
        password = document.getElementById("passwordInputRegister").value;
    }

    poolData = {
        UserPoolId: _config.cognito.userPoolId, // Your user pool id here
        ClientId: _config.cognito.clientId // Your client id here
    };
    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    var attributeList = [];

    var dataPreferred_username = {
        Name: 'preferred_username',
        Value: username, //get from form field
    };

    var dataEmail = {
        Name: 'email',
        Value: email, //get from form field
    };

    var dataPersonalName = {
        Name: 'name',
        Value: personalname, //get from form field
    };

    var dataPhonenumber = {
        Name: 'phone_number',
        Value: phonenumber, //get from form field
    };


    var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);
    var attributePersonalName = new AmazonCognitoIdentity.CognitoUserAttribute(dataPersonalName);
    var attributePhonenumber = new AmazonCognitoIdentity.CognitoUserAttribute(dataPhonenumber);
    var attributePreferedUsername = new AmazonCognitoIdentity.CognitoUserAttribute(dataPreferred_username);


    attributeList.push(attributeEmail);
    attributeList.push(attributePersonalName);
    attributeList.push(attributePhonenumber);
    attributeList.push(attributePreferedUsername);


    userPool.signUp(username, password, attributeList, null, function (err, result) {
        if (err) {
            alert(err.message || JSON.stringify(err));
            return;
        }
        cognitoUser = result.user;
        // store email number locally (per domain) for login.
        localStorage.setItem("email", username);
        //verify email
        showVerifyForm()
    });
}


// Phone number MFA
function verifyButton() {
    otp = document.getElementById("otp").value;

    var poolData = {
        UserPoolId: _config.cognito.userPoolId, // Your user pool id here
        ClientId: _config.cognito.clientId // Your client id here
    };

    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var userData = {
        Username: localStorage.getItem("email"),
        Pool: userPool
    };

    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
    cognitoUser.confirmRegistration(otp, true, function (err, result) {
        if (err) {
            alert(err);
            return;
        }
    });

    showLoginForm()
}


// Login
function loginButton() {
    var authenticationData = {
        Username: document.getElementById("username").value,
        Password: document.getElementById("password").value,
    };

    var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);

    var poolData = {
        UserPoolId: _config.cognito.userPoolId, // Your user pool id here
        ClientId: _config.cognito.clientId, // Your client id here
    };

    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

    var userData = {
        Username: document.getElementById("username").value,
        Pool: userPool,
    };

    var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

    cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function (result) {
            var IdToken = result.getIdToken().getJwtToken();
            // Store the token locally, so we can send it in the Auth headers to the API.
            localStorage.setItem("IdToken", IdToken);
            window.location.href = '/success.html';
        },

        onFailure: function (err) {
            alert(err.message || JSON.stringify(err));
        },
    });
}


function signOut() {
    var poolData = {
        UserPoolId: _config.cognito.userPoolId, // Your user pool id here
        ClientId: _config.cognito.clientId, // Your client id here
    };

    var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
    var cognitoUser = userPool.getCurrentUser();

    if (cognitoUser != null) {
        cognitoUser.signOut();
        // Delete the token from local storage locally.
        localStorage.setItem("IdToken", "");
        window.location.href = '/index.html';
    }
}



function showLoginForm() {
    $('#verify-modal').modal('hide');
    $('#signup-modal').modal('hide');
    $('#login-modal').modal('show');
}


function showVerifyForm() {
    $('#signup-modal').modal('hide');
    $('#login-modal').modal('hide');
    $('#verify-modal').modal('show');
}


function showSignupForm() {
    $('#verify-modal').modal('hide');
    $('#login-modal').modal('hide');
    $('#signup-modal').modal('show');
}


function hideLoginForm() {
    $('#login-modal').modal('hide');
}
