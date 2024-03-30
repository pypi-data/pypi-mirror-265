import inspect
import logging
import re
import time

from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .element_ext import is_element_existed

logger = logging.getLogger(__name__)


class BasicElement(object):
    def __init__(self, driver):
        self.driver = driver

    def get_el_type_xpath(self, el_type, label=None, attr=None, num=1, partial_matching=False):
        self.el_xpath_mappings = {
            'input': "input[@type='text' or @type='password' or not(@type) or @type='PASSWORD' or @type='search']",
            'checkbox': "input[@type='checkbox']",
            'select': 'select',
            'radio_button': "input[@type='radio']",
            'textarea': 'textarea',
            'upload_file': "input[@type='file']",
            'icon': f"*[contains(@class,'{attr}') or contains(@*,'{attr}') or contains(@id,'{attr}')]"
                    if partial_matching else f"*[@class='{attr}' or @*='{attr}' or @id='{attr}']",
            "text": f"*[text()[normalize-space() = '{label}']][{num}]" if label and "'" not in label else f'*[text()[normalize-space() = "{label}"]][{num}]',
            "link": f"a[.//text()[normalize-space() = '{label}']][{num}]",
            "button": '|'.join(["input[@type='button' or @type='submit'][@value='{0}']",
                                "button[.//text()[normalize-space() = '{0}']]",
                                "*[@role='button' and .//text()[normalize-space() = '{0}']]"]).format(label)
        }
        return self.el_xpath_mappings.get(el_type)

    def get_section(self, section=None, target=None, partial_matching=False, ignore_hidden=False):
        """
        A locator which is used to narrow down the scope when the current page include more than one element with the same name.
        para: {'section':None, 'target':None, 'ignore_hidden':False}
        """
        if isinstance(section, WebElement):
            return {'loc': section, 'xpath': None}
        elif isinstance(section, dict):
            try:
                inspect.getcallargs(self.driver.find_element, **section)
                loc = self.driver.find_element(**section)
                return {'loc': loc, 'xpath': section['value'] if section['by'] == 'xpath' else None}
            except TypeError:
                pass

            try:
                inspect.getcallargs(self.text, **section)
                beo = self.element(**section)
                return {'loc': beo.loc, 'xpath': beo.xpath[1] if beo.xpath else None}
            except TypeError:
                pass
        elif isinstance(section, str):
            parent_xpath = f"/descendant::*[text()[normalize-space() = '{section}']]"
            i = 1
            while not self.driver.find_element_by_xpath(f'{parent_xpath}[{i}]').is_displayed():
                i += 1
            parent_xpath = "%s[%s]" % (parent_xpath, i)
            if target in self.el_xpath_mappings.values():
                target_xpath = f'.//{target}'
            else:
                target_xpath = f".//*[text()[normalize-space() = '{target}'] or @value='{target}']" if not partial_matching else f".//*[contains(normalize-space(text()), '{target}') or contains(@value,'{target}')]"
            while True:
                parent_loc = self.driver.find_element_by_xpath(parent_xpath)
                if not is_element_existed("xpath", target_xpath, 0, parent_loc):
                    parent_xpath += "/parent::*"
                elif ignore_hidden and True not in map(lambda x: x.is_displayed(), parent_loc.find_elements_by_xpath(target_xpath)):
                    parent_xpath += "/parent::*"
                else:
                    return {'loc': parent_loc, 'xpath': parent_xpath}
        else:
            return {'loc': self.driver.find_element_by_xpath('*'), 'xpath': '/*'}

    def __webElement(self, label=None, attr=None, partial_matching=False, ignore_hidden=False,
                     axes='descendant', num=1, section=None, comment=None):
        el_type = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        label_xpath = f"/descendant::*[text()[normalize-space() = '{label}'] or @aria-label[normalize-space() = '{label}']]" if not partial_matching else f"/descendant::*[contains(normalize-space(text()), '{label}') or contains(normalize-space(@aria-label), '{label}')]"
        el_xpath = self.get_el_type_xpath(el_type=el_type, label=label, attr=attr, num=num,
                                          partial_matching=partial_matching)

        section_obj = self.get_section(
            section=section, target=label or el_type,
            partial_matching=partial_matching, ignore_hidden=ignore_hidden
        )
        section_loc = section_obj['loc']
        if not label:
            element_root_loc = section_loc
            if ignore_hidden:
                num = 1
                while not section_loc.find_element_by_xpath(f"./descendant::{el_xpath}[{num}]").is_displayed():
                    num += 1
            target_xpath = f"./descendant::{el_xpath}[{num}]"
            complete_xpath = target_xpath.replace("./descendant", f"{section_obj['xpath']}/descendant") if section_obj['xpath'] else None
        else:
            if ignore_hidden:
                i = 1
                while not section_loc.find_element_by_xpath(f".{label_xpath}[{i}]").is_displayed():
                    i += 1
                label_xpath = f"{label_xpath}[{i}]"
            while True:
                element_root_loc = section_loc.find_element_by_xpath(f".{label_xpath}")
                target_xpath = f"./{axes}::{el_xpath}[{num}]"
                if axes == 'descendant' and not is_element_existed("xpath", ".//%s" % el_xpath, 0, element_root_loc):
                    label_xpath += "/parent::*"
                else:
                    break
            complete_xpath = "%s%s%s" % (section_obj['xpath'], label_xpath, target_xpath.replace(f"./{axes}", f"/{axes}")) if section_obj['xpath'] else None
        target_loc = element_root_loc.find_element_by_xpath(target_xpath)
        logger.info(f"[{el_type}: '{label or comment}']ELEMENT XPATH: {complete_xpath}")
        return BasicElementOperation(driver=self.driver, el_type=el_type, label=label or comment,
                                     el_loc=target_loc, el_xpath=complete_xpath, comment=comment)
    
    def __webElement2(self, label=None, ignore_hidden=False, num=1, section=None):
        el_type = inspect.getframeinfo(inspect.currentframe().f_back)[2]
        section_obj = self.get_section(section=section, target=label or el_type, ignore_hidden=ignore_hidden)

        while True:
            el_xpath = self.get_el_type_xpath(el_type=el_type, label=label, num=num)
            target_xpath = "./descendant::%s" % el_xpath.replace("|", "|./descendant::")
            target_loc = section_obj['loc'].find_element_by_xpath(target_xpath)
            if ignore_hidden and not target_loc.is_displayed():
                num += 1
                continue
            break
        complete_xpath = target_xpath.replace("./descendant", f"{section_obj['xpath']}/descendant") if section_obj['xpath'] else None
        logger.info(f"[{el_type}: '{label}']ELEMENT XPATH: {complete_xpath}")
        return BasicElementOperation(driver=self.driver, el_type=el_type, label=label, el_loc=target_loc,
                                     el_xpath=complete_xpath)
    
    ########################
    # This Description is suitable for the 'inputbox','checkbox','radiobutton','select','textarea','icon'.
    ########################
    """
    Description: Locate the specified element in WEB UI.
    General Options:
        label:            The display name of element in the WEB UI.
        attr:               Using attribute to locate the element, this attribute can be used only in the 'icon' method. Acceptable value: The attribute of element. Defalut value: None
        ignore_hidden:      ignore the hidden text in the WEB UI or not. Acceptable value: True/False. Defalut value: False
        axes:               XPath Axes. 'axes' parameter accept following value. Defalut value: None
            ancestor:           Selects all ancestors (parent, grandparent, etc.) of the current node
            ancestor-or-self:   Selects all ancestors (parent, grandparent, etc.) of the current node and the current node itself
            attribute:          Selects all attributes of the current node
            child:              Selects all children of the current node
            descendant:         Selects all descendants (children, grandchildren, etc.) of the current node
            descendant-or-self: Selects all descendants (children, grandchildren, etc.) of the current node and the current node itself
            following:          Selects everything in the document after the closing tag of the current node
            following-sibling:  Selects all siblings after the current node
            namespace:          Selects all namespace nodes of the current node
            parent:             Selects the parent of the current node
            preceding:          Selects all nodes that appear before the current node in the document, except ancestors, attribute nodes and namespace nodes
            preceding-sibling:  Selects all siblings before the current node
            self:               Selects the current node
        num:                Specified a element if more than one element belong to a UI text. Acceptable value: int. Defalut value: 1
        section:            A locator which is used to narrow down the scope when the current page include more than one element with the same name.
                            Acceptable value: String/WebElement. Defalut value: None
    Return: BasicElementOperation instance.
    """
    def input(self, **kwargs):
        return self.__webElement(**kwargs)
  
    def checkbox(self, **kwargs):
        return self.__webElement(**kwargs)
    
    def radio_button(self, **kwargs):
        return self.__webElement(**kwargs)
        
    def select(self, **kwargs):
        return self.__webElement(**kwargs)
    
    def textarea(self, **kwargs):
        return self.__webElement(**kwargs)
    
    def upload_file(self, **kwargs):
        return self.__webElement(**kwargs)

    def icon(self, **kwargs):
        return self.__webElement(**kwargs)
    
    ########################
    # This Description is suitable for the 'link','button','text'.
    ########################
    """
    Description: Locate the specified element in WEB UI.
    General Options:
        label:        The display name of element in the WEB UI.
        ignore_hidden:  ignore the hidden text in the WEB UI or not. Acceptable value: True/False. Defalut value: False
        num:            Specified a element if more than one element belong to a UI text. Acceptable value: int. Defalut value: 1
        section:        A locator which is used to narrow down the scope when the current page include more than one element with the same name.
                        Acceptable value: String/WebElement. Defalut value: None
    Return: BasicElementOperation instance.
    """
    def link(self, **kwargs):
        return self.__webElement2(**kwargs)
        
    def button(self, **kwargs):
        return self.__webElement2(**kwargs)
    
    def text(self, **kwargs):
        return self.__webElement2(**kwargs)
        
    def element(self, el_type, **kwargs):
        """
        element_type:       Variable name in the resources/UIElements.conf, and the variable name should include the element type. example: "inputbox xxx"
        other parameters:   According to the 'element_type', the parameters are difference. See the description of element type for details.
        Return:             BasicElementOperation instance.
        """
        el_type = re.match(r'(\S+)', el_type).group(1)
        return getattr(self, el_type)(**kwargs)

    def is_existed(self, el_type, **kwargs):
        try:
            self.element(el_type=el_type, **kwargs)
            return True
        except Exception:
            return False


