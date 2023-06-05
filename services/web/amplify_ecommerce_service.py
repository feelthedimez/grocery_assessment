import re
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from selenium_utilities.common import SeleniumCore
from utilities.path_finder import get_path_to_file
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file

logger = get_logger(logger_name=__name__)

class AmplifyEcommerce:
    """A server/helper for the Amplify Ecommerce Feature"""

    def __init__(self, driver: Chrome) -> None:
        self.selenium_core = SeleniumCore(web_driver=driver)
        self.driver = driver
        self.default_config = read_config_file()
        self.locator_config = read_config_file(config_path=get_path_to_file('configs', 'web', 'locators.ini'))

    def screenshot(self, message: str = "Screenshot captured") -> None:
        """Take a screenshot of the page"""

        self.selenium_core.get_full_screenshot(message=message)

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
            
    def navigate_to_specials(self) -> None:
        """Navigating to the specials page"""

        config_locator = self.locator_config
        self.selenium_core.click(locator=(By.CSS_SELECTOR, config_locator['css']['specials_nav']))
        sleep(3)

    def extract_cost_from_item(self, product_name: str):
        """Extract the cost of an item from the product objetc"""

        config_locator = self.locator_config
        goal_locator= (By.XPATH, config_locator['xpath']['product_name'])

        child_divs = self.children_product_elements()

        for child_div in child_divs:
            try:
                product = child_div.find_element(by=goal_locator[0], value=goal_locator[1]).text

                if product == product_name:
                    cost = child_div.find_element(by=By.XPATH, value=config_locator['xpath']['item_cost'])
                    return cost.text
            except NoSuchElementException:
                pass

    def remove_specific_words(self, string, words_to_remove: list) -> str:
        """Removes specific words from a given string."""

        for word in words_to_remove:
            string = string.replace(word, "")

        return string

    def specials_url(self) -> str:
        """Get the specials URL"""

        return self.selenium_core.get_current_url()
    
    def total_cost_cart(self):
        """ """

        config_locator = self.locator_config
        total = self.selenium_core.get_text_from_element(locator=(By.CSS_SELECTOR, config_locator['css']['cart_total']))

        return self.extract_money(money_string=total)

    def extract_money(self, money_string: str) -> float | None:
        """Extracts the monetary value from a given string"""

        pattern = r"Total Price: R(\d+\.\d{2})"
        match = re.search(pattern, money_string)

        if match:
            money_str = match.group(1)
            money_float = float(money_str)
            return money_float
        
        return None
    
    def navigate_to_cart(self):
        """Navigate to the cart page"""

        config_locator = self.locator_config
        self.selenium_core.click(locator=(By.XPATH, config_locator['xpath']['cart_icon']))

    def extract_items_number_cart(self) -> int:
        """Extract the number of items in a cart from the cart icon"""

        config_locator = self.locator_config
        return int(self.selenium_core.get_text_from_element(locator=(By.CSS_SELECTOR, config_locator['css']['cart_counter'])))
    
    def increment_cart(self) -> None:
        """Click on the increment button in the cart"""

        config_locator = self.locator_config
        self.selenium_core.click(locator=(By.XPATH, config_locator['xpath']['increment_cart']))


    def decrement_cart(self) -> None:
        """Click on the decrement button in the cart"""

        config_locator = self.locator_config
        self.selenium_core.click(locator=(By.XPATH, config_locator['xpath']['decrement_cart']))
        self.selenium_core._create_a_highlight(locator=(By.XPATH, config_locator['xpath']['decrement_cart']), color="red")
