
from .base_control import BaseControl
from ..base_component import Selector

class TextBox(BaseControl):
    """
    Entity-Component: TextBox
    """

    def __init__(self, browser, container, encrypted=False):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """
        super(TextBox, self).__init__(browser, container)
        self.encrypted = encrypted
        self.elements.update({
            "input": Selector(select=container.select + " input")
        })

    def set_value(self, value):
        """
        set value of the textbox
        """

        self.input.clear()
        self.input.send_keys(value)

    def get_value(self):
        """
        get value from the textbox
        """
        return self.input.get_attribute('value').strip()

    def is_editable(self):
        '''
        Returns True if the Textbox is editable, False otherwise
        '''
        return not bool(self.input.get_attribute("readonly") or self.input.get_attribute("readOnly") or self.input.get_attribute("disabled"))


    def clear_text(self):
        '''
        Clears the textbox value
        '''
        self.input.clear()

    def get_type(self):
        '''
        Get type of value entered in textbox
        '''
        return self.input.get_attribute('type').strip()