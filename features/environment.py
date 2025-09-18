import logging
import os

from globebotter.llm import LLM_MODEL


def before_all(context):
    context.logger = logging.getLogger("behave_logger")
    context.logger.setLevel(logging.INFO)
    handler = logging.FileHandler("behave_test.log")
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    context.logger.addHandler(handler)

    context.llm_model = os.environ.get("LLM_MODEL", LLM_MODEL)
    logging.info(f"Running tests using LLM = {context.llm_model}")


def before_scenario(context, scenario):
    context.logger.info(f">>> {scenario.name}")


def after_scenario(context, scenario):
    context.logger.info("<<<")
