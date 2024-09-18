from services.aws_services.sqs_service import SQSService


class ServiceFactory:
    @staticmethod
    def get_sqs_service(queue_url):
        return SQSService(queue_url)
