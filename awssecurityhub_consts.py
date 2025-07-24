# File: awssecurityhub_consts.py
#
# Copyright (c) 2019-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
AWSSECURITYHUB_EQUALS_CONSTS = "EQUALS"
AWSSECURITYHUB_MAX_PER_PAGE_LIMIT = 100
AWSSECURITYHUB_SQS_MESSAGE_LIMIT = 10

AWSSECURITYHUB_REGION_DICT = {
    "US East (Ohio)": "us-east-2",
    "US East (N. Virginia)": "us-east-1",
    "US West (N. California)": "us-west-1",
    "US West (Oregon)": "us-west-2",
    "Africa (Cape Town)": "af-south-1",
    "Asia Pacific (Hong Kong)": "ap-east-1",
    "Asia Pacific (Hyderabad)": "ap-south-2",
    "Asia Pacific (Jakarta)": "ap-southeast-3",
    "Asia Pacific (Mumbai)": "ap-south-1",
    "Asia Pacific (Osaka)": "ap-northeast-3",
    "Asia Pacific (Seoul)": "ap-northeast-2",
    "Asia Pacific (Singapore)": "ap-southeast-1",
    "Asia Pacific (Sydney)": "ap-southeast-2",
    "Asia Pacific (Tokyo)": "ap-northeast-1",
    "China (Ningxia)": "cn-northwest-1",
    "China (Beijing)": "cn-north-1",
    "Canada (Central)": "ca-central-1",
    "Europe (Frankfurt)": "eu-central-1",
    "Europe (Ireland)": "eu-west-1",
    "Europe (London)": "eu-west-2",
    "Europe (Milan)": "eu-south-1",
    "Europe (Paris)": "eu-west-3",
    "Europe (Spain)": "eu-south-2",
    "Europe (Stockholm)": "eu-north-1",
    "Europe (Zurich)": "eu-central-2",
    "Middle East (Bahrain)": "me-south-1",
    "Middle East (UAE)": "me-central-1",
    "South America (Sao Paulo)": "sa-east-1",
    "AWS GovCloud (US-East)": "us-gov-east-1",
    "AWS GovCloud (US-West)": "us-gov-west-1",
}

AWSSECURITYHUB_FINDING_CEF_TYPES = {
    "Id": ["aws security hub findings id", "aws arn"],
    "ProductArn": ["aws arn"],
    "GeneratorId": ["aws arn"],
    "ProductFields.aws/securityhub/FindingId": ["aws arn"],
    "ProductFields.action/networkConnectionAction/localPortDetails/port": ["port"],
    "ProductFields.action/networkConnectionAction/remotePortDetails/port": ["port"],
    "ProductFields.action/networkConnectionAction/remoteIpDetails/ipAddressV4": ["ip"],
}

AWSSECURITYHUB_RESOURCE_CEF_TYPES = {"Id": ["aws arn"], "InstanceId": ["aws ec2 instance id"], "Details.AwsEc2Instance.IpV4Addresses": ["ip"]}

AWSSECURITYHUB_ERROR_TEST_CONNECTIVITY = "Test Connectivity Failed"
AWSSECURITYHUB_SUCC_TEST_CONNECTIVITY = "Test Connectivity Passed"
AWSSECURITYHUB_ERROR_REGION_INVALID = "Specified region is not valid"
AWSSECURITYHUB_ERROR_BOTO3_CLIENT_NOT_CREATED = "Could not create boto3 client: {error}"
AWSSECURITYHUB_ERROR_INVALID_METHOD = "Invalid method: {method}"
AWSSECURITYHUB_ERROR_BOTO3_CALL_FAILED = "Boto3 call to Security Hub failed: {error}"
AWSSECURITYHUB_ERROR_ALL_RESOURCE_IP_VALIDATION = "Resource ec2 IP validation failed for all the provided IPs"
AWSSECURITYHUB_ERROR_ALL_NETWORK_IP_VALIDATION = "Network source IP validation failed validation failed for all the provided IPs"
AWSSECURITYHUB_ERROR_FINDING_ID_IN_RECORD_STATE = "Provided findings ID is already in {record_state}"
AWSSECURITYHUB_ERROR_INVALID_FINDING_ID = "Please provide a valid findings ID"
AWSSECURITYHUB_SUCC_ADD_NOTE = "Note added successfully to the provided findings ID"
AWSSECURITYHUB_BAD_ASSET_CONFIG_ERROR_MESSAGE = "Please provide access keys or select assume role check box in asset configuration"

# constants relating to 'get_error_message_from_exception'
AWSSECURITYHUB_ERROR_MESSAGE_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters."
AWSSECURITYHUB_ERROR_CODE_UNAVAILABLE = "Error code unavailable"
AWSSECURITYHUB_PARSE_ERROR_MESSAGE = "Unable to parse the error message. Please check the asset configuration and|or action parameters"

# constants relating to 'validate_integer'
AWSSECURITYHUB_VALID_INT_MESSAGE = "Please provide a valid integer value in the {param}"
AWSSECURITYHUB_NON_NEG_NON_ZERO_INT_MESSAGE = "Please provide a valid non-zero positive integer value in {param}"
AWSSECURITYHUB_NON_NEG_INT_MESSAGE = "Please provide a valid non-negative integer value in the {param}"
AWSSECURITYHUB_LIMIT_KEY = "'limit' action parameter"
AWSSECURITYHUB_POLL_NOW_DAYS_KEY = "'poll_now_days' configuration parameter"
AWSSECURITYHUB_SCHEDULED_POLL_DAYS_KEY = "'scheduled_poll_days' configuration parameter"

AWSSECURITYHUB_DEFAULT_REQUEST_TIMEOUT = 30  # in seconds

# constants relating to 'initialize'
AWSSECURITYHUB_STATE_FILE_CORRUPT_ERROR = (
    "Error occurred while loading the state file due to its unexpected format. "
    "Resetting the state file with the default format. Please try again."
)
