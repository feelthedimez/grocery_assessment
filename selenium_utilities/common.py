from selenium.webdriver import Chrome

class SeleniumCore:
    """A class that contains all common selenium methods for easier reusability when instantiating the class"""

    def __init__(self, driver: Chrome):
        """A constructor that gets intialized with the chrome driver"""

        self.driver = driver

    def get_url(self, url):
        """Loads a web page in the current browser instance"""

        self.driver.get(url=url)

    
    