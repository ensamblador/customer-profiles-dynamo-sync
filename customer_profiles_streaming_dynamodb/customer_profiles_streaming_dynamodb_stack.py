from aws_cdk import (
    Stack,
    aws_kinesis as kinesis,
    aws_lambda_event_sources,
    aws_iam as iam,

    aws_lambda
)
from constructs import Construct

from lambdas import Lambdas
from databases import Tables

class CustomerProfilesStreamingDynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Fn = Lambdas(self, "L")
        T  = Tables(self, "T")


        kinesis_stream = kinesis.Stream(
            self, "KinesisStream",
            stream_name="customer-profiles"
        )

        kinesis_stream.grant_read(Fn.connect_stream_processor) 

        Fn.connect_stream_processor.add_event_source(
            aws_lambda_event_sources.KinesisEventSource(
                kinesis_stream, starting_position=aws_lambda.StartingPosition.TRIM_HORIZON
            )
        )

        T.profiles.grant_stream_read(Fn.dynamo_stream_processor)
        T.profiles.grant_full_access(Fn.dynamo_stream_processor)
        T.profiles.grant_full_access(Fn.connect_stream_processor)

        Fn.connect_stream_processor.add_environment(key="TABLE_NAME", value=T.profiles.table_name)
        Fn.dynamo_stream_processor.add_environment(key="TABLE_NAME", value=T.profiles.table_name)


        Fn.dynamo_stream_processor.add_event_source(
            aws_lambda_event_sources.DynamoEventSource(
                table=T.profiles, 
                starting_position=aws_lambda.StartingPosition.TRIM_HORIZON)
        )
        Fn.dynamo_stream_processor.add_to_role_policy(iam.PolicyStatement(actions=["profile:*"], resources=['*']))
