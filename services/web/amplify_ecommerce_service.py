from time import sleep
from selenium_utilities.common import SeleniumCore
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
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

    def children_product_elements(self):
        """All products elements from the parent element"""

        config_locator = self.locator_config
    
        parent_container = (By.XPATH, config_locator['xpath']['parents_products'])
        child_containers = (By.TAG_NAME, config_locator['tag']['child_product'])

        parent_div = self.driver.find_element(by=parent_container[0], value=parent_container[1])
        return parent_div.find_elements(by=child_containers[0], value=child_containers[1])

    def add_product_to_cart(self, product_name: str, items_to_add: str, add_to_cart: bool = True) -> None:
        """Add product to cart by deciding on the incrementor"""
        
        config_locator = self.locator_config

        goal_locator= (By.XPATH, config_locator['xpath']['product_name'])    

        child_divs = self.children_product_elements()
    
        for child_div in child_divs:
            try:
                product = child_div.find_element(by=goal_locator[0], value=goal_locator[1]).text

                if product == product_name:
                    increment_locator = child_div.find_element(by=By.XPATH, value=config_locator['xpath']['plus_btn'])
                    add_to_cart_locator = child_div.find_element(by=By.XPATH, value=config_locator['xpath']['add_to_cart'])

                    for _ in range(int(items_to_add)):
                        increment_locator.click()
                    
                    if add_to_cart:
                        add_to_cart_locator.click()
                    break

            except NoSuchElementException:
                pass

    def alert_message(self) -> str | None:
        """Extract the alert message after adding product to cart"""

        config_locator = self.locator_config
        alert_locator = (By.XPATH, config_locator['xpath']['add_alert'])

        alert_msg = self.selenium_core.get_text_from_element(locator=alert_locator)

        self.selenium_core.highlight_and_screenshot(
            locator=alert_locator,
            message="Alert message popped up",
            color="green"
        )
        
        return alert_msg

    def decrement_products(self, product_name: str, items_to_add: str) -> None:
        """Decrement items based on items added"""

        config_locator = self.locator_config
        goal_locator= (By.XPATH, config_locator['xpath']['product_name'])

        child_divs = self.children_product_elements()

        for child_div in child_divs:
            try:
                product = child_div.find_element(by=goal_locator[0], value=goal_locator[1]).text

                if product == product_name:
                    decrement = child_div.find_element(by=By.XPATH, value=config_locator['xpath']['minus_btn'])
                    
                    for _ in range(int(items_to_add)):
                        decrement.click()

                    break
            except NoSuchElementException:
                pass
    
    def input_item_value(self, product_name: str, items_to_add: int):
        """Input the value of product items"""
        
        self.selenium_core.wait_until_body_is_loaded()
        
        config_locator = self.locator_config
        goal_locator= (By.XPATH, config_locator['xpath']['product_name'])

        child_divs = self.children_product_elements()

        for child_div in child_divs:
            try:
                product = child_div.find_element(by=goal_locator[0], value=goal_locator[1]).text

                if product == product_name:
                    incrementor_value = child_div.find_element(by=By.XPATH, value=config_locator['xpath']['incrementor_value'])

                    incrementor_value.clear()
                    incrementor_value.send_keys(items_to_add)
                    
                    break
            except NoSuchElementException:
                pass

    def get_current_item_value(self, product_name: str) -> str | None:
        """Get the current item value from the product"""

        config_locator = self.locator_config
        goal_locator= (By.XPATH, config_locator['xpath']['product_name'])

        child_divs = self.children_product_elements()

        for child_div in child_divs:
            try:
                product = child_div.find_element(by=goal_locator[0], value=goal_locator[1]).text

                if product == product_name:
                    return self.selenium_core.get_value_from_element(locator=(By.XPATH, config_locator['xpath']['incrementor_value']))

            except NoSuchElementException:
                return None

    def is_button_active(self, product_name) -> bool | None:
        """Validate if the button is active"""

        config_locator = self.locator_config
        goal_locator= (By.XPATH, config_locator['xpath']['product_name'])

        child_divs = self.children_product_elements()

        for child_div in child_divs:
            try:
                product = child_div.find_element(by=goal_locator[0], value=goal_locator[1]).text

                if product == product_name:
                    logger.info(product_name)
                    add_to_cart_locator = (By.XPATH, config_locator['xpath']['add_to_cart'])                    
                    return self.selenium_core.is_element_clickable(add_to_cart_locator) 

            except NoSuchElementException:
                return None