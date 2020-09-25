from table import Table
from selenium.webdriver.common.by import By
import time
from selenium.common import exceptions

class InputTable(Table):
    """
    Component: Input Table
    Input table has enable/disable, more-info views additionally to configuration table.
    """
    def __init__(self, browser, container, mapping={}):
        super(InputTable, self).__init__(browser, container, mapping)

        self.elements.update({
            "enable": {
                "by": By.CSS_SELECTOR,
                "select": "a.enable"
            },
            "disable": {
                "by": By.CSS_SELECTOR,
                "select": "a.disable"
            },
            "more_info": {
                "by": By.CSS_SELECTOR,
                "select": container["select"] + " td.expands"
            },
            "more_info_row": {
                "by": By.CSS_SELECTOR,
                "select": container["select"] + " tr.expanded + tr"
            },
            "more_info_key": {
                "by": By.CSS_SELECTOR,
                "select":  "dt"
            },
            "more_info_value": {
                "by": By.CSS_SELECTOR,
                "select":  "dd"
            }
        })

    def update_input(self, name, enable):
        status = "enable" if enable else "disable"
        negative_status = "disable" if enable else "enable"
        _row = self._get_row(name)
        _row.find_element(*self.elements["action"].values()).click()
        time.sleep(40)
        try:
            self.wait_for(status)
        except:
            try:
                self.get_element(negative_status)
            except:
                raise Exception("The input is already {}".format(status))
            else:
                raise Exception("Enable/Disable not found")
        self.get_element(status).click()
        for _ in range(15):
            try:
            # The element will be stale after it's status was changed. Therefore getting _row again
                _row = self._get_row(name)
                if status in self._get_column_value(_row, "disabled").lower():
                    return True
                time.sleep(2)
            except exceptions.StaleElementReferenceException:
                pass       
        else:
            raise Exception("The input was not enabled")

    def get_more_info(self, name, cancel=True):
        _row = self._get_row(name)
        _row.find_element(*self.elements["more_info"].values()).click()
        keys = self.more_info_row.find_elements(*self.elements["more_info_key"].values())
        values = self.more_info_row.find_elements(*self.elements["more_info_value"].values())        
        more_info = {key.text: value.text for key, value in zip(keys, values)}

        if cancel:
            _row = self._get_row(name)
            _row.find_element(*self.elements["more_info"].values()).click()

        return more_info
