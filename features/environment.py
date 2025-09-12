import logging


def before_all(context):
    # Configure basic logging to a file
    logging.basicConfig(
        filename="behave_test.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    context.logger = logging.getLogger("behave_logger")
