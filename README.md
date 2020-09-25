# SmartX

UCC based Add-on UI automation framework 

Confluence Page link: https://confluence.splunk.com/display/PROD/SmartX+UI+Automation+Framework+for+Ucc+based+Add-ons

## Table of contents

- [Goal](#goal)
- [Design](#design)
- [Features](#features)
- [Attributes & Methods of each class of the framework](#attributes--methods-of-each-class-of-the-framework)
    - [Class: BaseComponent](#class-basecomponent)
    - [Classes and methods used for Logging page](#classes-and-methods-used-for-logging-page)
    - [Class: SingleSelect (BaseComponent)](#class-singleselect-basecomponent)
    - [Class: Table (BaseComponent)](#class-table-basecomponent)
    - [Class: Textbox (BaseComponent)](#class-textbox-basecomponent)
    - [Class: Button (BaseComponent)](#class-button-basecomponent)
    - [Class: Message (BaseComponent)](#class-message-basecomponent)
    - [Class: Tabs (BaseComponent)](#class-tabs-basecomponent)
    - [Class: InputTable (Table)](#class-inputtable-table)
    - [Class: MultiSelect (BaseComponent)](#class-multiselect-basecomponent)
    - [Class: Entity](#class-entity)
    - [Class: BackendConf](#class-backendconf)
    - [Class: ListBackendConf (BackendConf)](#class-listbackendconf-backendconf)
    - [Class: SingleBackendConf-BackendConf](#class-singlebackendconf-backendconf)
- [Build test cases using the framework](#build-test-cases-using-the-framework)
- [Steps to test in Local environment](#steps-to-test-in-local-environment)
- [Steps to test with Saucelabs](#steps-to-test-with-saucelabs)
 
### Goal

To test all the UI configuration page of the Splunk add-ons. All the add-ons are built with the same template. The configuration pages consist of an Input page and a configuration page that has different tabs to configure logging, proxy settings and add product account in the add-ons. To support the testing of all the add-ons, a generic framework should be made, which can be used in the test cases for all the add-ons. The framework should have methods that can interact with UI components and test the working of UI.

### Design

For UI development, we follow a practice in which we create a set of components first. The component has its own state-cycle. The component will be enough reusable so that it can be placed on any page. A web-page will be a composition of these components placed in the proper container.

The testing framework will follow the same practice. It will have classes for all the components used in all the pages. These “Component” class will consist of methods to interact with the component, to get & set values in the component.  These components will be put on different pages. The structure is created so that it be easy to maintain and easy to understand. As per the design, the class “Page” should only be used to contain a set of components only. No interaction methods should be in the Page class.

    The structure of the framework can be divided into 3 parts.

    Components   : An UI component with which a user interacts with.
    Pages        : Holds multiple components of a specific page
    Test cases   : Tests the interaction & values in the components

### Features

- pytest fixture to control when the browser should be initialized & tear-downed.
- Flag to easily convert the environment from SauceLabs to local for debugging purposes.
- Screenshot when any test case fails.
- An Html report containing the trace-back and the screenshots of the failed test cases.
- Pytest parameters to change the URL, credentials of the test page.
- Backend configuration can be fetched from the management API of the Splunk instance.
- Reruns, the test cases will be rerunning to avoid some rare timeout/network issues

### Attributes & Methods of each class of the framework
### Class: BaseComponent

| Method             | Description                             | Parameters                                                                                                                                                                                                                                                                                              | Return                |
|--------------------|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| \_init\_          | Initializes the BaseComponent class     | driver, css_selector<br/>browser - The selenium webdriver<br/>container-                                                                                                                                                                                                                                | -                     |
| get_element        | To get a single element                 | key<br/>key: "by" and "Select" keys of elements dictionary                                                                                                                                                                                                                                              | element               |
| get_elements       | To get more than one element            | key<br/>key: "by" and "Select" keys of elements dictionary                                                                                                                                                                                                                                              | elements              |
| get_child_element  | To get a single child element           | key<br/>key: "by" and "Select" keys of elements dictionary                                                                                                                                                                                                                                              | element               |
| get_child_elements | To get more than one child element      | key<br/>key: "by" and "Select" keys of elements dictionary                                                                                                                                                                                                                                              | elements              |
| get_tuple          | Gets the tuple from the set of elements | key<br/>key: "by" and "Select" keys of elements dictionary                                                                                                                                                                                                                                              | a tuple of an element |
| wait_for           | Waits for an element to be located      | key, event="presence", msg=None<br/>key: "by" and "Select" keys of elements dictionary<br/>event="presence": Will wait till the presence of the element<br/>event="clickable": Will wait till the the element is clickable<br/>msg=None: The message to be printed in case of timeout (Default is None) | -                     |
| wait_until         | Waits for an element to be invisible    | element, mgs=None<br/>element: Gets the element value<br/>msg: None                                                                                                                                                                                                                                     | -                     |

### Classes and methods used for Logging page

| Method                | Description                                     | Parameters                                                                                        | Return                   |
|-----------------------|-------------------------------------------------|---------------------------------------------------------------------------------------------------|--------------------------|
| \_init\_             | Initializes the logging class                   | browser, url<br/>browser: Initializes the browser object<br/>url: Gets the url of Splunk Instance | -                        |
| _go_to_logging        | Navigates to the logging page                   | -                                                                                                 | -                        |
| get_list_of_loglevels | Gets the list of log level values               | -                                                                                                 | List of log level values |
| get_loglevel          | Gets the value of the current log level         | -                                                                                                 | Current log level value  |
| update_loglevel       | Updates the log_level to the provided log level | level: Instance to the log level                                                                  |

### Class: SingleSelect (BaseComponent)

| Method          | Description                                                               | Parameters                                                                                                                              | Return                                |
|-----------------|---------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| \_init\_       | Initializes the single select class                                       | browser, container<br/>browser: Initializes the browser Instance<br/>container: Instance of the container which holds the single select | -                                     |
| select          | Selects a value from the dropdown                                         | value<br/>value: Instance of the selected value from the dropdown after each iteration                                                  | True/False                            |
| search          | Search for a keyword from dropdown                                        | query<br/>query : string query to search                                                                                                | -                                     |
| search_get_list | Search for a keyword from dropdown and return the list of filtered values | query<br/>query : string query to search                                                                                                | list of filtered values<br/>list(str) |
| get_value       | Gets the current value of the single select                               | -                                                                                                                                       | Current value of dropdown             |
| list_of_values  | Gets the list of values from the dropdown                                 | -                                                                                                                                       | Each value of dropdown                |

### Class: Table (BaseComponent)

| Method            | Description                                            | Parameters                                                                                                                                  | Return                                                                   |
|-------------------|--------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| \_init\_         | Initializes the Table class                            | browser, container<br/>browser: Initializes the browser instance<br/>container: Instance of the container which holds the table             | -                                                                        |
| get_count_title   | Gets the count title of the table                      | -                                                                                                                                           | Count text                                                               |
| get_row_count     | Gets the length of the table rows                      | -                                                                                                                                           | the count of the length of table rows                                    |
| get_headers       | Gets the value of each header of the table             | -                                                                                                                                           | each header of the table                                                 |
| get_sort_order    | Gets the sorting order of the values of a table header | -                                                                                                                                           | True/False                                                               |
| sort_column       | Sorts the column in ascending and descending order     | column, ascending=True<br/>column : The header of the column which should be sorted<br/>ascending : True = ascending, False = descending    | -                                                                        |
| get_table         | Gets the table as dictionary                           | -                                                                                                                                           | table (dictionary)<br/>{ "row_name": {<br/> "col_header": value,<br/>} , |
| get_cell_value    | Gets the specific cell value                           | name, column<br/>name: Instance of the Name column<br/>column: Name of the column                                                           | Value of the current row and Name column i.e value of the specified cell |
| get_column_values | Gets list of values for the specified column           | column<br/>column: Title of the column                                                                                                      | List of str-values for the specified column                              |
| edit_row          | Edits the specified row                                | name<br/>name: Instance of the Name column                                                                                                  | -                                                                        |
| clone_row         | Clones the current row                                 | name<br/>name: Instance of the Name column                                                                                                  | -                                                                        |
| delete_row        | Deletes the current row                                | name, cancel=False<br/>name: Instance of the Name column<br/>cancel: True = The cancel button will be clicked & the row will not be deleted | -                                                                        |
| set_filter        | Sets the filter value in the table                     | filter_query<br/>filter_query : query as a string                                                                                           | -                                                                        |
| clean_filter      | Cleans the filer                                       | -                                                                                                                                           | -                                                                        |

### Class: Textbox (BaseComponent)

| Methods   | Description                   | Parameters                                                                                                                                                                                                                                    | Return               |
|-----------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| \_init\_ | Initializes the textbox class | browser, container, encrypted=False<br/>browser: Instance of the browser<br/>container: Instance of the container that holds the textbox<br/>Encrypted=True: For encrypted textbox value<br/>Encrypted=False: For non-encrypted textbox value | -                    |
| set_value | Sets value to the textbox     | value<br/>value: Instance of the value attribute of textbox                                                                                                                                                                                   | -                    |
| get_value | Get the value of the textbox  | -                                                                                                                                                                                                                                             | Value of the textbox |

### Class: Button (BaseComponent)

| Methods         | Description                                            | Parameters                                                                                                              | Return |
|-----------------|--------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|--------|
| \_init\_       | Initializes the button class                           | browser, container<br/>browser: Instance of the browser<br/>container: Instance of the container that holds the textbox | -      |
| click           | To click on the container                              | -                                                                                                                       | -      |
| __getattr__     | Gets the button element through "by" and "select" keys | key<br/>key: "by" and "Select" keys of elements dictionary                                                              | -      |
| wait_to_display | Wait to display the container                          | -                                                                                                                       | -      |
### Class: Message (BaseComponent)

| Methods        | Description                                              | Parameters                                                                                                              | Return  |
|----------------|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|---------|
| \_init\_      | Initializes the message class                            | browser, container<br/>browser: Instance of the browser<br/>container: Instance of the container that holds the message | -       |
| wait_loading   | Checks that the message should appear and then disappear | -                                                                                                                       | Text    |
| wait_to_appear | Waits for the message to appear                          | -                                                                                                                       | Message |
### Class: Tabs (BaseComponent)

| Methods  | Description                                      | Parameters                                                                                                          | Return |
|----------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|--------|
| \_init\_| Initializes the tab class                        | browser, container<br/>browser: Instance of the browser<br/>container: Instance of the container that holds the tab | -      |
| open_tab | Gets the element of the tab that is to be opened | tab<br/>tab: Instance of the tab elememt                                                                            | -      |

### Class: InputTable (Table)

| Methods       | Description                                   | Parameters                                                                                                                  | Return            |
|---------------|-----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------|
| \_init\_     | Initializes the InputTable class              | browser, container<br/>browser: Instance of the browser<br/>container: Instance of the container that holds the Input Table |                   |
| update_input  | Changes the input status to enable or disable | name, enable<br/>name: Name column of the table<br/>enable: Instance of the Enable element of Action field                  | Status            |
| get_more_info | Expands an Input to display the configuration | name, cancel<br/>name: Name column of the table<br/>cancel: Closes the expanded input                                       | Input information |

### Class: MultiSelect (BaseComponent)

| Methods         | Description                                                 | Parameters                                                                                                                  | Return                  |
|-----------------|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------|
| \_init\_       | Initializes the multiselect class                           | browser, container<br/>browser: Instance of the browser<br/>container: Instance of the container that holds the Input Table |                         |
| search          | Adds text to multiselect field                              | value<br/>value: Instance of the multiselect values                                                                         | -                       |
| search_get_list | Searches for a value and gets the list                      | value<br/>value: Instance of the multiselect values                                                                         | List of searched values |
| select          | Selects each value from the list                            | value<br/>value: Instance of the multiselect values                                                                         | TRUE                    |
| deselect        | Deselects the selected value                                | value<br/>value: Instance of the multiselect values                                                                         | True/False              |
| get_values      | Returns the selected values                                 | -                                                                                                                           | Selected values         |
| list_of_values  | Returns the list of possible values to select from dropdown |

### Class: Entity

- Entity form to add/edit the configuration.
- The instance of the class expects that the entity is already open.
- The instance of the class holds all the controls in the entity and provides the generic interaction that can be done with the entity

| Methods           | Description                                           | Parameters                                                                               | Return                                                                                                    |
|-------------------|-------------------------------------------------------|------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| open              | Opens the configuration page by click on "New" button | -                                                                                        | -                                                                                                         |
| save              | saves the configuration                               | expect_error : True= If we are expecting an error message while saving the configuration | expect_error=True : returns True if saved successfully<br/>expect_error-False : returns the error message |
| cancel            | Closes the pop-up by clicking on cancel button        | -                                                                                        | -                                                                                                         |
| close             | Closes the pop-up by clicking on close button         | -                                                                                        | -                                                                                                         |
| get_error_message | Get the error message while saving the configuration  | -                                                                                        | Error message as string                                                                                   |

### Class: BackendConf

- Base Class to fetch configuration values from the rest endpoints.

| Methods    | Description                                           | Parameters                   | Return                                                                          |
|------------|-------------------------------------------------------|------------------------------|---------------------------------------------------------------------------------|
| rest_call  | make a GET request to the specified endpoint          | url : url to fetch data from | json response                                                                   |
| parse_conf | Parse the json response to a configuration dictionary | json_res : the json response | dictionary containing the configuration<br/>{ stanza : {parameter: value} ... } |

### Class: ListBackendConf (BackendConf)

- For the configurations which can have a list of stanzas. For example, Account.

| Methods          | Description                                  | Parameters                                                                        | Return                                                                                           |
|------------------|----------------------------------------------|-----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| get_all_stanzas  | get list of all stanzas as dictionary        | -                                                                                 | dictionary containing the list of stanzas<br/>{ stanza : {parameter: value } ... }               |
| get_stanza       | get dictionary for a specific stanza only    | stanza : stanza name                                                              | dictionary containing only the specified stanza<br/>{ specified_stanza: {parameter: value} ... } |
| get_stanza_value | get a specific value from a specified stanza | stanza : stanza name<br/>param : param name of which the value should be returned | parameter value                                                                                  |

### Class: SingleBackendConf-BackendConf

- For the configurations can only have one stanza. For example, logging.

| Methods       | Description                          | Parameters                 | Return                                                                                 |
|---------------|--------------------------------------|----------------------------|----------------------------------------------------------------------------------------|
| get_stanza    | get the configuration for the stanza | -                          | dictionary containing only one stanza<br/>{ specified_stanza: {parameter: value} ... } |
| get_parameter | get a specific value from the stanza | param : the parameter name | parameter value                                                                        |

### Build test cases using the framework

1. Copy/Clone the framework inside the test/ui
2. Create Add-on specific Page classes (we only need to specify which components it contains, demo: server_page)
3. Implement the test-cases by using the pages & its components
4. Jenkins integrations

Demo link : https://git.splunk.com/projects/SOLN/repos/ta-microsoft-scom/browse/test/ui

### Steps to test in Local environment

1. Install Python requirements
2. pip install -r requirements.txt
3. Download Browser's specific driver
    For Chrome: download chromedriver
    For Firefox: download geckodriver
    For IE: download IEdriverserver
4. Put the downloaded driver into test/ui/ directory
5. For Internet explorer, The steps mentioned at below link must be performed:
https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver#required-configuration
6. Execute the test cases:
 ```script
  pytest -vv --browser={browser} --web_url={web_url} --mgmt_url={mgmt_url} --username admin --password {password} --html {reportname.html} --local
 ```
### Steps to test with Saucelabs

1. Install Python requirements
2. pip install -r requirements.txt
3. Configure saucelabs credentials as environment variables
    SAUCE_USERNAME : <saucelabs_username>
    SAUCE_PASSWORD : <saucelabs_access_key>
4. Execute the test cases
```script
pytest -vv --browser={browser} --web_url={web_url} --mgmt_url={mgmt_url} --username admin --password {password} --html {reportname.html}
```
