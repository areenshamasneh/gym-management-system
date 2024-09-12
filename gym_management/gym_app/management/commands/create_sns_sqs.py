import json
from gym_management.settings import LOCALSTACK_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION
from django.core.management.base import BaseCommand
import boto3


class Command(BaseCommand):
    help = 'Create SNS topic and SQS queue in LocalStack and subscribe the SQS queue to the SNS topic.'

    def handle(self, *args, **kwargs):
        if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, LOCALSTACK_URL]):
            raise ValueError("One or more environment variables are not set.")

        sns = boto3.client(
            'sns',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=LOCALSTACK_URL
        )

        sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=LOCALSTACK_URL
        )

        sns_response = sns.create_topic(Name='TestTopic')
        topic_arn = sns_response['TopicArn']
        self.stdout.write(self.style.SUCCESS(f'Topic ARN: {topic_arn}'))

        sqs_response = sqs.create_queue(QueueName='TestQueue')
        queue_url = sqs_response['QueueUrl']
        self.stdout.write(self.style.SUCCESS(f'Queue URL: {queue_url}'))

        queue_attributes = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['QueueArn']
        )
        queue_arn = queue_attributes['Attributes']['QueueArn']
        self.stdout.write(self.style.SUCCESS(f'Queue ARN: {queue_arn}'))

        sns.subscribe(
            TopicArn=topic_arn,
            Protocol='sqs',
            Endpoint=queue_arn
        )

        self.stdout.write(self.style.SUCCESS('Subscription created between SNS and SQS'))

        # Save ARN and URL to a JSON file
        with open('config.json', 'w') as config_file:
            json.dump({
                'TOPIC_ARN': topic_arn,
                'QUEUE_URL': queue_url
            }, config_file)
