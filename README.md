# Introduction

This is a small utility intended to automatically generate data catalogs in markdown from a given Glue table.

Main use case is reducing the manual work when creating data catalogs for complying with data privacy regulations.

If your application writes custom logs or stores other data on AWS you can proceed as follows:
- send a sample to an S3 bucket (or another service that can be crawled by glue like DynamoDB or RDS)
- <a href="https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html">crawl the data with Glue</a> so that a Glue data catalog is created automatically
- run this solution on the glue catalog/database to get an initial version of your data documentation
- add the missing information (manually) in the table

# Prerequisites/Requirements

its recommended to use Cloud9 since all tools/libs are preinstalled by default

for a local setup you will need
    - Python3
    - Nodejs (compatible with the CDK!)
    - AWS CLI
    - AWS CDK

# Deployment

First clone this project

```
$ git clone https://github.com/aperov9/glue-datacatalog-to-markdown.git
```

Now create a virtualenv

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv on MacOS & Linux.

```
$ source .env/bin/activate
```

If you are on a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

If its your first CDK deployment in your AWS you have to bootstrap your environment first.

```
$ cdk bootstrap aws://<aws-account-id>/<aws-region>
```

Lastly, you can deploy everything

```
$ cdk deploy
```

# Usage of Lambda

After the Stack has been rolled out sucessfully you can define which glue database to use.

Go to Lambda -> Applications -> select this project. Now you can see all components.

Select the Lambda function, change the environment variable GLUE_DATABASE_NAME and run the function.  

The lambda function will put markdown files for each table in the selected glue database into an S3 bucket in your account.

# Example output

```
<table name>
============

|Nr|Datenfeldbezeichnung|Datentyp|Personengruppe|Verwendungszweck|Nutzungsdauer und Loeschung|
| :---: | :---: | :---: | :---: | :---: | :---: |
|0|<colname-0>|bigint|keine|-||
|1|<colname-1|string|keine|-||
|2|<colname-2>|string|keine|-||
|3|>colname-n>|string|keine|-||
```

which looks in Markdown like this:

|Nr|Datenfeldbezeichnung|Datentyp|Personengruppe|Verwendungszweck|Nutzungsdauer und Loeschung|
| :---: | :---: | :---: | :---: | :---: | :---: |
|0|<colname-0>|bigint|keine|-||
|1|<colname-1>|string|keine|-||
|2|<colname-2>|string|keine|-||
|3|<colname-n>|string|keine|-||