class BasicElementOperation(object):
    def __init__(self, driver, el_type, label=None, el_loc=None, el_xpath=None, comment=None):
        self.driver = driver
        self.type = el_type
        self.label = label or comment
        self.loc = el_loc
        self.xpath = ('xpath', el_xpath) if el_xpath else None
        
    @property
    def text(self):
        text = self.loc.text
        logger.info(f"{self.type}['{self.label}'] text: {text}")
        return text
        
    def is_displayed(self):
        status = self.loc.is_displayed()
        logger.info(f"{self.type}['{self.label}'] is displayed: {status}")
        return status
    
    def is_enabled(self):
        status = self.loc.is_enabled()
        logger.info(f"{self.type}['{self.label}'] is enabled: {status}")
        return status
    
    def click(self, interval=0):
        self.loc.click()
        logger.info(f"{self.type}['{self.label}'] is clicked, and wait {interval} seconds.")
        time.sleep(interval)
        
    def set(self, value=None):
        """
        Description: Set the value in the specified element. 
        Return: The value of the specified element.
        """
        logger.info(f"Set {self.type}['{self.label}'] as '{value}'.")
        if self.type == "input" or self.type == "textarea":
            self.loc.clear()
            self.loc.send_keys(value)
        elif self.type == "checkbox":
            if self.loc.is_selected() ^ value:
                self.loc.click()
        elif self.type == "radio_button":
            self.loc.click()
        elif self.type == "select":
            Select(self.loc).select_by_visible_text(value)
        elif self.type == "upload_file":
            self.loc.send_keys(value)
        else:
            pass

    @property
    def value(self):
        """
        Description: Get the current value of the specified element. 
        Return: The value of the specified element.
        """
        if self.type == "input" or self.type == "textarea":
            val = self.loc.get_attribute("value")
        elif self.type == "checkbox" or self.type == "radio_button":
            val = self.loc.is_selected()
        elif self.type == "select":
            val = Select(self.loc).first_selected_option.text.strip()
        else:
            return
        logger.info(f"{self.type}['{self.label}'] value: {val}")
        return val
        
    @property
    def options(self):
        """
        Description: Get all options of the specified element.
        Return: The all options of the specified element.
        """
        if self.type == "select":
            val = map(lambda x:  x.text, Select(self.loc).options)
            logger.info(f"{self.type}['{self.label}'] options: {val}")
            return val
        return

    def hover(self, interval=0):
        ActionChains(self.driver).move_to_element(self.loc).perform()
        logger.info(f"{self.type}['{self.label}'] The cursor is moved to '{self.label}'', and wait {interval} seconds.")
        time.sleep(interval)
