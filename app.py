from aws_cdk import App, Environment
from cdk_project.cdk_project_stack import CdkProjectStack
import os

app = App()

CdkProjectStack(app, "CdkProjectStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION")
    )
)

app.synth()
