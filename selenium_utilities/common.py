from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from utilities.project_logger import get_logger
from selenium.webdriver.common.by import By
from time import sleep
from utilities.allure_methods import allure_screenshot

logger = get_logger(logger_name=__name__)

class SeleniumCore:
    """A class that contains all common selenium methods for easier reusability when instantiating the class"""

    def __init__(self, web_driver: Chrome) -> None:
        """A constructor that gets intialized with the chrome driver"""

        self.driver = web_driver

    def get_url(self, url) -> None:
        """Loads a web page in the current browser instance"""

        self.driver.get(url=url)

    def click(self, locator: tuple, timeout=10) -> None:
        """A method to click an element"""

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            element.click()
        except Exception:
            logger.exception(f"Failed to click locator: {locator}")
    
    def input(self, locator: tuple, value: str, timeout=10) -> None:
        """Input method sets text into an editable element"""

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(value)
        except Exception as e:
            logger.exception(f"Failed to input field: {locator}")

    def does_element_exist(self, locator: tuple) -> bool:
        """Validate if an element exists"""

        try:
            self.driver.find_element(by=locator[0], value=locator[1])
        except NoSuchElementException:
            return False
        
        return True

    def children_in_parent(self, child_locator: tuple, parent_locator: tuple, goal_locator: tuple) -> list:
        """Extract values from a parent element"""

        parent_div = self.driver.find_element(by=parent_locator[0], value=parent_locator[1])
        child_divs = parent_div.find_elements(by=child_locator[0], value=child_locator[1])

        product_names = []

        for child_div in child_divs:
            try:
                product_name = child_div.find_element(by=goal_locator[0], value=goal_locator[1]).text
                product_names.append(product_name)
            except NoSuchElementException:
                continue
        
        return product_names

    def _create_a_highlight(self, locator: tuple, color) -> None:
        """Create a highlight for an element with a border"""

        highlight_js = f"""
        var div = document.evaluate("{locator[1]}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (div !== null) {{
            div.setAttribute("style", "outline: {color} solid 2px;");
        }}
        """
        try:
            self.driver.execute_script(highlight_js)
            logger.info(f"Highlighted: {self.driver.find_element(locator[0], locator[1]).tag_name}")
        except JavascriptException:
            logger.exception("Could not create a highlight")

    def _remove_a_highlight(self, locator: tuple) -> None:
        """Remove a highlight for an element with a border"""

        remove_highlight = f"""
        var div = document.evaluate("{locator[1]}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (div !== null) {{
            div.removeAttribute("style");
        }}
        """

        try:
            self.driver.execute_script(remove_highlight)
        except JavascriptException:
            logger.exception("Could not remove the highlight")

    def wait_until_body_is_loaded(self, timeout: float = 10) -> None:
        """Wait until the body has finished rendering"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception:
            logger.exception("An error occured while waiting for the body to load")

    def get_full_screenshot(self, message: str = "Full screenshot"):
        """Take the entire webpage a screenshot"""
        
        self.wait_until_body_is_loaded()
        
        original_size = self.driver.get_window_size()
        required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')

        self.driver.set_window_size(required_width, required_height)
        allure_screenshot(driver=self.driver, message=message)
        self.driver.set_window_size(original_size['width'], original_size['height'])

    def highlight_and_screenshot(self, locator: tuple, color: str = "red", message: str = "Took screenshot") -> None:
        """Highlight an element and then screenshot"""

        self.wait_until_body_is_loaded()
        self._create_a_highlight(locator=locator, color=color)
        allure_screenshot(driver=self.driver, message=message)
        self._remove_a_highlight(locator=locator) 

    def get_current_url(self) -> str:
        """Method of the WebDriver interface to get the current URL of the web page"""

        return self.driver.current_url
    
    def get_text_from_element(self, locator: tuple) -> str | None:
        """Extracting text from a web element"""

        try:
            return self.driver.find_element(by=locator[0], value=locator[1]).text
        except NoSuchElementException:
            logger.exception("Failed to locate element")
            return None
        
    def get_value_from_element(self, locator: tuple) -> str | None:
        """Extracting the attribute value from an element (usually input fields)"""

        try:
            return self.driver.find_element(by=locator[0], value=locator[1]).get_attribute("value")
        except NoSuchElementException:
            logger.exception("Failed to locate element")
            return None
    
    def is_element_clickable(self, locator: tuple) -> bool:
        """Checks if an element located by the provided locator is clickable."""

        try:
            element = WebDriverWait(driver=self.driver, timeout=5).until(
                EC.element_to_be_clickable(locator)
            )

            return True
        except TimeoutException:
            return False