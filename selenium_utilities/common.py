from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.support import expected_conditions as EC
from utilities.project_logger import get_logger

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

    def _create_a_highlight(self, locator: tuple, color):
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

    def _remove_a_highlight(self, locator: tuple):
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

    def get_current_url(self):
        """Method of the WebDriver interface to get the current URL of the web page"""

        return self.driver.current_url