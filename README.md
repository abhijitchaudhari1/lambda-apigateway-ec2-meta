# How to use
* clone the repo
* Install serverless. `npm install -g serverless`
* cd `lambda-apigateway-ec2-meta`
* Run `npm install --save-dev  serverless-python-requirements`
* Edit the `serverless.yml`
```
  Config to look for
  1. deploymentBucket -> name
  2. profile
  3. region
 ````
* Deploy using "sls deploy"
