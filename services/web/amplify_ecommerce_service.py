from time import sleep
from selenium_utilities.common import SeleniumCore
from selenium.webdriver import Chrome
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file

logger = get_logger(logger_name=__name__)

class AmplifyEcommerce:
    """A server/helper for the Amplify Ecommerce Feature"""

    def __init__(self, driver: Chrome) -> None:
        self.selenium_core = SeleniumCore(web_driver=driver)
        self.driver = driver

    def login(self, username: str, password: str):

        config_file = read_config_file(section='auth')
        url = f"https://{username}:{password}@{config_file['auth_url']}"
        self.selenium_core.get_url(url=url)
        sleep(20)

