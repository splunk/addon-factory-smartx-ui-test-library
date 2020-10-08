from ..base_component import BaseComponent
from .base_control import BaseControl
from selenium.webdriver.common.by import By

class Button(BaseControl):
    """
    Entity_Component : Button
    """
    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in. 
        """
        super(Button, self).__init__(browser, container)

    def click(self):
        """
        Click on the button
        """
        self.container.click()

    
