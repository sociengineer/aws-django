import boto3

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/687651457542/s3-ec2'

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)

message = response['Messages'][0]
receipt_handle = message['ReceiptHandle']

print(message)

# Delete received message from queue
# sqs.delete_message(
#     QueueUrl=queue_url,
#     ReceiptHandle=receipt_handle
# )
# print('Received and deleted message: %s' % message)