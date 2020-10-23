from ...components.base_component import BaseComponent, Selector


class ActionDropdown(BaseComponent):

    def __init__(self, browser, container, mapping=dict()):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        super(ActionDropdown, self).__init__(browser, container)
        self.elements.update({
            "add_action": Selector(select=container.select + " .dropdown-toggle.btn"),
            "action_name": Selector(select=".unselected-action span:first-of-type"), 
        })

    def _get_action_title(self, action_obj):
        action_obj.find_element(*self.elements)


    def get_value_list(self):
        self.add_action.click()
        value_list = []
        for each_action in self.get_elements("action_name"):
            value_list.append(self.get_clear_text(each_action))
        self.add_action.click()
        return value_list


    def select_action(self, action_name):
        self.add_action.click()
        for each_action in self.get_elements("action_name"):
            if  action_name == self.get_clear_text(each_action):
                each_action.click()
                break
        else:
            raise ValueError("{} not found in Alert Action list".format(action_name))