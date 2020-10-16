# SPDX-FileCopyrightText: 2020 Splunk Inc.
#
# SPDX-License-Identifier: Apache-2.0

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
