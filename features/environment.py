import logging
import os

from globebotter.llm import LLM_MODEL


def before_all(context):
    # Configure basic logging to a file
    logging.basicConfig(
        filename="behave_test.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    context.logger = logging.getLogger("behave_logger")

    context.llm_model = os.environ.get("LLM_MODEL", LLM_MODEL)
    logging.info(f"Running tests using LLM = {context.llm_model}")


def before_scenario(context, scenario):
    context.logger.info(f"{scenario}")
    # If the cosine similarity between the actual and expected responses
    # is less than this value, a test will fail. This value can be overridden
    # with a step like
    # 'Given the similarity should be at least 0.7'
    if context.llm_model == LLM_MODEL:
        context.minimum_good_similarity = 0.8
    else:
        context.minimum_good_similarity = 0.5
