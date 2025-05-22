from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_iot as iot,
)
from constructs import Construct

class CdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. สร้าง S3 Bucket
        bucket = s3.Bucket(self, "IoTDataBucket")

        # 2. สร้าง DynamoDB Table
        table = dynamodb.Table(
            self, "IoTDataTable",
            partition_key={"name": "deviceId", "type": dynamodb.AttributeType.STRING},
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # 3. สร้าง Lambda function
        iot_lambda = _lambda.Function(
            self, "IoTHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="handler.main",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TABLE_NAME": table.table_name
            }
        )

        # 4. ให้ Lambda เขียน S3 และ DynamoDB ได้
        bucket.grant_put(iot_lambda)
        table.grant_write_data(iot_lambda)

        # 5. สร้าง IoT Topic Rule → Trigger Lambda
        iot.CfnTopicRule(self, "IoTRule",
            topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                sql="SELECT * FROM 'iot/topic'",
                actions=[
                    iot.CfnTopicRule.ActionProperty(
                        lambda_=iot.CfnTopicRule.LambdaActionProperty(
                            function_arn=iot_lambda.function_arn
                        )
                    )
                ],
                rule_disabled=False
            )
        )
