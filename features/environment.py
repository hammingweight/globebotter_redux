import logging


def before_all(context):
    # Configure basic logging to a file
    logging.basicConfig(
        filename="behave_test.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    context.logger = logging.getLogger("behave_logger")
    # If the cosine similarity between the actual and expected responses
    # is less than this value, a test will fail. This value can be overridden
    # with a step like
    # 'Given the minimum good cosine similarity should be at least 0.7'
    context.minimum_good_similarity = 0.5
