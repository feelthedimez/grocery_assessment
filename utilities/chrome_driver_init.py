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
    chrome_options.add_argument('--headless') # comment this out if you wish to see the gui

    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
