import aws_cdk as core
import aws_cdk.assertions as assertions

from customer_profiles_streaming_dynamodb.customer_profiles_streaming_dynamodb_stack import CustomerProfilesStreamingDynamodbStack

# example tests. To run these tests, uncomment this file along with the example
# resource in customer_profiles_streaming_dynamodb/customer_profiles_streaming_dynamodb_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CustomerProfilesStreamingDynamodbStack(app, "customer-profiles-streaming-dynamodb")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
