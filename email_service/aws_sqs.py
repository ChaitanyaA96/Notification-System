import uuid

import boto3
import json
from keys.keys import SQS_URL, RECEIPIENT_EMAIL, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from event import event

session = boto3.session.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
sqs = session.client('sqs')
queue_url = SQS_URL


def send_message(event):
    from_user = event.initiated_by
    to_user = event.target_group
    event_type = event.event_type

    message = {
        'body': f'{from_user} has {event_type} on {to_user}',
        'recipients': RECEIPIENT_EMAIL,
        'subject': f' Someone has {event_type}d you',
    }
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message),
        MessageGroupId= "transactional_email",
        MessageDeduplicationId=str(uuid.uuid4())
    )
    print(f"Message sent")