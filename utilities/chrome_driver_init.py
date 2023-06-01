from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .path_finder import get_path_to_file


def initialize_driver():
    """
    Initilizing chrome driver
    :returns: The web driver with correct options and configurations
    """

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}

    return webdriver.Chrome(
        executable_path=get_path_to_file('drivers', 'chromedriver.exe'),
        options=chrome_options,
    )
