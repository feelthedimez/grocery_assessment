from time import sleep
from selenium_utilities.common import SeleniumCore
from selenium.webdriver import Chrome
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file
from utilities.path_finder import get_path_to_file
from selenium.webdriver.common.by import By

logger = get_logger(logger_name=__name__)

class AmplifyEcommerce:
    """A server/helper for the Amplify Ecommerce Feature"""

    def __init__(self, driver: Chrome) -> None:
        self.selenium_core = SeleniumCore(web_driver=driver)
        self.driver = driver
        self.default_config = read_config_file()
        self.locator_config = read_config_file(config_path=get_path_to_file('configs', 'web', 'locators.ini'))

    def login(self, username: str, password: str) -> None:
        """Using basic auth to login to the web app"""

        config_auth = self.default_config['auth']
        url = f"https://{username}:{password}@{config_auth['auth_url']}"
        self.selenium_core.get_url(url=url)

    def search_category(self, category: str) -> None:
        """Search for a specific category"""

        config_locator = self.locator_config
        self.selenium_core.input((By.XPATH, config_locator['xpath']['category_search']), category)

        self.selenium_core.highlight_and_screenshot(
            locator=(By.XPATH, config_locator['xpath']['products_container'])
        )

    def all_products_from_screen(self) -> list:
        """Extract all products from the screen"""

        config_locator = self.locator_config

        products = self.selenium_core.children_in_parent(
            parent_locator=(By.XPATH, config_locator['xpath']['parents_products']),
            child_locator=(By.TAG_NAME, config_locator['tag']['child_product']),
            goal_locator=(By.XPATH, config_locator['xpath']['product_name'])
        )

        return products
