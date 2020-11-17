Getting Started
================
If you want to create new set of UI tests for a Splunk App using SmartX, you can follow the following steps here:

Setup
======
To set up the environment, you should do the following:

**1. Create a Virtual environment and Install the SmartX framework**

Generally, you would want to install the SmartX framework as part of a Virtual Environment so that you can keep your environment clean and organized:

.. code-block:: console

    1. python3 -m venv .venv
    2. source .venv/bin/activate

There are two ways to install SmartX:

1) The Framework could be cloned from GitHub: `SmartX Repo <https://github.com/splunk/addon-factory-smartx-ui-test-library>`__ 

.. code-block:: console
    
    1. git clone https://github.com/splunk/addon-factory-smartx-ui-test-library.git
    4. cd addon-factory-smartx-ui-test-library
    5. poetry install

2) Download SmartX from PyPi: `SmartX PyPI <https://pypi.org/project/pytest-splunk-addon-ui-smartx/>`__

.. code-block:: console
    
    pip install pytest-splunk-addon-ui-smartx

**2. Setup the tests directory for SmartX within the App**

The tests should be structured in the following format, if the folders do not exist you should create them so that the common template for CICD tests works correctly:
    * test/ui: The parent ui-test directory in which we should put all of our SmartX test cases.
    * test/ui/<TA>_UccLib: This is where we should put the specific TA's unique page files that we want to test with here. By default page, proxy, login, and logging are already implemented, if you want to create another page class file, you would add it here.
    * test/ui/test_splunk_<ta_name>_<test_suite>.py: The test cases for a specific TA page or Input.
    * test/ui/pytest-ci.ini: This file is used with CICD (Jenkins/CircleCI) to set up the test environment and add pytest options for the tests.

.. dropdown:: Example pytest-ci.ini

    .. literalinclude:: ./example_code.py
        :language: console
        :lines: 174-


Test Page Creation
===================
When creating new UI tests for a Splunk App using SmartX, it would be helpful to start with creating the TA's page class files within test/ui/<TA>_UccLib. 

These files should contain Page classes that represent the webpage we want to test within the app, and hold the multiple components that are within that webpage. The class hould also contain the webdriver instance and the backend methods to make API calls to Splunk.

When creating a Page file, there are usually 2 portions of it to create: 

**1. The page class**
This would be the main class for the page file, which should hold all of the components and class instances for calling the backend. 
This file would also need to import all of the components as well from SmartX to be able to use them.
The usual parameters for this class are the following: 

    * ucc_smartx_selenium_helper (SmartX fixture): The SmartX instance for the selenium webdriver which helps control page interactions for the tests. This parameter is used to create the UI components, and we should not create the UI component classes without this parameter. 
    * ucc_smartx_rest_helper (SmartX fixture): The SmartX instance for the selenium helper which helps control page interactions. This parameter holds the selenium driver, urls(web, mgmt) and session key for the tests. This parameter is used for creating SmartX rest classes such as the classes found within backend_confs.py.
    * open_page(Flag): This parameter is to indicate whether or not we should open this webpage when we create this class instance. If we want to open the file later, we can use <class>.open() later on. 

This class should also hold functions to open the webpage and to store the backend endpoint. 

**2. The entities found within the page**
If the webpage consists of any entities (A web element on a page that consists of multiple components, such as popups or forms to create a new input). then you would need to create an entity that represents the entity's controls and components.
The usual parameters for this class are the following:

    * browser: The selenium webdriver
    * container: The container in which the entity is located in

The parent class for this type of class is found within the pytest_splunk_addon_ui_smartx/components/entity.py file. This base class has useful functions to click on a save button in the entity, closing the entity, and getting messages that may appear. 
This base class has the following parameters: 

    * browser: The selenium webdriver
    * container: Container in which the entity is located.
    * add_btn: The locator of add_button with which the entity will be opened

**Example**
A Example Page file would look like this: 

.. dropdown:: Example Page File
    
    .. literalinclude:: ./example_code.py
        :language: python3
        :lines: 1-94

Test Cases Creation
===================

**Creating tests**

These files contain the test suites for the webpages that we want to test. A test generally consists of creating an instance of the webpage class we created above and calling on component functions to manipulate and assert the status of an element on the webpage. The test cases also calls the two SmartX fixtures that creates the Selenium Driver classes that we need for our tests. It is also recommended to add docstrings to each test so that it can be easily identifiable of what each test is trying to accomplish. 
The test cases utilize a class function assert_util to conveniently test a plethora of different assertions in a unified way. It is recommended to use this function to keep the code simple and readable. This function has the following parameters:

    * left: The parameter you want to compare/assert with, generally this would be the status of the webelement. This parameter is required.
    * right: The parameter you want to compare/assert with to the left parameter. Generally this would be the state that you want the webelement to be in. This parameter is required.
    * operator: This will be the operator in which you want the left to be compared with the right. The options are as follows: ["==", "!=", "<", "<=", ">", ">=", "in", "not in", "is", "is not"]. This parameter's default: "=="
    * left_args: If the left parameter is a function, then you can provide that function with the arguments found here. This parameter's default: {}
    * right_args: If the right parameter is a function, then you can provide that function with the arguments found here. This parameter's default: {}
    * msg: If you want a custom error message to appear if this assertion fails, then you can add that here, otherwise the default message is as follows: "Condition Failed. \nLeft-value: {}\nOperator: {}\nRight-value: {}".format(args['left_value'], args["operator"], args['right_value'])

For the test cases, you may also want to include informative markers as well so that selectively testing the Addon's UI tests could be easy. Some of the common UI markers we used were:

    * <test_suite>: Test Page UI test cases (IE input)
    * forwarder: Tests to be run on Forwarder/Standalone
    * liveenvironment: Tests need live server to successfully execute
    * oauth_account: Oauth Account UI test cases
    * sanity_test: For sanity check of addons

.. dropdown:: An example of a test case

    .. literalinclude:: ./example_code.py
        :language: python3
        :lines: 96-101, 121-139

**Setup Fixtures**
The test suite could also contain setup fixtures that would be called before tests to setup the Splunk environment. This could range from creating new inputs, to using a different page class to create a related input/Account for the page being tested. It may also be useful to have global variables for the default configurations so that it could be easily edited and reused later.
An example of a setup fixture: 

.. dropdown:: Example setup Fixture

    .. literalinclude:: ./example_code.py
        :language: python3
        :lines: 141-163

**Teardown Fixtures**
The test suites should also contain teardown fixtures to revert the Splunk instance back to its original state after each test, this way each test is independent of each other and so if one test fails, then another test shouldn't fail in correspondence as to the first test.
An example of the teardown fixture: 

.. dropdown:: Example teardown Fixture

    .. literalinclude:: ./example_code.py
        :language: python3
        :lines: 104-119

**Environment Variables**
You may also want to get environment variables so that you can dynamically setup different test variables easily through the environment instead of having to hardcode them into the test. This may useful in hiding sensitive data such as login credentials.
An example for getting environment variables is as follows:

.. dropdown:: Example Environment Variables Fixture

    .. literalinclude:: ./example_code.py
        :language: python3
        :lines: 165-172