To set up the environment, you should do the following:

**1. Create a Virtual environment and Install the SmartX framework**

Generally, you would want to install the SmartX framework as part of a Virtual Environment so that you can keep your environment clean and organized:

```console
1. python3 -m venv .venv
2. source .venv/bin/activate
```

```bash
pip install pytest-splunk-addon-ui-smartx
```

**2. Setup the tests directory for SmartX within the App**

The tests should be structured in the following format, if the folders do not exist you should create them so that the common template for CICD tests works correctly:

  - `test/ui`: The parent ui-test directory in which we should put all of our SmartX test cases.
  - `test/ui/<TA>_UccLib`: This is where we should put the specific TA's unique page files that we want to test with here. By default page, proxy, login, and logging are already implemented, if you want to create another page class file, you would add it here.
  - `test/ui/test_splunk_<ta_name>_<test_suite>.py`: The test cases for a specific TA page or Input.
  - `test/ui/pytest-ci.ini`: This file is used with CI/CD pipelines to set up the test environment and add pytest options for the tests.

```conf
[pytest]
norecursedirs = .git .venv venv build deps tests/deps node_modules package
addopts = -v -s --tb=long
    --splunk-type=external
    --junitxml=/home/circleci/work/test-results/test.xml
    --html=report.html
    --splunk-web-scheme=https
    --splunk-host=splunk 
    --splunkweb-port=8000 
    --splunk-port=8089 
    --splunk-password=Chang3d!
filterwarnings =
    ignore::DeprecationWarning
markers =
	logging: Logging Page UI test cases
	account: Account page UI test cases
	proxy: proxy page UI test cases
    input: Input page UI test cases
	forwarder: Tests to be run on Forwarder/Standalone
	liveenvironment: Tests need live server to successfully execute
	oauth_account: Oauth Account UI test cases
	sanity_test: For sanity check of addons
```
