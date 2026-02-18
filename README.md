# AWS Security Hub

Publisher: Splunk <br>
Connector Version: 2.4.3 <br>
Product Vendor: AWS <br>
Product Name: Security Hub <br>
Minimum Product Version: 5.5.0

This app integrates with AWS Security Hub to ingest findings

**Functioning of On Poll**

- There are two approaches for ingesting data using the On Poll action.

- **SQS Polling**

  SQS polling is the preferred ingestion technique due to limitations in the AWS SecurityHub API
  used to ingest findings. Detailed instructions on configuring SQS-polling can be found below.

- **Normal Polling**

  1. On Poll

     This is manual On Poll. Here, the findings data of the past N days (poll_now_days
     configuration parameter) will be ingested.

  1. Scheduled Polling

     In the first run, the findings data of the past M days (Scheduled_poll_days configuration
     parameter) will be ingested and then, for the consecutive runs, only the findings are
     updated after the last run's time (last_ingested_date stored in the state file) will be
     fetched.

  1. Interval Polling

     The logic of fetching and ingesting the findings is the same as scheduled polling.

## Ingesting Security Hub Findings from SQS

The following section explains how to configure the preferred means of ingesting findings from AWS,
SQS polling. These instructions leverage a CloudFormation template to set up the forwarding of
Security Hub findings into an SQS queue. Splunk SOAR in turn ingests the findings from this queue.

Note that SQS-based polling will ignore the **poll_now_days** and **scheduled_poll_days** asset
configuration parameters.

### 1 - Forward Security Hub Alerts to an SQS Queue

Start by navigating to the CloudFormation page on your AWS console and running CloudFormation
template linked below. The template will generate a new CloudWatch Event Rule which will forward all
new Security Hub findings to an SQS Queue.

CloudFormation Template:
<https://splunkphantom.s3.amazonaws.com/cloud-formation/phantom-sechub-to-sqs.yaml>

