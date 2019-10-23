## Requirements
- The [serverless](https://serverless.com/) framework for deploying the functions and creating required AWS resources.

## How to deploy and configure this project

NOTE: You can skip this section if you'd just like to use my deployed service. By default, when you clone this repo and download the postman collection linked below, everything will be pointing to my deployed environment.

This repo uses the serverless framework to deploy the project. Please install it first. Link provided above.

- Clone this repo `git clone git@github.com:murali44/Hackathon.git`

- Run the deploy command in the repo root folder. `sls deploy -v`

- Note the following outputs once the deployment is successful.

	`Stack Outputs`

	`UserPoolId: us-east-1_aUIYzcnd2`

	`ClientId: 5s8p640r6a7h5q8qpjehco520`

- Update the config file `/js/cognito_config.js` with the Id's from the previous step
```
window._config = {
    cognito: {
        userPoolId: 'us-east-1_aUIYzcnd2',
        region: 'us-east-1',
        clientId: '5s8p640r6a7h5q8qpjehco520'
    },
};
```

All the AWS recourses are defined in the serverless.yml file. Addtional resource definitions can be found in the /resources folder



## Sign-up/Sign-in and getting a user token.

- I've created a simple webpage to help with signup. Once you have configured the cognito_config.js file, 
	-	click on the index.html file in the root folder to register a user
	-	validate the user with the verification code sent to the email
	-	login with the username and password to get the user token

![Token](https://i.ibb.co/XxhK5R1/Screen-Shot-2019-08-14-at-4-41-32-PM.png "Token")

You'll need this token for accessing all the API's via Postman


## Using postman to access APIs

The postman collection can be found here:
[https://www.getpostman.com/collections/3f95225750a80feaa16a](https://www.getpostman.com/collections/3f95225750a80feaa16a)

Import the collection into your postman app. `File > Import > Import From Link` 

##### API Testing


Use postman to talk to the API's. By default the collection has all requests pointing to my deployed environment.


- You'll need to update the `Authorization` header with a valid token you received when you logged in earlier.

![Auth Header](https://i.ibb.co/gwSnCRy/auth-header.png "Auth Header")

- Update the Json body with the paramentes you want to test.

![Body Json](https://i.ibb.co/kMsHpdp/body.png "Body Json")




## Design Considerations
-	We don't need to create a seperate API for user sign-up and sign-in Cognito provides us with a API for user registration and login. I've decided to use that instead of create a pass through API for this feature.
-	All API's are configured to use the CognitoAuthorizer. The APIGateway expects a header named `Authorizer` in all requests with a valid user token.
