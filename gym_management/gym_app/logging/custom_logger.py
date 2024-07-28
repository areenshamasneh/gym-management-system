import logging


class CustomLogger:
    def __init__(self):
        self.logger = logging.getLogger("AdminComponent")
        self.logger.setLevel(logging.DEBUG)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler("logs/logging.log")

        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.ERROR)

        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)
