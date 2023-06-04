import allure
from allure_commons.types import AttachmentType
from selenium.webdriver import Chrome
from .project_logger import get_logger

logger = get_logger(logger_name=__name__)

def log_to_allure(message: str, data: any = None) -> None:
    """Log an allure step"""

    with allure.step(f"{message}: {data if data != None else ''}"):
        logger.info("{}: {}".format(message, data if data != None else ''))


def allure_screenshot(driver: Chrome, message: str = "Result screenshot") -> None:
    """Capture a screenshot and add it to the results"""

    allure.attach(
        driver.get_screenshot_as_png(),
        name=message,
        attachment_type=AttachmentType.PNG
    )


def assert_with_allure(condition: bool = None, message: str = None, data: any = None) -> None:
    """Assert a condition and log the step using allure"""

    if condition is None:
        raise TypeError("The condition must be a boolean")
    
    if message is None:
        raise TypeError("The message must not be None")
    
    with allure.step(f"{message}: {data}"):

        if not condition:
            logger.error("{}: \n{}".format(message, data))
        else:
            logger.info("{}: \n{}".format(message, data))

        assert condition, message