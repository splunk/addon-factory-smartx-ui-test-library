from selenium.webdriver.support import select
from selenium.common.exceptions import UnexpectedTagNameException


class SplunkSelect(select.Select):
    def __init__(self, webelement):
        if not webelement.tag_name.lower() in ("select", "splunk-select"):
            raise UnexpectedTagNameException(
                "Select only works on <select> and <splunk-select> elements, "
                "not on <%s>" % webelement.tag_name
            )
        self._el = webelement
        multi = self._el.get_attribute("multiple")
        self.is_multiple = multi and multi != "false"
