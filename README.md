[comment]: # "Auto-generated SOAR connector documentation"
# AWS Security Hub

Publisher: Splunk  
Connector Version: 2\.3\.2  
Product Vendor: AWS  
Product Name: Security Hub  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.10\.0\.40961  

This app integrates with AWS Security Hub to ingest findings

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2016-2021 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)"
[comment]: # ""
**Functioning of On Poll**

-   There are two approaches for ingesting data using the On Poll action.  

-   **SQS Polling**

      

    SQS polling is the preferred ingestion technique due to limitations in the AWS SecurityHub API
    used to ingest findings. Detailed instructions on configuring SQS-polling can be found below.

-   **Normal Polling**

      
      

    1.  On Poll

        This is manual On Poll. Here, the findings data of the past N days (poll_now_days
        configuration parameter) will be ingested.

    2.  Scheduled Polling

        In the first run, the findings data of the past M days (Scheduled_poll_days configuration
        parameter) will be ingested and then, for the consecutive runs, only the findings are
        updated after the last run's time (last_ingested_date stored in the state file) will be
        fetched.

    3.  Interval Polling

        The logic of fetching and ingesting the findings is the same as scheduled polling.

      

## Ingesting Security Hub Findings from SQS

The following section explains how to configure the preferred means of ingesting findings from AWS,
SQS polling. These instructions leverage a CloudFormation template to set up the forwarding of
Security Hub findings into an SQS queue. Phantom in turn ingests the findings from this queue.

  

Note that SQS-based polling will ignore the **poll_now_days** and **scheduled_poll_days** asset
configuration parameters.

### 1 - Forward Security Hub Alerts to an SQS Queue

Start by navigating to the CloudFormation page on your AWS console and running CloudFormation
template linked below. The template will generate a new CloudWatch Event Rule which will forward all
new Security Hub findings to an SQS Queue.

CloudFormation Template:
<https://splunkphantom.s3.amazonaws.com/cloud-formation/phantom-sechub-to-sqs.yaml>

