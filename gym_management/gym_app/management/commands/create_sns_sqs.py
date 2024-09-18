from django.core.management.base import BaseCommand
import boto3
from gym_management.settings import LOCALSTACK_URL, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_REGION, QUEUE_URL

class Command(BaseCommand):
    help = 'Create multiple SNS topics and SQS queue, and subscribe SQS to each topic.'

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

        topics = ['Topic1', 'Topic2']
        topic_arns = []
        for topic_name in topics:
            sns_response = sns.create_topic(Name=topic_name)
            topic_arn = sns_response['TopicArn']
            topic_arns.append(topic_arn)
            self.stdout.write(self.style.SUCCESS(f'Topic ARN created: {topic_arn}'))

        sqs_response = sqs.create_queue(QueueName='Queue')
        queue_url = sqs_response['QueueUrl']
        self.stdout.write(self.style.SUCCESS(f'Queue URL: {queue_url}'))

        queue_attributes = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['QueueArn']
        )
        queue_arn = queue_attributes['Attributes']['QueueArn']
        self.stdout.write(self.style.SUCCESS(f'Queue ARN: {queue_arn}'))

        for topic_arn in topic_arns:
            sns.subscribe(
                TopicArn=topic_arn,
                Protocol='sqs',
                Endpoint=queue_arn
            )
            self.stdout.write(self.style.SUCCESS(f'Subscription created between {topic_arn} and {queue_arn}'))
