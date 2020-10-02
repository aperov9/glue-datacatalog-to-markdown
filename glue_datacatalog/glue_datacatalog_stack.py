from aws_cdk import (
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_iam as iam,
    core
)

class GlueDatacatalogStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        glue_database_name="<ENTER YOUR GLUE DATABASE NAME>"
        
        outputbucket = s3.Bucket(self, "OutputBucket", removal_policy=core.RemovalPolicy.DESTROY);
        main_lambda = lambda_.Function(self, "MainLambda", 
                                        runtime= lambda_.Runtime.PYTHON_3_8,
                                        handler='handler.lambda_handler',
                                        code= lambda_.Code.asset('./lambda'),
                                        environment={"GLUE_DATABASE_NAME": glue_database_name,
                                                     "BUCKET_NAME": outputbucket.bucket_name});
                                        
        main_lambda.role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=[outputbucket.arn_for_objects("*")],
            actions=["s3:PutObject"],
            )
        )
        main_lambda.role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["glue:GetTables"],
            )
        )
            
        outputbucket.add_to_resource_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["s3:PutObject"],
            resources=[outputbucket.arn_for_objects("*")],
            principals=[main_lambda.role]))
        