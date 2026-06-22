import logging

class Logger:
    logger = logging.getLogger("poligrafo")

    @staticmethod
    def setup():
        logging.basicConfig(
            level=logging.INFO,
            format="\033[94m[%(asctime)s]\033[0m \033[92m[%(levelname)s]\033[0m %(message)s",
            datefmt="%H:%M:%S"
        )