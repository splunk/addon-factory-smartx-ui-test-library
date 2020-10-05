from __future__ import print_function
from builtins import str
from builtins import range
import json

def get_orca_deployment_urls():
    """
    Fetch the web_url and management_url from the orca_deployment.json file to execute the testcases.
    reason: In windows containers "so1" hostname does not work directly. 
    """
    try:
        with open("orca_deployment.json", "r") as f:
            data = f.read()
        json_data = json.loads(data)

    except Exception as e:
        print(str(e))
        
    web_url = json_data['server_roles']['standalone'][0]['splunk']['web_url']
    mgmt_url = json_data['server_roles']['standalone'][0]['splunk']['management_url']
    return {"web":web_url,"mgmt":mgmt_url}

# Decorator with argument
def backend_retry(retry_count):
    # The decorator itself
    def backend_retry_decorator(method):
        # Inner method in the decorator
        def retry_method(*args, **kwargs):
            last_exc = Exception()

            # Try 3 times
            for _ in range(retry_count):
                try:
                    return method(*args, **kwargs)
                except Exception as e:
                    last_exc = e
            else:
                if last_exc:
                    raise(last_exc)
        return retry_method
    return backend_retry_decorator

def verify_dict_equal(actual=dict(), expected=dict(), ignore_fields=list()):
        """
        :param: actual dict
        :param: expected dict
        :param ignore_fields dict, ignore_fields in actual will be ignored
        Example:
        actual = {"1": [a,b,c], "2": "hello","3" : {"4": "value"} }
        expected = {"2": "hello","3" : {"4": "value"} }
        ignore_fields = ["1"]
        return True
        """
        if ignore_fields:
            for field in ignore_fields:
                if field in actual:
                    del actual[field]
                if field in expected:
                    del expected[field]

        if sorted(actual.keys()) != sorted(expected.keys()):
            return False
        elif sorted(actual.keys()) == sorted(expected.keys()):
            for key in actual.keys():
                if type(actual[key]) != type(expected[key]):
                    return False
                elif type(actual[key]) == type(expected[key]) == list:
                    if sorted(actual[key]) != sorted(expected[key]):
                        return False
                elif (type(actual[key]) == type(expected[key]) == int) \
                        or (type(actual[key]) == type(expected[key]) == str) \
                        or (type(actual[key]) == type(expected[key]) == unicode):
                    if actual[key] != expected[key]:
                        return False
                elif type(actual[key]) == type(expected[key]) == dict:
                    verify_dict_equal(actual[key], expected[key])
        return True