### Requirements
- The [serverless](https://serverless.com/) framework for creating the Cognito userpool.

### How to deploy and configure this project

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


### Using postman to access APIs

The postman collection can be found here: https://www.getpostman.com/collections/3f95225750a80feaa16a

Import the collection into your postman app. `File > Import > Import From Link` 


### Sign-up/Sign-in and getting a user token.

- I've created a simple webpage to help with signup. Once you have configured the cognito_config.js file, 
	-	click on the index.html file in the root folder to register a user
	-	validate the user with the verification code sent to the email
	-	login with the username and password to get the user token



### Design Considerations
-	We don't need to create a seperate API for user sign-up and sign-in Cognito provides us with a API for user registration and login. I've decided to use that instead of create a pass through API for this feature.
-	