![Cloud Formation - Selecting the Splunk SOAR
Template](https://splunkphantom.s3.amazonaws.com/images/PhantomSecHubToSQSCloudFormation.png)

For detailed steps refer to the following documentation:\
<https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html>

After the Cloud Formation stack has been created be sure to take note of the
*securityHubToPhantomSQSURL* field in the output - you will need it later.

![Cloud Formation
Output](https://splunkphantom.s3.amazonaws.com/images/PhantomCloudFormationOutputHighlighted.png)

### 2 - Configure your Splunk SOAR App Asset

Next, login to your Splunk SOAR instance. If you are new to Splunk SOAR you can easily launch the
Splunk SOAR Community Edition available in the AWS Marketplace.

Navigate to the "Apps" page in Splunk SOAR. Search for the Security Hub app - if you don't find it
in your search results, you may need to select the *New Apps* and install the app before proceeding.
Select "Configure New Asset" for the v1.1+ Security Hub App.

> **Important** These instructions require the Splunk SOAR Security Hub app v1.1 or higher - if you
> are running an older version, be sure to upgrade it by selecting "Upgrade Apps" in your Splunk
> SOAR instance or downloading the latest version of the app from
> [Splunkbase](https://splunkbase.splunk.com/apps) and manually installing it.

![Security Hub Splunk SOAR App
Configure](https://splunkphantom.s3.amazonaws.com/images/security-hub-app-asset.png)

### App Configuration Parameters

Setting up the Security Hub Splunk SOAR app requires input on 3 configuration tabs.

##### Asset Info

Provide a unique name asset name. It is a good idea to use a name that reminds you which AWS
environment the app connects to.

##### Ingest Settings

- Select a Label to apply to all Findings consumed from security hub, or create a new one by
  typing in the drop-down box
- Select "Interval" to enable periodic polling of the SQS Queue
- Modify the polling interval as desired to suit your organization's needs.

##### Asset Settings

Supply values for the following fields:

- AWS Access Key - The access key associated with an IAM account
- AWS Secret Key - The secret key associated with an IAM account
- SQS URL - The URL provided by the Cloud Formation template from part 1 of this guide

![Security Hub Splunk SOAR App - Asset Settings
Tab](https://splunkphantom.s3.amazonaws.com/images/phantom-sechub-app-assetsettings.png)

### Finalize the Configuration

Once you have configured the Asset Info, Ingest Settings, and Asset Settings select *Save* to
finalize your app configuration. You are now ready to start consuming Security Hub Findings in
Splunk SOAR!

Any new Security Hub Findings will now appear on your Splunk SOAR "Events" page according to your
polling interval. Note that the integration relies on forwarding events from the Security Hub to the
SQS queue, so the app will only know about any findings that were created after the Cloud Formation
template was run in Step 1.

______________________________________________________________________

### Configuration variables

This table lists the configuration variables required to operate AWS Security Hub. These variables are specified when configuring a Security Hub asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access_key** | optional | password | AWS Access Key |
**secret_key** | optional | password | AWS Secret Key |
**region** | required | string | AWS Region |
**sqs_url** | optional | string | SQS URL |
**poll_now_days** | required | numeric | Poll last 'n' days for POLL NOW |
**scheduled_poll_days** | required | numeric | Poll last 'n' days for scheduled polling |
**use_role** | optional | boolean | Use attached role when running Splunk SOAR in EC2 |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration <br>
[on poll](#action-on-poll) - Ingest findings from Security Hub <br>
[get findings](#action-get-findings) - Lists and describes Security Hub aggregated findings that are specified by a single filter attribute <br>
[get related findings](#action-get-related-findings) - Lists Security Hub aggregated findings that are specified by filter attributes <br>
[archive findings](#action-archive-findings) - Archive the AWS Security Hub aggregated findings specified by the filter attributes <br>
[unarchive findings](#action-unarchive-findings) - Unarchive the AWS Security Hub aggregated findings specified by the filter attributes <br>
[add note](#action-add-note) - Add Note to the AWS Security Hub aggregated findings specified by the filter attributes

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'on poll'

Ingest findings from Security Hub

Type: **ingest** <br>
Read only: **True**

This app supports two possible methods for ingesting findings:<ul><li>Directly from Security Hub - To use this method, leave the <b>sqs_url</b> asset configuration field blank.</li><li>Via an SQS Queue - To use this method, add the URL of an SQS queue to the <b>sqs_url</b> asset configuration field. This method will ignore the <b>poll_now_days</b> and <b>scheduled_poll_days</b> asset configuration parameters. Messages will be deleted from the queue after being received.</li></ul>

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container_id** | optional | Container IDs to limit the ingestion to | string | |
**start_time** | optional | Start of the time range, in epoch time (milliseconds) | numeric | |
**end_time** | optional | End of the time range, in epoch time (milliseconds) | numeric | |
**container_count** | optional | Maximum number of container records to query for | numeric | |
**artifact_count** | optional | Maximum number of artifact records to query for | numeric | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

No Output

## action: 'get findings'

Lists and describes Security Hub aggregated findings that are specified by a single filter attribute

Type: **investigate** <br>
Read only: **True**

If none of the filter parameters are provided, all the findings will be fetched controlled by the limit parameter. For the parameters 'resource_ec2_ipv4_addresses' and 'network_source_ipv4', if the user provides comma-separated values and one or more values are incorrect, then those values will be simply ignored and only correct values will be used for further filtering of the findings.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**resource_id** | optional | The canonical identifier for the given resource type | string | `aws security hub resource id` `aws arn` |
**resource_ec2_ipv4_addresses** | optional | Comma-separated IPv4 addresses associated with the instance | string | `aws security hub resource ip` |
**network_source_ipv4** | optional | Comma-separated source IPv4 addresses of network-related information about a finding | string | `aws security hub network source ip` |
**network_source_mac** | optional | The source media access control (MAC) address of network-related information about a finding | string | `mac address` |
**resource_region** | optional | The canonical AWS external region name where this resource is located | string | `aws security hub resource region` |
**limit** | optional | Maximum number of findings to be fetched | numeric | |
**is_archived** | optional | Flag to fetch the archived findings | boolean | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.parameter.is_archived | boolean | | False True |
action_result.parameter.limit | numeric | | 150 |
action_result.parameter.network_source_ipv4 | string | `aws security hub network source ip` | 172.40.20.1 |
action_result.parameter.network_source_mac | string | `mac address` | 00:00:5e:00:53:af |
action_result.parameter.resource_ec2_ipv4_addresses | string | `aws security hub resource ip` | 12.123.1.1 |
action_result.parameter.resource_id | string | `aws security hub resource id` `aws arn` | AWS::IAM::AccessKey:ABCDEFGH123456789 arn:aws:ec2:us-east-1:123456789012:instance/i-abcdefgh1234567 |
action_result.parameter.resource_region | string | `aws security hub resource region` | us-east-1 |
action_result.data.\*.AwsAccountId | string | | ABCDEFGH123456789 |
action_result.data.\*.CompanyName | string | | AWS |
action_result.data.\*.Compliance.AssociatedStandards.\*.StandardsId | string | | standards/aws-foundational-security-best-practices/v/1.0.0 |
action_result.data.\*.Compliance.SecurityControlId | string | | DynamoDB.2 |
action_result.data.\*.Compliance.Status | string | | WARNING |
action_result.data.\*.Compliance.StatusReasons.\*.Description | string | | Unable to describe the supporting AWS Config Rule, Please verify that you have enabled AWS Config. |
action_result.data.\*.Compliance.StatusReasons.\*.ReasonCode | string | | CONFIG_ACCESS_DENIED |
action_result.data.\*.Confidence | numeric | | 5 |
action_result.data.\*.CreatedAt | string | | 2019-04-10T11:58:12.766Z |
action_result.data.\*.Description | string | | EC2 instance has an unprotected port which is being probed by a known malicious host |
action_result.data.\*.FindingProviderFields.Severity.Label | string | | MEDIUM |
action_result.data.\*.FindingProviderFields.Severity.Original | string | | MEDIUM |
action_result.data.\*.FirstObservedAt | string | | 2019-04-10T11:48:10Z |
action_result.data.\*.GeneratorId | string | | arn:aws:guardduty:us-east-1:123456789012:detector/abcd1234abcd1234abcd1234 |
action_result.data.\*.Id | string | `aws security hub findings id` | arn:aws:guardduty:us-east-1:1234567890:detector/abcd1234abcd1234abcd1234/finding/abcd1234abcd1234abcd1234 |
action_result.data.\*.LastObservedAt | string | | 2019-04-11T22:24:14Z |
action_result.data.\*.Network.DestinationDomain | string | `domain` | |
action_result.data.\*.Network.DestinationIpV4 | string | `ip` | |
action_result.data.\*.Network.DestinationIpV6 | string | `ip` | |
action_result.data.\*.Network.DestinationPort | string | `port` | |
action_result.data.\*.Network.Direction | string | | IN OUT |
action_result.data.\*.Network.Protocol | string | | |
action_result.data.\*.Network.SourceDomain | string | `domain` | |
action_result.data.\*.Network.SourceIpV4 | string | `aws security hub network source ip` `ip` | |
action_result.data.\*.Network.SourceIpV6 | string | `ip` | |
action_result.data.\*.Network.SourceMac | string | `mac address` | |
action_result.data.\*.Network.SourcePort | string | `port` | |
action_result.data.\*.NextToken | string | | Long base64 encoded string |
action_result.data.\*.Note.Text | string | | (test - 2019-06-20 09:41:25) test overwrite false (test - 2019-06-20 09:40:46) true |
action_result.data.\*.Note.UpdatedAt | string | | 2019-04-12T10:06:44.134Z |
action_result.data.\*.Note.UpdatedBy | string | | automation-test |
action_result.data.\*.ProductArn | string | | arn:aws:securityhub:us-east-1::product/aws/guardduty |
action_result.data.\*.ProductFields.RecommendationUrl | string | | https://docs.aws.amazon.com/console/securityhub/standards-cis-2.9/remediation |
action_result.data.\*.ProductFields.RelatedAWSResources:0/name | string | | securityhub-vpc-flow-logs-enabled-e8258e90 |
action_result.data.\*.ProductFields.RelatedAWSResources:0/type | string | | AWS::Config::ConfigRule |
action_result.data.\*.ProductFields.Resources:0/Id | string | | arn:aws:dynamodb:us-east-1:157568067690:table/doNotDeleteTable |
action_result.data.\*.ProductFields.RuleId | string | | 2.9 |
action_result.data.\*.ProductFields.StandardsControlArn | string | | arn:aws:securityhub:us-east-1:157568067690:control/cis-aws-foundations-benchmark/v/1.2.0/2.9 |
action_result.data.\*.ProductFields.StandardsGuideArn | string | | arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0 |
action_result.data.\*.ProductFields.StandardsGuideSubscriptionArn | string | | arn:aws:securityhub:us-east-1:157568067690:subscription/cis-aws-foundations-benchmark/v/1.2.0 |
action_result.data.\*.ProductFields.action/actionType | string | | PORT_PROBE |
action_result.data.\*.ProductFields.action/awsApiCallAction/api | string | | DescribeAlarms |
action_result.data.\*.ProductFields.action/awsApiCallAction/callerType | string | | remote IP |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/city/cityName | string | | cityName |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/country/countryName | string | | CountryName |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/geoLocation/isp | string | | Test |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/geoLocation/lat | string | | 37.000 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/geoLocation/lon | string | | 37.000 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/ipAddressV4 | string | `ip` | 123.123.1.1 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/organization/asn | string | | 123456 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/organization/asnOrg | string | | Test Inc. |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/organization/org | string | | Test |
action_result.data.\*.ProductFields.action/awsApiCallAction/serviceName | string | | monitoring.amazonaws.com |
action_result.data.\*.ProductFields.action/networkConnectionAction/blocked | string | | false |
action_result.data.\*.ProductFields.action/networkConnectionAction/connectionDirection | string | | INBOUND |
action_result.data.\*.ProductFields.action/networkConnectionAction/localPortDetails/port | string | | 11 |
action_result.data.\*.ProductFields.action/networkConnectionAction/localPortDetails/portName | string | | SSH |
action_result.data.\*.ProductFields.action/networkConnectionAction/protocol | string | | TCP |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/city/cityName | string | | cityName |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/country/countryName | string | | countryName |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/geoLocation/lat | string | | 37.0000 |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/geoLocation/lon | string | | 37.0000 |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/ipAddressV4 | string | `ip` | 12.12.123.123 |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/organization/asn | string | | 1234 |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/organization/asnOrg | string | | test |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/organization/isp | string | | test |
action_result.data.\*.ProductFields.action/networkConnectionAction/remoteIpDetails/organization/org | string | | test |
action_result.data.\*.ProductFields.action/networkConnectionAction/remotePortDetails/port | string | | 12345 |
action_result.data.\*.ProductFields.action/networkConnectionAction/remotePortDetails/portName | string | | Unknown |
action_result.data.\*.ProductFields.action/portProbeAction/blocked | string | | false |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/localPortDetails/port | string | | 11 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/localPortDetails/portName | string | | SSH |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/city/cityName | string | | cityName |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/country/countryName | string | | countryName |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/geoLocation/lat | string | | 9 3333.943392 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/geoLocation/lon | string | | -80 1318.243958 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/ipAddressV4 | string | `ip` | 123.12.1.1 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/asn | string | | 12345 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/asnOrg | string | | Test B.v. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/isp | string | | Test S.A. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/org | string | | Test S.A. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/localPortDetails/port | string | | 11 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/localPortDetails/portName | string | | SSH |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/city/cityName | string | | cityName |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/country/countryName | string | | countryName |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/geoLocation/lat | string | | 9 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/geoLocation/lon | string | | -80 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/ipAddressV4 | string | `ip` | 123.12.1.1 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/organization/asn | string | | 12345 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/organization/asnOrg | string | | Test B.v. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/organization/isp | string | | Test S.A. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:1/remoteIpDetails/organization/org | string | | Test S.A. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/localPortDetails/port | string | | 11 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/localPortDetails/portName | string | | SSH |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/city/cityName | string | | cityname |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/country/countryName | string | | countryName |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/geoLocation/lat | string | | 9 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/geoLocation/lon | string | | -80 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/ipAddressV4 | string | `ip` | 123.12.1.1 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/organization/asn | string | | 12345 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/organization/asnOrg | string | | Test B.v. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/organization/isp | string | | Test S.A. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:2/remoteIpDetails/organization/org | string | | Test S.A. |
action_result.data.\*.ProductFields.additionalInfo | string | | {"threatName":"Scanner","threatListName":"ThreatListName"} |
action_result.data.\*.ProductFields.archived | string | | false |
action_result.data.\*.ProductFields.attributes/ACL | string | | acl-b68b09d0 |
action_result.data.\*.ProductFields.attributes/ENI | string | | eni-0e16d09e9d9720222 |
action_result.data.\*.ProductFields.attributes/IGW | string | | igw-35109f52 |
action_result.data.\*.ProductFields.attributes/INSTANCE_ID | string | | i-0af916767974b7daf |
action_result.data.\*.ProductFields.attributes/PORT | string | | 80 |
action_result.data.\*.ProductFields.attributes/PORT_GROUP_NAME | string | | HTTP |
action_result.data.\*.ProductFields.attributes/PROTOCOL | string | | TCP |
action_result.data.\*.ProductFields.attributes/REACHABILITY_TYPE | string | | Internet |
action_result.data.\*.ProductFields.attributes/RULE_TYPE | string | | RecognizedPortNoAgent |
action_result.data.\*.ProductFields.attributes/SECURITY_GROUP | string | | sg-082e3689120474d29 |
action_result.data.\*.ProductFields.attributes/TCP_PORTS | string | | \[[22 - 22], [80 - 80], [443 - 443], [8000 - 8000], [9999 - 9999]\] |
action_result.data.\*.ProductFields.attributes/UDP_PORTS | string | | [] |
action_result.data.\*.ProductFields.attributes/VPC | string | | vpc-b962a3df |
action_result.data.\*.ProductFields.attributes:0/key | string | | UDP_PORTS |
action_result.data.\*.ProductFields.attributes:0/value | string | | [] |
action_result.data.\*.ProductFields.attributes:1/key | string | | ENI |
action_result.data.\*.ProductFields.attributes:1/value | string | | eni-12345abcdfe123 |
action_result.data.\*.ProductFields.attributes:10/key | string | | INSTANCE_ID |
action_result.data.\*.ProductFields.attributes:10/value | string | | i-12345abcdfe123 |
action_result.data.\*.ProductFields.attributes:2/key | string | | RULE_TYPE |
action_result.data.\*.ProductFields.attributes:2/value | string | | NetworkExposure |
action_result.data.\*.ProductFields.attributes:3/key | string | | PROTOCOL |
action_result.data.\*.ProductFields.attributes:3/value | string | | TCP |
action_result.data.\*.ProductFields.attributes:4/key | string | | IGW |
action_result.data.\*.ProductFields.attributes:4/value | string | | igw-12345abcdfe123 |
action_result.data.\*.ProductFields.attributes:5/key | string | | VPC |
action_result.data.\*.ProductFields.attributes:5/value | string | | vpc-12345abcdf |
action_result.data.\*.ProductFields.attributes:6/key | string | | SECURITY_GROUP |
action_result.data.\*.ProductFields.attributes:6/value | string | | sg-12345abcdfe123 |
action_result.data.\*.ProductFields.attributes:7/key | string | | REACHABILITY_TYPE |
action_result.data.\*.ProductFields.attributes:7/value | string | | Internet |
action_result.data.\*.ProductFields.attributes:8/key | string | | ACL |
action_result.data.\*.ProductFields.attributes:8/value | string | | acl-12345abcdfe123 |
action_result.data.\*.ProductFields.attributes:9/key | string | | TCP_PORTS |
action_result.data.\*.ProductFields.attributes:9/value | string | | \[[22 - 22]\] |
action_result.data.\*.ProductFields.aws/guardduty/service/action/actionType | string | | AWS_API_CALL |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/affectedResources | string | | |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS::CloudTrail::Trail | string | | GeneratedFindingCloudTrailName |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS::EC2::Instance | string | | i-99999999 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS::IAM::Role | string | | GeneratedFindingIAMRole |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS::IAM::User | string | | GeneratedFindingIAMUser |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS::S3::Bucket | string | | ssm-app |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/api | string | | DescribeNetworkInterfaces |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/callerType | string | | |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/errorCode | string | | NoSuchEntityException |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/city | string | | |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/city/cityName | string | | Ashburn |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/country/countryName | string | | United States |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/geoLocation/lat | string | | 40.0481 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/geoLocation/lon | string | | -77.4728 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/ipAddressV4 | string | | 3.238.239.205 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/asn | string | | 14618 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/asnOrg | string | | AMAZON-AES |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/isp | string | | Amazon.com |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/org | string | | Amazon.com |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/serviceName | string | | ec2.amazonaws.com |
action_result.data.\*.ProductFields.aws/guardduty/service/action/dnsRequestAction/blocked | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/action/dnsRequestAction/domain | string | | GeneratedFindingDomainName |
action_result.data.\*.ProductFields.aws/guardduty/service/action/dnsRequestAction/protocol | string | | UDP |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/blocked | string | | false |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/connectionDirection | string | | INBOUND |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/localIpDetails/ipAddressV4 | string | | 172.31.48.171 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/localPortDetails/port | string | | 22 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/localPortDetails/portName | string | | SSH |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/protocol | string | | TCP |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/city/cityName | string | | Montreal |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/country/countryName | string | | Canada |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/geoLocation/lat | string | | 45.5072 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/geoLocation/lon | string | | -73.6498 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/ipAddressV4 | string | | 24.200.121.125 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/asn | string | | 5769 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/asnOrg | string | | VIDEOTRON |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/isp | string | | Videotron Ltee |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/org | string | | Videotron Ltee |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remotePortDetails/port | string | | 40455 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/networkConnectionAction/remotePortDetails/portName | string | | Unknown |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/blocked | string | | false |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/localIpDetails/ipAddressV4 | string | | 10.0.0.23 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/localPortDetails/port | string | | 9999 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/localPortDetails/portName | string | | Unknown |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/city/cityName | string | | St Petersburg |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/country/countryName | string | | Russia |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/geoLocation/lat | string | | 59.909 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/geoLocation/lon | string | | 30.295 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/ipAddressV4 | string | | 45.155.205.225 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/organization/asn | string | | 49505 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/organization/asnOrg | string | | OOO Network of data-centers Selectel |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/organization/isp | string | | 3NT Solutions LLP |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.0\_/remoteIpDetails/organization/org | string | | 3NT Solutions LLP |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/localIpDetails/ipAddressV4 | string | | 10.0.0.23 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/localPortDetails/port | string | | 443 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/localPortDetails/portName | string | | HTTPS |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/city/cityName | string | | GeneratedFindingCityName2 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/country/countryName | string | | GeneratedFindingCountryName2 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/geoLocation/lat | string | | 0 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/geoLocation/lon | string | | 0 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/ipAddressV4 | string | | 198.51.100.1 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/organization/asn | string | | 29073 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/organization/asnOrg | string | | GeneratedFindingASNOrg2 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/organization/isp | string | | GeneratedFindingISP2 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/portProbeAction/portProbeDetails.1\_/remoteIpDetails/organization/org | string | | GeneratedFindingORG2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo | string | | |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/additionalScannedPorts | string | | [] |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.0\_/count | string | | 18 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.0\_/firstSeen | string | | 1512692639 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.0\_/lastSeen | string | | 1512692839 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.0\_/name | string | | GeneratedFindingAPIName1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.1\_/count | string | | 8 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.1\_/firstSeen | string | | 1512692639 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.1\_/lastSeen | string | | 1512692837 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.1\_/name | string | | GeneratedFindingAPIName1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.2\_/count | string | | 2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.2\_/firstSeen | string | | 1512692637 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.2\_/lastSeen | string | | 1512692637 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/apiCalls.2\_/name | string | | GeneratedFindingAPIName1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/domain | string | | GeneratedFindingThreatListName |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/inBytes | string | | 321987 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/localPort | string | | 34875 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/allowUsersToChangePassword | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/hardExpiry | string | | false |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/maxPasswordAge | string | | 150 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/minimumPasswordLength | string | | 6 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/passwordReusePrevention | string | | 2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/requireLowercaseCharacters | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/requireNumbers | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/requireSymbols | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/newPolicy/requireUppercaseCharacters | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/allowUsersToChangePassword | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/hardExpiry | string | | false |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/maxPasswordAge | string | | 180 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/minimumPasswordLength | string | | 6 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/passwordReusePrevention | string | | 2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/requireLowercaseCharacters | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/requireNumbers | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/requireSymbols | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/oldPolicy/requireUppercaseCharacters | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/outBytes | string | | 6841 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/policyArn | string | | arn:aws:iam::aws:policy/AdministratorAccess |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/portsScannedSample.0\_ | string | | 855 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/portsScannedSample.10\_ | string | | 400 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/portsScannedSample.11\_ | string | | 813 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentApiCalls.0\_/api | string | | GeneratedFindingAPIName1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentApiCalls.0\_/count | string | | 2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentApiCalls.1\_/api | string | | GeneratedFindingAPIName2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentApiCalls.1\_/count | string | | 2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.0\_/accessKeyId | string | | GeneratedFindingAccessKeyId1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.0\_/ipAddressV4 | string | | 198.51.100.1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.0\_/principalId | string | | GeneratedFindingPrincipalId1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.1\_/accessKeyId | string | | GeneratedFindingAccessKeyId2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.1\_/ipAddressV4 | string | | 198.51.100.1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.1\_/principalId | string | | GeneratedFindingPrincipalId2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.2\_/accessKeyId | string | | GeneratedFindingAccessKeyId3 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.2\_/ipAddressV4 | string | | 198.51.100.1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.2\_/principalId | string | | GeneratedFindingPrincipalId3 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.3\_/accessKeyId | string | | GeneratedFindingAccessKeyId4 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.3\_/ipAddressV4 | string | | 198.51.100.1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/recentCredentials.3\_/principalId | string | | GeneratedFindingPrincipalId4 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/sample | string | | true |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/scannedPort | string | | 80 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/threatListName | string | | ProofPoint |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/threatName | string | | Scanner |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusual | string | | 25 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusual/countries.0\_ | string | | GeneratedFindingUnusualCountryName1 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusual/countries.1\_ | string | | GeneratedFindingUnusualCountryName2 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusual/countries.2\_ | string | | GeneratedFindingUnusualCountryName3 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusual/hoursOfDay.0\_ | string | | 1513609200000 |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusual/isps | string | | amazon.com |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusual/userNames.0\_ | string | | GeneratedFindingUserName |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/unusualProtocol | string | | UDP |
action_result.data.\*.ProductFields.aws/guardduty/service/archived | string | | false |
action_result.data.\*.ProductFields.aws/guardduty/service/count | string | | 108675 |
action_result.data.\*.ProductFields.aws/guardduty/service/detectorId | string | | c8b6836865362e2b73f679f650bdsaddds |
action_result.data.\*.ProductFields.aws/guardduty/service/eventFirstSeen | string | | 2019-09-06T13:43:03Z |
action_result.data.\*.ProductFields.aws/guardduty/service/eventLastSeen | string | | 2021-03-10T23:53:31Z |
action_result.data.\*.ProductFields.aws/guardduty/service/evidence | string | | |
action_result.data.\*.ProductFields.aws/guardduty/service/evidence/threatIntelligenceDetails.0\_/threatListName | string | | ProofPoint |
action_result.data.\*.ProductFields.aws/guardduty/service/evidence/threatIntelligenceDetails.0\_/threatNames | string | | [] |
action_result.data.\*.ProductFields.aws/guardduty/service/evidence/threatIntelligenceDetails.0\_/threatNames.0\_ | string | | Scanner |
action_result.data.\*.ProductFields.aws/guardduty/service/resourceRole | string | | TARGET |
action_result.data.\*.ProductFields.aws/guardduty/service/serviceName | string | | guardduty |
action_result.data.\*.ProductFields.aws/guardduty/service/userFeedback | string | | USEFUL |
action_result.data.\*.ProductFields.aws/inspector/RulesPackageName | string | | Network Reachability |
action_result.data.\*.ProductFields.aws/inspector/arn | string | | arn:aws:inspector:us-east-1:157568067690:target/0-6eg3IiCE/template/0-xAf9XX8I/run/0-VVOWh3IP/finding/0-2pwnXhww |
action_result.data.\*.ProductFields.aws/inspector/id | string | | Recognized port reachable from internet |
action_result.data.\*.ProductFields.aws/securityhub/CompanyName | string | | test |
action_result.data.\*.ProductFields.aws/securityhub/FindingId | string | `aws arn` | arn:aws:securityhub:us-east-1::product/aws/guardduty/arn:aws:guardduty:us-east-1:123456789012:detector/1234567abcdefghijkl12345abcde/finding/1234567abcdefghijkl12345abcde |
action_result.data.\*.ProductFields.aws/securityhub/ProductName | string | | GuardDuty |
action_result.data.\*.ProductFields.aws/securityhub/SeverityLabel | string | | MEDIUM |
action_result.data.\*.ProductFields.aws/securityhub/annotation | string | | Unable to describe the supporting AWS Config Rule, Please verify that you have enabled AWS Config. |
action_result.data.\*.ProductFields.count | string | | 159 |
action_result.data.\*.ProductFields.detectorId | string | `md5` | 1234567abcdefghijkl12345abcde |
action_result.data.\*.ProductFields.dlpRisk:0/count | string | | 1 |
action_result.data.\*.ProductFields.dlpRisk:0/risk | string | | 6 |
action_result.data.\*.ProductFields.owner:0/count | string | | 1 |
action_result.data.\*.ProductFields.owner:0/name | string | | test.user |
action_result.data.\*.ProductFields.resourceRole | string | | TARGET |
action_result.data.\*.ProductFields.rule-arn | string | | arn:aws:macie:us-east-1:123456789012:trigger/1234567abcdefghijkl12 |
action_result.data.\*.ProductFields.serviceAttributes/assessmentRunArn | string | | arn:aws:inspector:us-east-1:123456789012:target/0-XXXXX/template/0-XXXXX/run/0-XXXXX |
action_result.data.\*.ProductFields.serviceAttributes/rulesPackageArn | string | | arn:aws:inspector:us-east-1:123456789012:rulespackage/1234567abcdefghijkl12 |
action_result.data.\*.ProductFields.serviceAttributes/schemaVersion | string | | 1 |
action_result.data.\*.ProductFields.tags:0 | string | | OPEN_PERMISSIONS |
action_result.data.\*.ProductFields.tags:1 | string | | BASIC_ALERT |
action_result.data.\*.ProductFields.themes:0/count | string | | 1 |
action_result.data.\*.ProductFields.themes:0/theme | string | | encryption_key |
action_result.data.\*.ProductName | string | | Security Hub |
action_result.data.\*.RecordState | string | | ARCHIVED ACTIVE |
action_result.data.\*.Region | string | | us-east-1 |
action_result.data.\*.Remediation.Recommendation.Text | string | | v2 Release |
action_result.data.\*.Remediation.Recommendation.Url | string | | https://docs.aws.amazon.com/console/securityhub/standards-cis-2.9/remediation |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.IamInstanceProfileArn | string | | arn:aws:iam::157568067690:instance-profile/AmazonSSMRoleForInstancesQuickSetup |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.ImageId | string | | ami-1234567abcdef |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.IpV4Addresses | string | `aws security hub resource ip` `ip` | 123.12.1.1 |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.LaunchedAt | string | | 2019-04-10T10:47:11.000Z |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.SubnetId | string | | subnet-1234567abcde |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.Type | string | | t2.micro |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.VpcId | string | | vpc-12345ABCDE |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.PrincipalId | string | | 157568067690 |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.PrincipalName | string | | Root |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.PrincipalType | string | | Root |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.UserName | string | | Root |
action_result.data.\*.Resources.\*.Details.AwsS3Bucket.CreatedAt | string | | 2021-03-01T13:39:44Z |
action_result.data.\*.Resources.\*.Details.AwsS3Bucket.OwnerId | string | | 042b1aa6d5faa5cfe9d016645ce14be41235ed6f94c988c6af6550f439e3f444 |
action_result.data.\*.Resources.\*.Details.AwsS3Bucket.ServerSideEncryptionConfiguration.Rules.\*.ApplyServerSideEncryptionByDefault.KMSMasterKeyID | string | | arn:aws:kms:region:123456789012:key/key-id |
action_result.data.\*.Resources.\*.Details.AwsS3Bucket.ServerSideEncryptionConfiguration.Rules.\*.ApplyServerSideEncryptionByDefault.SSEAlgorithm | string | | SSEAlgorithm |
action_result.data.\*.Resources.\*.Id | string | `aws security hub resource id` | arn:aws:ec2:us-east-1:123456789012:instance/i-1234567abcdefgh |
action_result.data.\*.Resources.\*.InstanceId | string | `aws ec2 instance id` | i-1234567abcdefghi |
action_result.data.\*.Resources.\*.Partition | string | | test |
action_result.data.\*.Resources.\*.Region | string | `aws security hub resource region` | us-east-1 |
action_result.data.\*.Resources.\*.Tags.APP | string | | SSM_AUTOMATION |
action_result.data.\*.Resources.\*.Tags.ASG | string | | ASG_VALUE |
action_result.data.\*.Resources.\*.Tags.App | string | | AWS-EC2 |
action_result.data.\*.Resources.\*.Tags.Description | string | | used for testing MC + splunk connect |
action_result.data.\*.Resources.\*.Tags.GeneratedFindingInstaceTag1 | string | | GeneratedFindingInstaceValue1 |
action_result.data.\*.Resources.\*.Tags.GeneratedFindingInstaceTag2 | string | | GeneratedFindingInstaceTagValue2 |
action_result.data.\*.Resources.\*.Tags.JIRA | string | | PINF-000 |
action_result.data.\*.Resources.\*.Tags.Name | string | | test Enterprise Redux |
action_result.data.\*.Resources.\*.Tags.Project | string | | Splunk |
action_result.data.\*.Resources.\*.Tags.Ticket | string | | PINF-000 |
action_result.data.\*.Resources.\*.Tags.aws:autoscaling:groupName | string | | test-group |
action_result.data.\*.Resources.\*.Tags.aws:cloudformation:logical-id | string | | MinemeldInstance |
action_result.data.\*.Resources.\*.Tags.aws:cloudformation:stack-id | string | | arn:aws:cloudformation:us-east-1:123456789012:stack/minemeld/1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.Resources.\*.Tags.aws:cloudformation:stack-name | string | | minemeld |
action_result.data.\*.Resources.\*.Tags.btest | string | | |
action_result.data.\*.Resources.\*.Tags.foo | string | | bar |
action_result.data.\*.Resources.\*.Tags.name | string | | PINF-000 |
action_result.data.\*.Resources.\*.Tags.new-key | string | | new-value |
action_result.data.\*.Resources.\*.Tags.owner | string | | abc@test.com |
action_result.data.\*.Resources.\*.Tags.purpose | string | | github-opensource-apps-testing |
action_result.data.\*.Resources.\*.Tags.userid | string | | testId |
action_result.data.\*.Resources.\*.Type | string | | AwsEc2Instance |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.RequestId | string | | 1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.data.\*.SchemaVersion | string | | 2018-10-08 |
action_result.data.\*.Severity.Label | string | | MEDIUM |
action_result.data.\*.Severity.Normalized | numeric | | 40 |
action_result.data.\*.Severity.Original | string | | MEDIUM |
action_result.data.\*.Severity.Product | numeric | | 2 |
action_result.data.\*.SourceUrl | string | | https://us-east-1.console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?macros=current&fId=02b6836ac80ffa143f61fec798de288d |
action_result.data.\*.Title | string | | Unprotected port on EC2 instance i-123456abcdefhgf is being probed |
action_result.data.\*.Types | string | | TTPs/Initial Access/UnauthorizedAccess:EC2-SSHBruteForce |
action_result.data.\*.UpdatedAt | string | | 2019-04-11T22:35:03.677Z |
action_result.data.\*.Workflow.Status | string | | NEW |
action_result.data.\*.WorkflowState | string | | NEW |
action_result.summary.total_findings | numeric | | 2 |
action_result.summary.total_groups | numeric | | 2 |
action_result.message | string | | Total findings: 2 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get related findings'

Lists Security Hub aggregated findings that are specified by filter attributes

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings_id** | required | Identifier of security finding | string | `aws security hub findings id` `aws arn` |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.parameter.findings_id | string | `aws security hub findings id` `aws arn` | arn:aws:guardduty:us-east-1:123456789012:detector/1234abcd12abab1ab12123456abcdef/finding/1234abcd12abab1ab12123456abcdef |
action_result.data.\*.AwsAccountId | string | | 01234567890 |
action_result.data.\*.CompanyName | string | | AWS |
action_result.data.\*.Compliance.AssociatedStandards.\*.StandardsId | string | | standards/aws-foundational-security-best-practices/v/1.0.0 |
action_result.data.\*.Compliance.SecurityControlId | string | | DynamoDB.2 |
action_result.data.\*.Compliance.Status | string | | WARNING |
action_result.data.\*.Compliance.StatusReasons.\*.Description | string | | Unable to describe the supporting AWS Config Rule, Please verify that you have enabled AWS Config. |
action_result.data.\*.Compliance.StatusReasons.\*.ReasonCode | string | | CONFIG_ACCESS_DENIED |
action_result.data.\*.CreatedAt | string | | 2019-04-10T11:58:12.766Z |
action_result.data.\*.Description | string | | EC2 instance has an unprotected port which is being probed by a known malicious host |
action_result.data.\*.FindingProviderFields.Severity.Label | string | | MEDIUM |
action_result.data.\*.FindingProviderFields.Severity.Original | string | | MEDIUM |
action_result.data.\*.FirstObservedAt | string | | 2019-04-10T11:48:10Z |
action_result.data.\*.GeneratorId | string | | arn:aws:guardduty:us-east-1:123456789012:detector/1234abcd12abab1ab12123456abcdef |
action_result.data.\*.Id | string | `aws security hub findings id` | arn:aws:guardduty:us-east-1:123456789012:detector/1234abcd12abab1ab12123456abcdef/finding/1234abcd12abab1ab12123456abcdef |
action_result.data.\*.LastObservedAt | string | | 2019-04-11T22:24:14Z |
action_result.data.\*.Network.DestinationDomain | string | `domain` | |
action_result.data.\*.Network.DestinationIpV4 | string | `ip` | |
action_result.data.\*.Network.DestinationIpV6 | string | `ip` | |
action_result.data.\*.Network.DestinationPort | string | `port` | |
action_result.data.\*.Network.Direction | string | | IN OUT |
action_result.data.\*.Network.Protocol | string | | |
action_result.data.\*.Network.SourceDomain | string | `domain` | |
action_result.data.\*.Network.SourceIpV4 | string | `aws security hub network source ip` `ip` | |
action_result.data.\*.Network.SourceIpV6 | string | `ip` | |
action_result.data.\*.Network.SourceMac | string | `mac address` | |
action_result.data.\*.Network.SourcePort | string | `port` | |
action_result.data.\*.Note.Text | string | | (test test - 2019-06-20 09:41:25) test overwrite false (test test - 2019-06-20 09:40:46) true |
action_result.data.\*.Note.UpdatedAt | string | | 2019-04-12T10:06:44.134Z |
action_result.data.\*.Note.UpdatedBy | string | | automation-test |
action_result.data.\*.ProductArn | string | | arn:aws:securityhub:us-east-1::product/aws/guardduty |
action_result.data.\*.ProductFields.RecommendationUrl | string | | https://docs.aws.amazon.com/console/securityhub/standards-cis-2.7/remediation |
action_result.data.\*.ProductFields.RelatedAWSResources:0/name | string | | securityhub-cloud-trail-encryption-enabled-e8fd8829 |
action_result.data.\*.ProductFields.RelatedAWSResources:0/type | string | | AWS::Config::ConfigRule |
action_result.data.\*.ProductFields.Resources:0/Id | string | | arn:aws:dynamodb:us-east-1:157568067690:table/doNotDeleteTable |
action_result.data.\*.ProductFields.RuleId | string | | 2.7 |
action_result.data.\*.ProductFields.StandardsControlArn | string | | arn:aws:securityhub:us-east-1:157568067690:control/cis-aws-foundations-benchmark/v/1.2.0/2.7 |
action_result.data.\*.ProductFields.StandardsGuideArn | string | | arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0 |
action_result.data.\*.ProductFields.StandardsGuideSubscriptionArn | string | | arn:aws:securityhub:us-east-1:157568067690:subscription/cis-aws-foundations-benchmark/v/1.2.0 |
action_result.data.\*.ProductFields.action/actionType | string | | PORT_PROBE |
action_result.data.\*.ProductFields.action/awsApiCallAction/api | string | | DescribeAlarms |
action_result.data.\*.ProductFields.action/awsApiCallAction/callerType | string | | Remote IP |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/city/cityName | string | | cityName |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/country/countryName | string | | countryName |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/geoLocation/lat | string | | 3337.4073 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/geoLocation/lon | string | | -1321.939 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/ipAddressV4 | string | `ip` | 12.123.1.1 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/organization/asn | string | | 1234 |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/organization/asnOrg | string | | Test Services, Inc. |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/organization/isp | string | | Test Services |
action_result.data.\*.ProductFields.action/awsApiCallAction/remoteIpDetails/organization/org | string | | Test Services |
action_result.data.\*.ProductFields.action/awsApiCallAction/serviceName | string | | monitoring.amazonaws.com |
action_result.data.\*.ProductFields.action/portProbeAction/blocked | string | | false |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/localPortDetails/port | string | | 22 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/localPortDetails/portName | string | | SSH |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/city/cityName | string | | cityName |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/country/countryName | string | | countryName |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/geoLocation/lat | string | | 9 3333.9492 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/geoLocation/lon | string | | -80 11338.2958 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/ipAddressV4 | string | `ip` | 123.12.1.1 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/asn | string | | 12345 |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/asnOrg | string | | Test B.v. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/isp | string | | Test S.A. |
action_result.data.\*.ProductFields.action/portProbeAction/portProbeDetails:0/remoteIpDetails/organization/org | string | | Test S.A. |
action_result.data.\*.ProductFields.additionalInfo | string | | {"threatName":"Scanner","threatListName":"ThreatListName"} |
action_result.data.\*.ProductFields.archived | string | | false |
action_result.data.\*.ProductFields.aws/guardduty/service/action/actionType | string | | AWS_API_CALL |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/affectedResources | string | | |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/api | string | | GetLayout |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/callerType | string | | Remote IP |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/city/cityName | string | | Mumbai |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/country/countryName | string | | India |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/geoLocation/lat | string | | 19.0748 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/geoLocation/lon | string | | 72.8856 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/ipAddressV4 | string | | 136.226.232.247 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/asn | string | | 53813 |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/asnOrg | string | | ZSCALER-INC |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/isp | string | | Zscaler |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/org | string | | Zscaler |
action_result.data.\*.ProductFields.aws/guardduty/service/action/awsApiCallAction/serviceName | string | | cloudshell.amazonaws.com |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/type | string | | default |
action_result.data.\*.ProductFields.aws/guardduty/service/additionalInfo/value | string | | |
action_result.data.\*.ProductFields.aws/guardduty/service/archived | string | | false |
action_result.data.\*.ProductFields.aws/guardduty/service/count | string | | 1584 |
action_result.data.\*.ProductFields.aws/guardduty/service/detectorId | string | | c8b6836865362e2b73f679f650bdaf16 |
action_result.data.\*.ProductFields.aws/guardduty/service/eventFirstSeen | string | | 2023-04-24T17:06:01.000Z |
action_result.data.\*.ProductFields.aws/guardduty/service/eventLastSeen | string | | 2023-04-27T05:22:52.000Z |
action_result.data.\*.ProductFields.aws/guardduty/service/resourceRole | string | | TARGET |
action_result.data.\*.ProductFields.aws/guardduty/service/serviceName | string | | guardduty |
action_result.data.\*.ProductFields.aws/securityhub/CompanyName | string | | test |
action_result.data.\*.ProductFields.aws/securityhub/FindingId | string | `aws arn` | arn:aws:securityhub:us-east-1::product/aws/guardduty/arn:aws:guardduty:us-east-1:123456789012:detector/123456abcdef1234abcdef/finding/123456abcdef1234abcdef |
action_result.data.\*.ProductFields.aws/securityhub/ProductName | string | | GuardDuty |
action_result.data.\*.ProductFields.aws/securityhub/SeverityLabel | string | | MEDIUM |
action_result.data.\*.ProductFields.aws/securityhub/annotation | string | | Unable to describe the supporting AWS Config Rule, Please verify that you have enabled AWS Config. |
action_result.data.\*.ProductFields.count | string | | 159 |
action_result.data.\*.ProductFields.detectorId | string | `md5` | 123456abcdef1234abcdef |
action_result.data.\*.ProductFields.resourceRole | string | | TARGET |
action_result.data.\*.ProductName | string | | Security Hub |
action_result.data.\*.RecordState | string | | ARCHIVED ACTIVE |
action_result.data.\*.Region | string | | us-east-1 |
action_result.data.\*.Remediation.Recommendation.Text | string | | For directions on how to fix this issue, please consult the AWS Security Hub CIS documentation. |
action_result.data.\*.Remediation.Recommendation.Url | string | | https://docs.aws.amazon.com/console/securityhub/standards-cis-2.7/remediation |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.ImageId | string | | ami-123456abcdef1234a |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.IpV4Addresses | string | `aws security hub resource ip` `ip` | 123.12.1.1 |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.LaunchedAt | string | | 2019-04-10T10:47:11.000Z |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.SubnetId | string | | subnet-123456abcdef |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.Type | string | | t2.micro |
action_result.data.\*.Resources.\*.Details.AwsEc2Instance.VpcId | string | | vpc-513464894 |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.PrincipalId | string | | 157568067690 |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.PrincipalName | string | | Root |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.PrincipalType | string | | Root |
action_result.data.\*.Resources.\*.Details.AwsIamAccessKey.UserName | string | | Root |
action_result.data.\*.Resources.\*.Id | string | `aws security hub resource id` | arn:aws:ec2:us-east-1:123456789012:instance/i-123456abcdef1234ab |
action_result.data.\*.Resources.\*.InstanceId | string | `aws ec2 instance id` | i-123456abcdef1234abcdef |
action_result.data.\*.Resources.\*.Partition | string | | test |
action_result.data.\*.Resources.\*.Region | string | `aws security hub resource region` | us-east-1 |
action_result.data.\*.Resources.\*.Tags.Name | string | | test-actions |
action_result.data.\*.Resources.\*.Tags.aws:autoscaling:groupName | string | | test-group |
action_result.data.\*.Resources.\*.Tags.new-key | string | | new-value |
action_result.data.\*.Resources.\*.Type | string | | AwsEc2Instance |
action_result.data.\*.Sample | boolean | | True False |
action_result.data.\*.SchemaVersion | string | | 2018-10-08 |
action_result.data.\*.Severity.Label | string | | MEDIUM |
action_result.data.\*.Severity.Normalized | numeric | | 40 |
action_result.data.\*.Severity.Original | string | | MEDIUM |
action_result.data.\*.Severity.Product | numeric | | 2 |
action_result.data.\*.SourceUrl | string | | https://us-east-1.console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?macros=current&fId=32c3da20b4a8e7cc262e2b21a35f5c04 |
action_result.data.\*.Title | string | | Unprotected port on EC2 instance i-123456abcdef1234abcd is being probed |
action_result.data.\*.Types | string | | TTPs/Discovery/Recon:EC2-PortProbeUnprotectedPort |
action_result.data.\*.UpdatedAt | string | | 2019-04-11T22:35:03.677Z |
action_result.data.\*.Workflow.Status | string | | NEW |
action_result.data.\*.WorkflowState | string | | NEW |
action_result.summary.total_findings | numeric | | 1 |
action_result.summary.total_groups | numeric | | 1 |
action_result.message | string | | Total findings: 1 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'archive findings'

Archive the AWS Security Hub aggregated findings specified by the filter attributes

Type: **contain** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings_id** | required | Identifier of security finding | string | `aws security hub findings id` `aws arn` |
**note** | optional | The text of a note | string | |
**overwrite** | optional | Check this box to overwrite the existing notes, otherwise, notes will be appended to existing notes | boolean | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.parameter.findings_id | string | `aws security hub findings id` `aws arn` | arn:aws:guardduty:us-east-1123456789012detector/123456abcdef1234abcdef123456abcdef1234abcdef/finding/123456abcdef1234abcdef |
action_result.parameter.note | string | | note for archive findings |
action_result.parameter.overwrite | boolean | | True False |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-headers | string | | Authorization,Date,X-Amz-Date,X-Amz-Security-Token,X-Amz-Target,content-type,x-amz-content-sha256,x-amz-user-agent,x-amzn-platform-id,x-amzn-trace-id |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-methods | string | | GET,POST,OPTIONS,PUT,PATCH,DELETE |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-origin | string | | * |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-expose-headers | string | | x-amzn-errortype,x-amzn-requestid,x-amzn-errormessage,x-amzn-trace-id,x-amz-apigw-id,date |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-max-age | string | | 86400 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string | | keep-alive |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string | | 2 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string | | application/json |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Fri, 12 Apr 2019 11:22:20 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-apigw-id | string | | ABCFD123456= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string | | 1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-trace-id | string | | Root=1-1234abcd-12ab-ab12-ab12-123456abcdef;Sampled=0 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.RequestId | string | | 1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary.archive_note | string | | Added successfully Error occurred while adding note Note is not added as it is not provided in the input parameters of the action |
action_result.summary.archived_status | string | | Successful Failed |
action_result.message | string | | Archive note: Added successfully, Archived status: Successful |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'unarchive findings'

Unarchive the AWS Security Hub aggregated findings specified by the filter attributes

Type: **correct** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings_id** | required | Identifier of security finding | string | `aws security hub findings id` `aws arn` |
**note** | optional | The text of a note | string | |
**overwrite** | optional | Check this box to overwrite the existing notes, otherwise, notes will be appended to existing notes | boolean | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.parameter.findings_id | string | `aws security hub findings id` `aws arn` | arn:aws:guardduty:us-east-1:123456789012:detector/123456abcdef1234abcdef123456abcdef1234abcdef/finding/123456abcdef1234abcdef123456abcdef1234abcdef |
action_result.parameter.note | string | | Unarchive |
action_result.parameter.overwrite | boolean | | True False |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-headers | string | | Authorization,Date,X-Amz-Date,X-Amz-Security-Token,X-Amz-Target,content-type,x-amz-content-sha256,x-amz-user-agent,x-amzn-platform-id,x-amzn-trace-id |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-methods | string | | GET,POST,OPTIONS,PUT,PATCH,DELETE |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-origin | string | | * |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-expose-headers | string | | x-amzn-errortype,x-amzn-requestid,x-amzn-errormessage,x-amzn-trace-id,x-amz-apigw-id,date |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-max-age | string | | 86400 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string | | keep-alive |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string | | 2 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string | | application/json |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Fri, 12 Apr 2019 11:24:59 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-apigw-id | string | | 123456abcdef1234= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string | | 1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-trace-id | string | | Root=1-1234abcd-12ab-ab12-ab12-123456abcdef;Sampled=0 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.RequestId | string | | 1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary.unarchive_note | string | | Added successfully Error occurred while adding note Note is not added as it is not provided in the input parameters of the action |
action_result.summary.unarchived_status | string | | Successful Failed |
action_result.message | string | | Unarchive note: Added successfully, Unarchived status: Successful |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'add note'

Add Note to the AWS Security Hub aggregated findings specified by the filter attributes

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings_id** | required | Identifier of security finding | string | `aws security hub findings id` `aws arn` |
**note** | required | The text of a note | string | |
**overwrite** | optional | Check this box to overwrite the existing notes, otherwise, notes will be appended to existing notes | boolean | |
**credentials** | optional | Assumed role credentials | string | `aws credentials` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.credentials | string | `aws credentials` | {'AccessKeyId': 'ASIASJL6ZZZZZ3M7QC2J', 'Expiration': '2021-06-07 22:28:04', 'SecretAccessKey': 'ZZZZZAmvLPictcVBPvjJx0d7MRezOuxiLCMZZZZZ', 'SessionToken': 'ZZZZZXIvYXdzEN///////////wEaDFRU0s4AVrw0k0oYICK4ATAzOqzAkg9bHY29lYmP59UvVOHjLufOy4s7SnAzOxGqGIXnukLis4TWNhrJl5R5nYyimrm6K/9d0Cw2SW9gO0ZRjEJHWJ+yY5Qk2QpWctS2BGn4n+G8cD6zEweCCMj+ScI5p8n7YI4wOdvXvOsVMmjV6F09Ujqr1w+NwoKXlglznXGs/7Q1kNZOMiioEhGUyoiHbQb37GCKslDK+oqe0KNaUKQ96YCepaLgMbMquDgdAM8I0TTxUO0o5ILF/gUyLT04R7QlOfktkdh6Qt0atTS+xeKi1hirKRizpJ8jjnxGQIikPRToL2v3ZZZZZZ=='} |
action_result.parameter.findings_id | string | `aws security hub findings id` `aws arn` | arn:aws:guardduty:us-east-1:123456789012:detector/123456789abcdefghi1234ab/finding/123456789abcdefghi1234ab |
action_result.parameter.note | string | | note for findings |
action_result.parameter.overwrite | boolean | | True False |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-headers | string | | Authorization,Date,X-Amz-Date,X-Amz-Security-Token,X-Amz-Target,content-type,x-amz-content-sha256,x-amz-user-agent,x-amzn-platform-id,x-amzn-trace-id |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-methods | string | | GET,POST,OPTIONS,PUT,PATCH,DELETE |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-allow-origin | string | | * |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-expose-headers | string | | x-amzn-errortype,x-amzn-requestid,x-amzn-errormessage,x-amzn-trace-id,x-amz-apigw-id,date |
action_result.data.\*.ResponseMetadata.HTTPHeaders.access-control-max-age | string | | 86400 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.connection | string | | keep-alive |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-length | string | | 2 |
action_result.data.\*.ResponseMetadata.HTTPHeaders.content-type | string | | application/json |
action_result.data.\*.ResponseMetadata.HTTPHeaders.date | string | | Fri, 12 Apr 2019 11:26:08 GMT |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amz-apigw-id | string | | 123456789abcdefghi1234ab= |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-requestid | string | | 1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.ResponseMetadata.HTTPHeaders.x-amzn-trace-id | string | | Root=1-5cb075cf-123456789abcdefghi1234ab;Sampled=0 |
action_result.data.\*.ResponseMetadata.HTTPStatusCode | numeric | | 200 |
action_result.data.\*.ResponseMetadata.RequestId | string | | 1234abcd-12ab-ab12-ab12-123456abcdef |
action_result.data.\*.ResponseMetadata.RetryAttempts | numeric | | 0 |
action_result.summary.add_note | string | | Success |
action_result.message | string | | Note added successfully to the provided findings ID |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
