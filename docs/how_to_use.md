# How to use

## Steps to test in Local Environment

**1. Install the framework**

The Framework could be cloned from here: [SmartX Repo](https://github.com/splunk/addon-factory-smartx-ui-test-library)

```console
1. git clone https://github.com/splunk/addon-factory-smartx-ui-test-library.git
2. python3 -m venv .venv
3. source .venv/bin/activate
4. cd addon-factory-smartx-ui-test-library
5. pip install .
```

**2. Download Browser Drivers**

Download the drivers for the browser you want to test

  - For Chrome: download chromedriver [ChromeDriver download](https://chromedriver.chromium.org/downloads)
  - For Firefox: download geckodriver [Geckodriver Download](https://github.com/mozilla/geckodriver/releases)
  - For IE: download IEdriverserver [IEdriverserver Download](https://www.selenium.dev/downloads/)

**2A. For Internet Explorer:**

For Internet Explorer, the following steps need to be performed for it to work correctly:
[IEDriver required configuration steps](https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver#required-configuration)

**3. Put the downloaded driver into test/ui/ directory**

Make sure that the drivers are in at least an area that could be found

**4. include the driver location in your PATH environment variable**

This needs to be done so that pytest can find the drivers.

**5. Execute the test cases**

You can execute the test cases with the following console command:

```console
pytest -vv --browser={browser} --local --persist-browser --splunk-host={web_url} --splunk-port={mgmt_url} --splunk-user {username} --splunk-password {password} --html {reportname.html} --setup-retry-count={retry-count} --headless --splunk-type=external
```

The parameters are as follows:

  - \--browser: The browser in which the test will run on. The supported values are: chrome, firefox, safari (Default: firefox)
  - \--local: The test will be run on the local browsers, used during development and testing phase (Default: False)
  - \--persist-browser: For local execution, keep a single browser to execute all tests. (Only supported with --local)
  - \--splunk-host: The Splunk web url
  - \--splunk-port: Splunk management port (Default: 8089)
  - \--splunk-user: Splunk instance username (Default: admin)
  - \--splunk-password: Splunk instance account password (Default: Chang3d!)
  - \--html: The output html file for debugging purposes
  - \--setup-retry-count: The number of times the browser should try to connect to the SeleniumBrowser (Default: 1)
  - \--headless: Run the test case on headless mode
  - \--splunk-type=external

## Steps to test in Saucelabs

Saucelabs is a cloud service that allows engineers/systems to provision any platform + browser combination to run some tests. The Saucelab app can be found (here)[https://app.saucelabs.com/dashboard/builds].

**1. Install the framework**

The Framework could be cloned from here: [SmartX Repo](https://github.com/splunk/addon-factory-smartx-ui-test-library)

**2. Configure Saucelabs credentials as environment variables**

  - SAUCE_USERNAME : &lt;saucelabs_username&gt;
  - SAUCE_PASSWORD : &lt;saucelabs_access_key&gt;

**3. Execute the test cases**

```console
pytest -vv --browser={browser} --splunk-host={web_url} --splunk-port={mgmt_url} --splunk-user {username} --splunk-password {password} --local
```

## General workflow for writing test cases using the Framework
1. Clone and install the framework inside test/ui
2. Create Add-on specific Page classes (we only need to specify which components it contains)
3. Implement the test-cases by using the pages & its components
