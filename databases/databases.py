from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as ddb
)
from constructs import Construct


REMOVAL_POLICY = RemovalPolicy.DESTROY

TABLE_CONFIG = dict (removal_policy=REMOVAL_POLICY, billing_mode= ddb.BillingMode.PAY_PER_REQUEST)


class Tables(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.profiles = ddb.Table(
            self, "CustomerProfiles", 
            partition_key=ddb.Attribute(name="ProfileId", type=ddb.AttributeType.STRING),
            stream=ddb.StreamViewType.NEW_AND_OLD_IMAGES,
            **TABLE_CONFIG)