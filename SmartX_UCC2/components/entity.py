from ..pages.page import Page
from selenium.webdriver.common.by import By
# from ..controls.textbox import TextBox
from abc import abstractmethod
from ..controls.button import Button
from ..controls.message import Message
import time

class Entity(object):
    """
    Entity form to add/edit the configuration.
    The instance of the class expects that the entity is already open.
    The instance of the class holds all the controls in the entity and provides the generic interaction that can be done with the entity
    """
    
    def __init__(self, browser, container, add_btn=None, wait_for=0):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param add_btn: The locator of add_button with which the entity will be opened
        """
        self.browser = browser
        
        # Controls
        self.save_btn = Button(browser, {"by": By.CSS_SELECTOR, "select": container["select"] + " input.submit-btn" })
        self.loading = Message(browser, {"by": By.CSS_SELECTOR,"select": container["select"] + " .msg-loading"})
        self.error_msg = Message(browser, {"by": By.CSS_SELECTOR,"select": container["select"] + " .msg-error"})
        self.add_btn = add_btn
        self.cancel_btn = Button(browser, {"by": By.CSS_SELECTOR, "select": container["select"] + " button.cancel-btn" })
        self.close_btn = Button(browser, {"by": By.CSS_SELECTOR, "select": container["select"] + " button.close" })
        
        self.wait_for = wait_for

    def get_error_msg(self):
        """
        Get the error message displayed while saving the configuration
        """
        return self.error_msg.wait_to_display()

    def save(self, expect_error=False):
        """
        Save the configuration
            :param expect_error: if True, the error message will be fetched. Otherwise, the function will return True if the configuration was saved properly
        """
        self.save_btn.click()
        if expect_error:
            return self.get_error_msg()
        else:
            self.loading.wait_loading()
            return True

    def cancel(self):
        """
        Cancel the entity 
        """
        self.cancel_btn.click()
        self.save_btn.wait_until("container")
        return True

    def close(self):
        """
        Close the entity 
        """
        self.close_btn.click()
        self.save_btn.wait_until("container")
        return True

    def open(self):
        """
        Open the entity by click on "New" button. 
        """
        self.add_btn.click()
        self.save_btn.wait_to_display()
        time.sleep(self.wait_for)