![Cloud Formation - Selecting the Phantom
Template](https://splunkphantom.s3.amazonaws.com/images/PhantomSecHubToSQSCloudFormation.png)

After the Cloud Formation stack has been created be sure to take note of the
*securityHubToPhantomSQSURL* field in the output - you will need it later.

![Cloud Formation
Output](https://splunkphantom.s3.amazonaws.com/images/PhantomCloudFormationOutputHighlighted.png)

### 2 - Configure your Phantom App Asset

Next, login to your Splunk Phantom instance. If you are new to Phantom you can easily launch the
Phantom Community Edition available in the AWS Marketplace.

Navigate to the "Apps" page in Phantom. Search for the Security Hub app - if you don't find it in
your search results, you may need to select the *New Apps* and install the app before proceeding.
Select "Configure New Asset" for the v1.1+ Security Hub App.

> **Important** These instructions require the Phantom Security Hub app v1.1 or higher - if you are
> running an older version, be sure to upgrade it by selecting "Upgrade Apps" in your phantom
> instance or downloading the latest version of the app from my.phantom.us/apps and manually
> installing it.

![Security Hub Phantom App
Configure](https://splunkphantom.s3.amazonaws.com/images/security-hub-app-asset.png)

### App Configuration Parameters

Setting up the Security Hub Phantom app requires input on 3 configuration tabs.

##### Asset Info

Provide a unique name asset name. It is a good idea to use a name that reminds you which AWS
environment the app connects to.

##### Ingest Settings

-   Select a Label to apply to all Findings consumed from security hub, or create a new one by
    typing in the drop-down box
-   Select "Interval" to enable periodic polling of the SQS Queue
-   Modify the polling interval as desired to suit your organization's needs.  

##### Asset Settings

Supply values for the following fields:

-   AWS Access Key - The access key associated with an IAM account
-   AWS Secret Key - The secret key associated with an IAM account
-   SQS URL - The URL provided by the Cloud Formation template from part 1 of this guide

![Security Hub Phantom App - Asset Settings
Tab](https://splunkphantom.s3.amazonaws.com/images/phantom-sechub-app-assetsettings.png)

### Finalize the Configuration

Once you have configured the Asset Info, Ingest Settings, and Asset Settings select *Save* to
finalize your app configuration. You are now ready to start consuming Security Hub Findings in
Phantom!

Any new Security Hub Findings will now appear on your Phantom "Events" page according to your
polling interval. Note that the integration relies on forwarding events from the Security Hub to the
SQS queue, so the app will only know about any findings that were created after the Cloud Formation
template was run in Step 1.

----------------------------------------------------------------------------------------------------


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Security Hub asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access\_key** |  optional  | password | AWS Access Key
**secret\_key** |  optional  | password | AWS Secret Key
**region** |  required  | string | AWS Region
**sqs\_url** |  optional  | string | SQS URL
**poll\_now\_days** |  required  | numeric | Poll last 'n' days for POLL NOW
**scheduled\_poll\_days** |  required  | numeric | Poll last 'n' days for scheduled polling
**use\_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[on poll](#action-on-poll) - Ingest findings from Security Hub  
[get findings](#action-get-findings) - Lists and describes Security Hub aggregated findings that are specified by a single filter attribute  
[get related findings](#action-get-related-findings) - Lists Security Hub aggregated findings that are specified by filter attributes  
[archive findings](#action-archive-findings) - Archive the AWS Security Hub aggregated findings specified by the filter attributes  
[unarchive findings](#action-unarchive-findings) - Unarchive the AWS Security Hub aggregated findings specified by the filter attributes  
[add note](#action-add-note) - Add Note to the AWS Security Hub aggregated findings specified by the filter attributes  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Ingest findings from Security Hub

Type: **ingest**  
Read only: **True**

This app supports two possible methods for ingesting findings\:<ul><li>Directly from Security Hub \- To use this method, leave the <b>sqs\_url</b> asset configuration field blank\.</li><li>Via an SQS Queue \- To use this method, add the URL of an SQS queue to the <b>sqs\_url</b> asset configuration field\. This method will ignore the <b>poll\_now\_days</b> and <b>scheduled\_poll\_days</b> asset configuration parameters\. Messages will be deleted from the queue after being received\.</li></ul>

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container\_id** |  optional  | Container IDs to limit the ingestion to | string | 
**start\_time** |  optional  | Start of the time range, in epoch time \(milliseconds\) | numeric | 
**end\_time** |  optional  | End of the time range, in epoch time \(milliseconds\) | numeric | 
**container\_count** |  optional  | Maximum number of container records to query for | numeric | 
**artifact\_count** |  optional  | Maximum number of artifact records to query for | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'get findings'
Lists and describes Security Hub aggregated findings that are specified by a single filter attribute

Type: **investigate**  
Read only: **True**

If none of the filter parameters are provided, all the findings will be fetched controlled by the limit parameter\. For the parameters 'resource\_ec2\_ipv4\_addresses' and 'network\_source\_ipv4', if the user provides comma\-separated values and one or more values are incorrect, then those values will be simply ignored and only correct values will be used for further filtering of the findings\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**resource\_id** |  optional  | The canonical identifier for the given resource type | string |  `aws security hub resource id`  `aws arn` 
**resource\_ec2\_ipv4\_addresses** |  optional  | Comma\-separated IPv4 addresses associated with the instance | string |  `aws security hub resource ip` 
**network\_source\_ipv4** |  optional  | Comma\-separated source IPv4 addresses of network\-related information about a finding | string |  `aws security hub network source ip` 
**network\_source\_mac** |  optional  | The source media access control \(MAC\) address of network\-related information about a finding | string |  `mac address` 
**resource\_region** |  optional  | The canonical AWS external region name where this resource is located | string |  `aws security hub resource region` 
**limit** |  optional  | Maximum number of findings to be fetched | numeric | 
**is\_archived** |  optional  | Flag to fetch the archived findings | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.is\_archived | boolean | 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.network\_source\_ipv4 | string |  `aws security hub network source ip` 
action\_result\.parameter\.network\_source\_mac | string |  `mac address` 
action\_result\.parameter\.resource\_ec2\_ipv4\_addresses | string |  `aws security hub resource ip` 
action\_result\.parameter\.resource\_id | string |  `aws security hub resource id`  `aws arn` 
action\_result\.parameter\.resource\_region | string |  `aws security hub resource region` 
action\_result\.data\.\*\.AwsAccountId | string | 
action\_result\.data\.\*\.Compliance\.Status | string | 
action\_result\.data\.\*\.Compliance\.StatusReasons\.\*\.Description | string | 
action\_result\.data\.\*\.Compliance\.StatusReasons\.\*\.ReasonCode | string | 
action\_result\.data\.\*\.Confidence | numeric | 
action\_result\.data\.\*\.CreatedAt | string | 
action\_result\.data\.\*\.Description | string | 
action\_result\.data\.\*\.FirstObservedAt | string | 
action\_result\.data\.\*\.GeneratorId | string | 
action\_result\.data\.\*\.Id | string |  `aws security hub findings id` 
action\_result\.data\.\*\.LastObservedAt | string | 
action\_result\.data\.\*\.Network\.DestinationDomain | string |  `domain` 
action\_result\.data\.\*\.Network\.DestinationIpV4 | string |  `ip` 
action\_result\.data\.\*\.Network\.DestinationIpV6 | string |  `ip` 
action\_result\.data\.\*\.Network\.DestinationPort | string |  `port` 
action\_result\.data\.\*\.Network\.Direction | string | 
action\_result\.data\.\*\.Network\.Protocol | string | 
action\_result\.data\.\*\.Network\.SourceDomain | string |  `domain` 
action\_result\.data\.\*\.Network\.SourceIpV4 | string |  `aws security hub network source ip`  `ip` 
action\_result\.data\.\*\.Network\.SourceIpV6 | string |  `ip` 
action\_result\.data\.\*\.Network\.SourceMac | string |  `mac address` 
action\_result\.data\.\*\.Network\.SourcePort | string |  `port` 
action\_result\.data\.\*\.NextToken | string | 
action\_result\.data\.\*\.Note\.Text | string | 
action\_result\.data\.\*\.Note\.UpdatedAt | string | 
action\_result\.data\.\*\.Note\.UpdatedBy | string | 
action\_result\.data\.\*\.ProductArn | string | 
action\_result\.data\.\*\.ProductFields\.RecommendationUrl | string | 
action\_result\.data\.\*\.ProductFields\.RelatedAWSResources\:0/name | string | 
action\_result\.data\.\*\.ProductFields\.RelatedAWSResources\:0/type | string | 
action\_result\.data\.\*\.ProductFields\.RuleId | string | 
action\_result\.data\.\*\.ProductFields\.StandardsControlArn | string | 
action\_result\.data\.\*\.ProductFields\.StandardsGuideArn | string | 
action\_result\.data\.\*\.ProductFields\.StandardsGuideSubscriptionArn | string | 
action\_result\.data\.\*\.ProductFields\.action/actionType | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/api | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/callerType | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/geoLocation/isp | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/ipAddressV4 | string |  `ip` 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/serviceName | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/blocked | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/connectionDirection | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/protocol | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/ipAddressV4 | string |  `ip` 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remotePortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.action/networkConnectionAction/remotePortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/blocked | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/ipAddressV4 | string |  `ip` 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/ipAddressV4 | string |  `ip` 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:1/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/ipAddressV4 | string |  `ip` 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:2/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.additionalInfo | string | 
action\_result\.data\.\*\.ProductFields\.archived | string | 
action\_result\.data\.\*\.ProductFields\.attributes/ACL | string | 
action\_result\.data\.\*\.ProductFields\.attributes/ENI | string | 
action\_result\.data\.\*\.ProductFields\.attributes/IGW | string | 
action\_result\.data\.\*\.ProductFields\.attributes/INSTANCE\_ID | string | 
action\_result\.data\.\*\.ProductFields\.attributes/PORT | string | 
action\_result\.data\.\*\.ProductFields\.attributes/PORT\_GROUP\_NAME | string | 
action\_result\.data\.\*\.ProductFields\.attributes/PROTOCOL | string | 
action\_result\.data\.\*\.ProductFields\.attributes/REACHABILITY\_TYPE | string | 
action\_result\.data\.\*\.ProductFields\.attributes/RULE\_TYPE | string | 
action\_result\.data\.\*\.ProductFields\.attributes/SECURITY\_GROUP | string | 
action\_result\.data\.\*\.ProductFields\.attributes/TCP\_PORTS | string | 
action\_result\.data\.\*\.ProductFields\.attributes/UDP\_PORTS | string | 
action\_result\.data\.\*\.ProductFields\.attributes/VPC | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:0/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:0/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:1/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:1/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:10/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:10/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:2/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:2/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:3/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:3/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:4/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:4/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:5/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:5/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:6/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:6/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:7/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:7/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:8/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:8/value | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:9/key | string | 
action\_result\.data\.\*\.ProductFields\.attributes\:9/value | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/actionType | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/affectedResources | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS\:\:CloudTrail\:\:Trail | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS\:\:EC2\:\:Instance | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS\:\:IAM\:\:Role | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS\:\:IAM\:\:User | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/affectedResources/AWS\:\:S3\:\:Bucket | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/api | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/callerType | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/errorCode | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/city | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/awsApiCallAction/serviceName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/dnsRequestAction/blocked | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/dnsRequestAction/domain | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/dnsRequestAction/protocol | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/blocked | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/connectionDirection | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/localIpDetails/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/protocol | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remotePortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/networkConnectionAction/remotePortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/blocked | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/localIpDetails/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.0\_/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/localIpDetails/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/action/portProbeAction/portProbeDetails\.1\_/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/additionalScannedPorts | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.0\_/count | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.0\_/firstSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.0\_/lastSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.0\_/name | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.1\_/count | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.1\_/firstSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.1\_/lastSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.1\_/name | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.2\_/count | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.2\_/firstSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.2\_/lastSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/apiCalls\.2\_/name | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/domain | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/inBytes | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/localPort | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/allowUsersToChangePassword | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/hardExpiry | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/maxPasswordAge | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/minimumPasswordLength | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/passwordReusePrevention | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/requireLowercaseCharacters | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/requireNumbers | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/requireSymbols | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/newPolicy/requireUppercaseCharacters | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/allowUsersToChangePassword | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/hardExpiry | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/maxPasswordAge | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/minimumPasswordLength | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/passwordReusePrevention | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/requireLowercaseCharacters | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/requireNumbers | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/requireSymbols | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/oldPolicy/requireUppercaseCharacters | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/outBytes | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/policyArn | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/portsScannedSample\.0\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/portsScannedSample\.10\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/portsScannedSample\.11\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentApiCalls\.0\_/api | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentApiCalls\.0\_/count | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentApiCalls\.1\_/api | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentApiCalls\.1\_/count | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.0\_/accessKeyId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.0\_/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.0\_/principalId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.1\_/accessKeyId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.1\_/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.1\_/principalId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.2\_/accessKeyId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.2\_/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.2\_/principalId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.3\_/accessKeyId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.3\_/ipAddressV4 | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/recentCredentials\.3\_/principalId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/sample | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/scannedPort | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/threatListName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/threatName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusual | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusual/countries\.0\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusual/countries\.1\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusual/countries\.2\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusual/hoursOfDay\.0\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusual/isps | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusual/userNames\.0\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/additionalInfo/unusualProtocol | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/archived | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/count | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/detectorId | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/eventFirstSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/eventLastSeen | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/evidence | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/evidence/threatIntelligenceDetails\.0\_/threatListName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/evidence/threatIntelligenceDetails\.0\_/threatNames | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/evidence/threatIntelligenceDetails\.0\_/threatNames\.0\_ | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/resourceRole | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/serviceName | string | 
action\_result\.data\.\*\.ProductFields\.aws/guardduty/service/userFeedback | string | 
action\_result\.data\.\*\.ProductFields\.aws/inspector/RulesPackageName | string | 
action\_result\.data\.\*\.ProductFields\.aws/inspector/arn | string | 
action\_result\.data\.\*\.ProductFields\.aws/inspector/id | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/CompanyName | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/FindingId | string |  `aws arn` 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/ProductName | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/SeverityLabel | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/annotation | string | 
action\_result\.data\.\*\.ProductFields\.count | string | 
action\_result\.data\.\*\.ProductFields\.detectorId | string |  `md5` 
action\_result\.data\.\*\.ProductFields\.dlpRisk\:0/count | string | 
action\_result\.data\.\*\.ProductFields\.dlpRisk\:0/risk | string | 
action\_result\.data\.\*\.ProductFields\.owner\:0/count | string | 
action\_result\.data\.\*\.ProductFields\.owner\:0/name | string | 
action\_result\.data\.\*\.ProductFields\.resourceRole | string | 
action\_result\.data\.\*\.ProductFields\.rule\-arn | string | 
action\_result\.data\.\*\.ProductFields\.serviceAttributes/assessmentRunArn | string | 
action\_result\.data\.\*\.ProductFields\.serviceAttributes/rulesPackageArn | string | 
action\_result\.data\.\*\.ProductFields\.serviceAttributes/schemaVersion | string | 
action\_result\.data\.\*\.ProductFields\.tags\:0 | string | 
action\_result\.data\.\*\.ProductFields\.tags\:1 | string | 
action\_result\.data\.\*\.ProductFields\.themes\:0/count | string | 
action\_result\.data\.\*\.ProductFields\.themes\:0/theme | string | 
action\_result\.data\.\*\.RecordState | string | 
action\_result\.data\.\*\.Remediation\.Recommendation\.Text | string | 
action\_result\.data\.\*\.Remediation\.Recommendation\.Url | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.IamInstanceProfileArn | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.ImageId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.IpV4Addresses | string |  `aws security hub resource ip`  `ip` 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.LaunchedAt | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.SubnetId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.Type | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.VpcId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsIamAccessKey\.PrincipalId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsIamAccessKey\.PrincipalName | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsIamAccessKey\.PrincipalType | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsIamAccessKey\.UserName | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsS3Bucket\.CreatedAt | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsS3Bucket\.OwnerId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsS3Bucket\.ServerSideEncryptionConfiguration\.Rules\.\*\.ApplyServerSideEncryptionByDefault\.KMSMasterKeyID | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsS3Bucket\.ServerSideEncryptionConfiguration\.Rules\.\*\.ApplyServerSideEncryptionByDefault\.SSEAlgorithm | string | 
action\_result\.data\.\*\.Resources\.\*\.Id | string |  `aws security hub resource id` 
action\_result\.data\.\*\.Resources\.\*\.InstanceId | string |  `aws ec2 instance id` 
action\_result\.data\.\*\.Resources\.\*\.Partition | string | 
action\_result\.data\.\*\.Resources\.\*\.Region | string |  `aws security hub resource region` 
action\_result\.data\.\*\.Resources\.\*\.Tags\.APP | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.ASG | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.App | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.Description | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.GeneratedFindingInstaceTag1 | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.GeneratedFindingInstaceTag2 | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.JIRA | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.Name | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.Project | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.Ticket | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.aws\:autoscaling\:groupName | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.aws\:cloudformation\:logical\-id | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.aws\:cloudformation\:stack\-id | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.aws\:cloudformation\:stack\-name | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.btest | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.foo | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.name | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.new\-key | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.owner | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.purpose | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.userid | string | 
action\_result\.data\.\*\.Resources\.\*\.Type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.data\.\*\.SchemaVersion | string | 
action\_result\.data\.\*\.Severity\.Label | string | 
action\_result\.data\.\*\.Severity\.Normalized | numeric | 
action\_result\.data\.\*\.Severity\.Original | string | 
action\_result\.data\.\*\.Severity\.Product | numeric | 
action\_result\.data\.\*\.SourceUrl | string | 
action\_result\.data\.\*\.Title | string | 
action\_result\.data\.\*\.Types | string | 
action\_result\.data\.\*\.UpdatedAt | string | 
action\_result\.data\.\*\.Workflow\.Status | string | 
action\_result\.data\.\*\.WorkflowState | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_findings | numeric | 
action\_result\.summary\.total\_groups | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'get related findings'
Lists Security Hub aggregated findings that are specified by filter attributes

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings\_id** |  required  | Identifier of security finding | string |  `aws security hub findings id`  `aws arn` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.findings\_id | string |  `aws security hub findings id`  `aws arn` 
action\_result\.data\.\*\.AwsAccountId | string | 
action\_result\.data\.\*\.Compliance\.Status | string | 
action\_result\.data\.\*\.Compliance\.StatusReasons\.\*\.Description | string | 
action\_result\.data\.\*\.Compliance\.StatusReasons\.\*\.ReasonCode | string | 
action\_result\.data\.\*\.CreatedAt | string | 
action\_result\.data\.\*\.Description | string | 
action\_result\.data\.\*\.FirstObservedAt | string | 
action\_result\.data\.\*\.GeneratorId | string | 
action\_result\.data\.\*\.Id | string |  `aws security hub findings id` 
action\_result\.data\.\*\.LastObservedAt | string | 
action\_result\.data\.\*\.Network\.DestinationDomain | string |  `domain` 
action\_result\.data\.\*\.Network\.DestinationIpV4 | string |  `ip` 
action\_result\.data\.\*\.Network\.DestinationIpV6 | string |  `ip` 
action\_result\.data\.\*\.Network\.DestinationPort | string |  `port` 
action\_result\.data\.\*\.Network\.Direction | string | 
action\_result\.data\.\*\.Network\.Protocol | string | 
action\_result\.data\.\*\.Network\.SourceDomain | string |  `domain` 
action\_result\.data\.\*\.Network\.SourceIpV4 | string |  `aws security hub network source ip`  `ip` 
action\_result\.data\.\*\.Network\.SourceIpV6 | string |  `ip` 
action\_result\.data\.\*\.Network\.SourceMac | string |  `mac address` 
action\_result\.data\.\*\.Network\.SourcePort | string |  `port` 
action\_result\.data\.\*\.Note\.Text | string | 
action\_result\.data\.\*\.Note\.UpdatedAt | string | 
action\_result\.data\.\*\.Note\.UpdatedBy | string | 
action\_result\.data\.\*\.ProductArn | string | 
action\_result\.data\.\*\.ProductFields\.RecommendationUrl | string | 
action\_result\.data\.\*\.ProductFields\.RelatedAWSResources\:0/name | string | 
action\_result\.data\.\*\.ProductFields\.RelatedAWSResources\:0/type | string | 
action\_result\.data\.\*\.ProductFields\.RuleId | string | 
action\_result\.data\.\*\.ProductFields\.StandardsControlArn | string | 
action\_result\.data\.\*\.ProductFields\.StandardsGuideArn | string | 
action\_result\.data\.\*\.ProductFields\.StandardsGuideSubscriptionArn | string | 
action\_result\.data\.\*\.ProductFields\.action/actionType | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/api | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/callerType | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/ipAddressV4 | string |  `ip` 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.action/awsApiCallAction/serviceName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/blocked | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/localPortDetails/port | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/localPortDetails/portName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/city/cityName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/country/countryName | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/geoLocation/lat | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/geoLocation/lon | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/ipAddressV4 | string |  `ip` 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/asn | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/asnOrg | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/isp | string | 
action\_result\.data\.\*\.ProductFields\.action/portProbeAction/portProbeDetails\:0/remoteIpDetails/organization/org | string | 
action\_result\.data\.\*\.ProductFields\.additionalInfo | string | 
action\_result\.data\.\*\.ProductFields\.archived | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/CompanyName | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/FindingId | string |  `aws arn` 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/ProductName | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/SeverityLabel | string | 
action\_result\.data\.\*\.ProductFields\.aws/securityhub/annotation | string | 
action\_result\.data\.\*\.ProductFields\.count | string | 
action\_result\.data\.\*\.ProductFields\.detectorId | string |  `md5` 
action\_result\.data\.\*\.ProductFields\.resourceRole | string | 
action\_result\.data\.\*\.RecordState | string | 
action\_result\.data\.\*\.Remediation\.Recommendation\.Text | string | 
action\_result\.data\.\*\.Remediation\.Recommendation\.Url | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.ImageId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.IpV4Addresses | string |  `aws security hub resource ip`  `ip` 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.LaunchedAt | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.SubnetId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.Type | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsEc2Instance\.VpcId | string | 
action\_result\.data\.\*\.Resources\.\*\.Details\.AwsIamAccessKey\.UserName | string | 
action\_result\.data\.\*\.Resources\.\*\.Id | string |  `aws security hub resource id` 
action\_result\.data\.\*\.Resources\.\*\.InstanceId | string |  `aws ec2 instance id` 
action\_result\.data\.\*\.Resources\.\*\.Partition | string | 
action\_result\.data\.\*\.Resources\.\*\.Region | string |  `aws security hub resource region` 
action\_result\.data\.\*\.Resources\.\*\.Tags\.Name | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.aws\:autoscaling\:groupName | string | 
action\_result\.data\.\*\.Resources\.\*\.Tags\.new\-key | string | 
action\_result\.data\.\*\.Resources\.\*\.Type | string | 
action\_result\.data\.\*\.SchemaVersion | string | 
action\_result\.data\.\*\.Severity\.Label | string | 
action\_result\.data\.\*\.Severity\.Normalized | numeric | 
action\_result\.data\.\*\.Severity\.Original | string | 
action\_result\.data\.\*\.Severity\.Product | numeric | 
action\_result\.data\.\*\.Title | string | 
action\_result\.data\.\*\.Types | string | 
action\_result\.data\.\*\.UpdatedAt | string | 
action\_result\.data\.\*\.Workflow\.Status | string | 
action\_result\.data\.\*\.WorkflowState | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.total\_findings | numeric | 
action\_result\.summary\.total\_groups | numeric | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'archive findings'
Archive the AWS Security Hub aggregated findings specified by the filter attributes

Type: **contain**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings\_id** |  required  | Identifier of security finding | string |  `aws security hub findings id`  `aws arn` 
**note** |  optional  | The text of a note | string | 
**overwrite** |  optional  | Check this box to overwrite the existing notes, otherwise, notes will be appended to existing notes | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.findings\_id | string |  `aws security hub findings id`  `aws arn` 
action\_result\.parameter\.note | string | 
action\_result\.parameter\.overwrite | boolean | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-apigw\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-trace\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.archive\_note | string | 
action\_result\.summary\.archived\_status | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'unarchive findings'
Unarchive the AWS Security Hub aggregated findings specified by the filter attributes

Type: **correct**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings\_id** |  required  | Identifier of security finding | string |  `aws security hub findings id`  `aws arn` 
**note** |  optional  | The text of a note | string | 
**overwrite** |  optional  | Check this box to overwrite the existing notes, otherwise, notes will be appended to existing notes | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.findings\_id | string |  `aws security hub findings id`  `aws arn` 
action\_result\.parameter\.note | string | 
action\_result\.parameter\.overwrite | boolean | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-apigw\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-trace\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.unarchive\_note | string | 
action\_result\.summary\.unarchived\_status | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'add note'
Add Note to the AWS Security Hub aggregated findings specified by the filter attributes

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**findings\_id** |  required  | Identifier of security finding | string |  `aws security hub findings id`  `aws arn` 
**note** |  required  | The text of a note | string | 
**overwrite** |  optional  | Check this box to overwrite the existing notes, otherwise, notes will be appended to existing notes | boolean | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.findings\_id | string |  `aws security hub findings id`  `aws arn` 
action\_result\.parameter\.note | string | 
action\_result\.parameter\.overwrite | boolean | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.connection | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-length | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.content\-type | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.date | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amz\-apigw\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-requestid | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPHeaders\.x\-amzn\-trace\-id | string | 
action\_result\.data\.\*\.ResponseMetadata\.HTTPStatusCode | numeric | 
action\_result\.data\.\*\.ResponseMetadata\.RequestId | string | 
action\_result\.data\.\*\.ResponseMetadata\.RetryAttempts | numeric | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.summary\.add\_note | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials` 