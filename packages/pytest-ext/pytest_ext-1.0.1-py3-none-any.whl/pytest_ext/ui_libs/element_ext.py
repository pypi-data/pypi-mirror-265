import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebElement
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromService


def chrome_headless_opts():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    return chrome_options


def local_driver(browser):
    if browser == 'chrome_headless':
        driver = webdriver.Chrome(options=chrome_headless_opts())
    else:
        driver = getattr(webdriver, f'{browser.title()}Options')()
    return driver


def remote_driver(svr, browser):
    if browser == 'chrome_headless':
        options = chrome_headless_opts()
    elif browser == 'ie':
        options = webdriver.IeOptions()
    else:
        options = getattr(webdriver, f'{browser.title()}Options')()
    driver = webdriver.Remote(f'http://{svr}', options=options)
    return driver


def get_screen_resolution(driver):
    js = 'var winW = window.screen.width;var winH = window.screen.height;alert(winW+","+winH)'
    driver.execute_script(js)
    line = driver.switch_to_alert().text
    driver.switch_to_alert().accept()
    size = line.split(',')
    resolution = dict()
    resolution['width'] = int(size[0])
    resolution['height'] = int(size[1])
    return resolution


def is_element_existed(method, evalue, timeout=5, locator=None):
    """
    Check if the element exists
    method: id/xpath/name/link text
    evalue: the element value
    Return: True/False
    """
    try:
        pytest.driver.implicitly_wait(timeout)
        if locator:
            locator.find_element(method, evalue)
        else:
            pytest.driver.find_element(method, evalue)
        return True
    except NoSuchElementException:
        return False
    finally:
        pytest.driver.implicitly_wait(5)


class SwitchIframe:
    def __init__(self, iframe):
        self.iframe = iframe

    def __enter__(self):
        if not isinstance(self.iframe, WebElement):
            self.iframe = pytest.driver.switch_to.frame(self.iframe)
        pytest.driver.switch_to.frame(self.iframe)

    def __exit__(self, type, value, traceback):
        pytest.driver.switch_to.default_content()