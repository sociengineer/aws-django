import boto3
import json
import pandas as pd

# Create SQS client
sqs = boto3.client('sqs', region_name='ap-northeast-2', )

queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/687651457542/s3-sqs-standard-que'

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

message = json.loads(response['Messages'][0]['Body'])
# receipt_handle = message['ReceiptHandle']

bucket_name = json.loads(response['Messages'][0]['Body'])['Records'][0]['s3']['bucket']['name']
file_name = json.loads(response['Messages'][0]['Body'])['Records'][0]['s3']['object']['key']
# receipt_handle = message['ReceiptHandle']


print(bucket_name, file_name)

s3 = boto3.client('s3')
s3.download_file(bucket_name, file_name, file_name)

df = pd.DataFrame(file_name)
print(df)



# Delete received message from queue
# sqs.delete_message(
#     QueueUrl=queue_url,
#     ReceiptHandle=receipt_handle
# )
# print('Received and deleted message: %s' % message)