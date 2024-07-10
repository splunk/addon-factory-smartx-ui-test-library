# v5.0.0

The `get_placeholder_value` method has been removed in this version. The value present in placeholder will no longer be accessible starting SmartX v5.0.0.
To ensure smooth upgrade of the SmartX from v4.x to v5.0 in your environment, ensure that your add-on doesn't use `placeholder` property defined in your add-on's globalConfig file.
The `placeholder` property for an entity of an input has been deprecated as of September 2023 and has been removed as of UCC framework v5.48.0. You can use `help` property instead. Refer [this documentation](https://splunk.github.io/addonfactory-ucc-generator/entity/) of UCC framework for more details.

Refer the [deprecation notice](https://github.com/splunk/addonfactory-ucc-generator/issues/831) for more details.

