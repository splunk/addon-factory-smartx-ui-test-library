from ..components.base_component import BaseComponent
from selenium.webdriver.common.by import By

class Message(BaseComponent):
    """
    Entity-Component: Message
    """
    def __init__(self, browser, container):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """
        super(Message, self).__init__(browser, container)        

    def wait_loading(self):
        """
        Wait till the message appears and then dissapears
        """
        try:
            text = self.container.text
            self.wait_until("container")
            return text
        except:
            pass

    def wait_to_display(self):
        """
        Wait till the message appears
        """
        return self.container.text
        
