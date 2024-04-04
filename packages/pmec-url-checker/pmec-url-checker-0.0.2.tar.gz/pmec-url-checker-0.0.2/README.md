# Url Checker

## Introduction
Url Checker tool is intended to run a series of tests to check mandatory and optional firewall settings on the network where you deploy your AP5GC on Azure Stack Edge devices. The tool returns Pass/Fail status for each URL and saves a report file with more detail. Along with the URL, it also checks if the configured NTP server is accessible or not. This tool is capable of checking the required URLs for each layers such as Azure Stack Edge device, Network function manager, Azure Arc and AP5GC facilitate the checking of URLs required for ASE configuration, ARC configuration on ASE and PMEC installation. 

The tool is designed by using python programming language. You can run the tool on any machine where python is installed. The tool is designed to run on Windows, Linux and Mac OS.

See the [Contribution guidelines for this project](CONTRIBUTING.md) for details on how to make changes to this utility.

## About the tool
This tool can check whether the firewall settings for mandatory URL patterns meets to commission the ASE and AP5GC installation.
Below Prerequsites are being checked by the tool:
- The Domain Name System (DNS) server is available and functioning.
- The Network Time Protocol (NTP) server is available and functioning.
- DNS resoultion is working for all the Azure URLs.
- Azure Endpoints are available for Azure Stack Edge device, Network function manager, Azure Arc and AP5GC.

## Report file and logging
The tool saves a report into csv format url_checker_report.csv on user's home directory unless -o option is given, 
The report file contains the list of URLs tested and its status and failure reason if any that are collected during each test. This information can be helpful if you need to contact Microsoft Support.

It also dispays the detailed information on the console based on the verbose option -v or -vv provided.

## Build

~~~shell
# Clone repository
git clone <Git repo>
cd <Repo name>

# Install dependencies
poetry install

# Build the tool
poetry build
~~~


## static checks
~~~shell
## Development
# Autoformat, add (--dry-run) to see proposed changes before they are applied
poetry run python-static-checks fmt

# Perform other checks
poetry run python-static-checks check
poetry run mypy .
~~~

## Upload to python artifactory
~~~shell
python setup.py sdist bdist_wheel
twine upload dist/*
~~~

## Install

~~~shell
# install the tool locally
pip install .
python setup.py install

# install the tool from python artifactory
pip install pmec-url-checker
~~~


## Usage

Before running the tool, make sure the prerequisites are met. The tool requires python 3.9 or later to be installed on the machine.:

- Open the cmd(windows) or terminal(linux) and run the below command to check the help of the tool.

```shell
pmec-url-checker --help
usage: pmec-url-checker [-h] [-c <Azure Cloud type>] [--custom-url CUSTOM_URL [CUSTOM_URL ...]] -d <List of DNS Server> [<List of DNS Server> ...] [-o <Output File Path>]
                  [-r <Region in small case without space>] [--skip-test <Skip Test> [<Skip Test> ...]] [-s <Source IP>] [-t <List of NTP Server> [<List of NTP Server> ...]] [-v] [--version]

URL Checker tool for AP5GC

optional arguments:
  -h, --help            show this help message and exit
  -c <Azure Cloud type>, --cloud <Azure Cloud type>
                        Indicates the Azure environment. Required if the device is deployed to an environment other than the Azure public cloud (Azure Cloud). Supported values are [ AzureCloud |
                        AzureChinaCloud | AzureUSGovernmentCloud | AzureGermanCloud ]
  --custom-url CUSTOM_URL [CUSTOM_URL ...]
                        List ofs other URLs that you want to test HTTP access to.
  -d <List of DNS Server> [<List of DNS Server> ...], --dns-server <List of DNS Server> [<List of DNS Server> ...]
                        IP addresses of the DNS servers (for example, your primary and secondary DNS servers) used for name resolution of URLs.
  -o <Output File Path>, --output <Output File Path>
                        Dump the Result into file.
  -r <Region in small case without space>, --region <Region in small case without space>
                        Deployment Region ( default to eastus).
  --skip-test <Skip Test> [<Skip Test> ...]
                        skip checking URLs ( Supported values are [ASE, ARC, NFM, PMEC]).
  -s <Source IP>, --source-ip <Source IP>
                        Source IP address to be used for querying the HTTP request.
  -t <List of NTP Server> [<List of NTP Server> ...], --time-server <List of NTP Server> [<List of NTP Server> ...]
                        FQDN of one or more Network Time Protocol (NTP) servers used in ASE
  -v, --Verbose         Increase verbosity level
  --version             show program's version number and exit

```

- Run the below command to check the URLs and NTP servers for the default Azure Cloud environment.
```shell
pmec-url-checker -d 8.8.8.8 -c AzureCloud -r eastus -t pool.ntp.org


Testing the URL Endpoints.
2024-03-05 23:11:10,302 - ERROR - The Domain name does not exist: None of DNS query names exist: privatemecprivatemecartifactstore052cdf040a.azurecr.io., privatemecprivatemecartifactstore052cdf040a.azurecr.io.ad.datcon.co.uk., privatemecprivatemecartifactstore052cdf040a.azurecr.io.datcon.co.uk.
2024-03-05 23:11:10,303 - ERROR - Failed to resolve the FQDN: privatemecprivatemecartifactstore052cdf040a.azurecr.io with error: Domain name does not exist
2024-03-05 23:11:18,771 - ERROR - No Answer received for the Query: The DNS response does not contain an answer to the question: prod.hot.ingestion.msftcloudes.com. IN A
2024-03-05 23:11:18,771 - ERROR - Failed to resolve the FQDN: prod.hot.ingestion.msftcloudes.com with error: No Answer received
2024-03-05 23:11:20,240 - ERROR - The Domain name does not exist: None of DNS query names exist: eastus.login.microsoft.net., eastus.login.microsoft.net.ad.datcon.co.uk., eastus.login.microsoft.net.datcon.co.uk.
2024-03-05 23:11:20,240 - ERROR - Failed to resolve the FQDN: eastus.login.microsoft.net with error: Domain name does not exist
2024-03-05 23:11:54,998 - ERROR - The Domain name does not exist: None of DNS query names exist: wustat.windows.com., wustat.windows.com.ad.datcon.co.uk., wustat.windows.com.datcon.co.uk.
2024-03-05 23:11:54,998 - ERROR - Failed to resolve the FQDN: wustat.windows.com with error: Domain name does not exist


        URL Endpoints for ASE: Partially Pass
        URL Endpoints for ARC: Partially Pass
        URL Endpoints for NFM: Pass
        URL Endpoints for PMEC: Partially Pass

Testing the NTP Server.
        NTP Server pool.ntp.org: PASS

URL Checker completed successfully.
To view the complete URL status in detail, View the Report at Location: /home/sagar_bhatt/url_checker_report.csv
```

- To bind the DNS and HTTP request with specific source IP, you can use -s option.
```shell
pmec-url-checker -d 8.8.8.8 -c AzureCloud -r eastus -t pool.ntp.org -vv -s 172.24.190.7
```

- For more verbose output, you can use -v or -vv option.
```shell
pmec-url-checker -d 8.8.8.8 -c AzureCloud -r eastus -t pool.ntp.org -vv

pmec-url-checker -d 8.8.8.8 -c AzureCloud -r eastus -t pool.ntp.org -vv

Testing the URL Endpoints.
2024-03-05 23:18:43,512 - INFO - ----------------------------------------------------
2024-03-05 23:18:43,513 - INFO - Total URLs to be checked: 63
2024-03-05 23:18:43,513 - INFO - ----------------------------------------------------
2024-03-05 23:18:43,513 - INFO - Checking the URL accessibility: https://privatemecprivatemecartifactstore4ab6cc42d9.azurecr.io/v2/_catalog
2024-03-05 23:18:43,514 - INFO - Resolving the FQDN (privatemecprivatemecartifactstore4ab6cc42d9.azurecr.io) using the provided DNS server


2024-03-05 23:18:43,588 - DEBUG - Received DNS Response:
2024-03-05 23:18:43,589 - DEBUG - Server:        8.8.8.8
2024-03-05 23:18:43,589 - DEBUG - Address:       8.8.8.8#53

2024-03-05 23:18:43,589 - DEBUG - Source Ip:
2024-03-05 23:18:43,589 - DEBUG - Answers:
2024-03-05 23:18:43,589 - DEBUG -       IP:  20.38.140.204      Type:  RdataType.A
2024-03-05 23:18:43,589 - DEBUG - Testing Webrequest to: https://20.38.140.204/v2/_catalog  Source: None
2024-03-05 23:18:43,592 - DEBUG - Starting new HTTPS connection (1): 20.38.140.204:443
2024-03-05 23:18:43,880 - DEBUG - https://20.38.140.204:443 "GET /v2/_catalog HTTP/1.1" 400 0
2024-03-05 23:18:43,881 - DEBUG - HTTP Status Code: 400
2024-03-05 23:18:43,881 - DEBUG - PASS: Successfull webrequest using Source IP None to: https://20.38.140.204/v2/_catalog
2024-03-05 23:18:43,882 - INFO - PASS: URL is accessible: https://20.38.140.204/v2/_catalog
2024-03-05 23:18:43,882 - INFO - ----------------------------------------------------
2024-03-05 23:18:43,883 - INFO - Checking the URL accessibility: https://privatemecdevpublisherprivatemecdevartifactstore1c.azurecr.io/v2/_catalog
2024-03-05 23:18:43,884 - INFO - Resolving the FQDN (privatemecdevpublisherprivatemecdevartifactstore1c.azurecr.io) using the provided DNS server
...

```

- To dump the result into a file, at user specified location you can use -o option. 
```shell
pmec-url-checker -d 8.8.8.8 -c AzureCloud -r eastus -t pool.ntp.org -vv -o /home/<User>/report.csv
```

## Review Report File. 
The report file contains the list of URLs tested and its status and failure reason if any that are collected during each test. This information can be helpful if you need to contact Microsoft Support.

|    | Cloud Environment |	Layer	| URL	                                                                         | Service	 | Status     | Reason  |
|----|-------------------|--------|----------------------------------------------------------------------------------|-----------|------------|---------|
|Cloud Environment|Layer|URL|Service|Status|Reason
0|AzureCloud|PMEC|https://privatemecprivatemecartifactstore4ab6cc42d9.azurecr.io/v2/_catalog|Azure Container Registry|Pass|NA
1|AzureCloud|PMEC|https://privatemecdevpublisherprivatemecdevartifactstore1c.azurecr.io/v2/_catalog|Azure Container Registry|Pass|NA
2|AzureCloud|PMEC|https://privatemecdevpublishereastus2euapprivatea803a14a92.azurecr.io/v2/_catalog|Azure Container Registry|Pass|NA
3|AzureCloud|PMEC|https://privatemecdevpublishercentraluseuappriva6b3529cad4.azurecr.io/v2/_catalog|Azure Container Registry|Pass|NA
4|AzureCloud|PMEC|https://privatemeceastus2euapprivatemecartifactsf14e732aab.azurecr.io/v2/_catalog|Azure Container Registry|Pass|NA
5|AzureCloud|PMEC|https://privatemeccentraluseuapprivatemecartifac166168b140.azurecr.io/v2/_catalog|Azure Container Registry|Pass|NA
6|AzureCloud|PMEC|https://pcmeprodeastusacr.azurecr.io/v2/_catalog|Azure Container Registry|Pass|NA
7|AzureCloud|PMEC|https://global.prod.microsoftmetrics.com/|Monitoring and telemetry|Pass|NA
8|AzureCloud|PMEC|https://global.int.microsoftmetrics.com/|Monitoring and telemetry|Pass|NA
9|AzureCloud|PMEC|https://global.ppe.microsoftmetrics.com/|Monitoring and telemetry|Pass|NA
10|AzureCloud|PMEC|https://prod.hot.ingestion.msftcloudes.com/|Monitoring and telemetry|Fail|No Answer received
11|AzureCloud|ARC|https://eastus.dp.kubernetesconfiguration.azure.com|Data Plane Endpoint|Pass|NA
12|AzureCloud|ARC|https://login.windows.net|To Update ARM tokens|Pass|NA
13|AzureCloud|ARC|https://eastus.login.microsoft.net|To Update ARM tokens|Fail|Domain name does not exist
14|AzureCloud|ARC|https://eastus.login.microsoft.com|To Update ARM tokens|Pass|NA
15|AzureCloud|ARC|https://eastus.data.mcr.microsoft.com/v2/_catalog|Container service for ARC Agent|Pass|NA
16|AzureCloud|ARC|https://gbl.his.arc.azure.com|System Assigned Managed Identity|Pass|NA
17|AzureCloud|ARC|https://eus.his.arc.azure.com|System Assigned Managed Identity|Pass|NA
18|AzureCloud|ARC|https://k8connecthelm.azureedge.net|For Cluster Connect and for Custom Location|Pass|NA
19|AzureCloud|ARC|https://guestnotificationservice.azure.com|For Cluster Connect and for Custom Location|Pass|NA
20|AzureCloud|ARC|https://sts.windows.net|For Cluster Connect and for Custom Location|Pass|NA
21|AzureCloud|ARC|https://graph.microsoft.com/|Required when Azure RBAC is configured|Pass|NA
22|AzureCloud|ARC|https://graph.windows.net|Required when Azure RBAC is configured|Pass|NA
23|AzureCloud|ARC|https://eastus.obo.arc.azure.com:8084/|Container service for ARC Agent|Pass|NA
24|AzureCloud|ARC|https://dl.k8s.io|For Automatic Agent Upgrade|Pass|NA
25|AzureCloud|NFM|https://eastus-prod.mecdevice.azure.com|NFM Service|Pass|NA
26|AzureCloud|ASE|https://login.microsoftonline.com|Authentication Service - Microsoft Entra ID|Pass|NA
27|AzureCloud|ASE|https://pod01-edg1.eus.databoxedge.azure.com/|Azure Stack Edge Service|Pass|NA
28|AzureCloud|ASE|https://pod01-edg1.wus2.databoxedge.azure.com/|Azure Stack Edge Service|Pass|NA
29|AzureCloud|ASE|https://pod01-edg1.sea.databoxedge.azure.com/|Azure Stack Edge Service|Pass|NA
30|AzureCloud|ASE|https://pod01-edg1.we.databoxedge.azure.com/|Azure Stack Edge Service|Pass|NA
31|AzureCloud|ASE|https://euspod01edg1sbcnpu53n.servicebus.windows.net/|Azure Service Bus|Pass|NA
32|AzureCloud|ASE|https://wus2pod01edg1sbcnqh26z.servicebus.windows.net/|Azure Service Bus|Pass|NA
33|AzureCloud|ASE|https://seapod01edg1sbcnkw22o.servicebus.windows.net/|Azure Service Bus|Pass|NA
34|AzureCloud|ASE|https://wepod01edg1sbcnhk23j.servicebus.windows.net/|Azure Service Bus|Pass|NA
35|AzureCloud|ASE|https://azgnrelay-eastus-l1.servicebus.windows.net|Azure Service Bus|Pass|NA
36|AzureCloud|ASE|http://crl.microsoft.com/pki/|Certificate Revocation|Pass|NA
37|AzureCloud|ASE|http://www.microsoft.com/pki/|Certificate Revocation|Pass|NA
38|AzureCloud|ASE|https://seapod1edg1monsa01kw22o.table.core.windows.net|Azure Storage Accounts|Pass|NA
39|AzureCloud|ASE|https://seapod1edg1monsa02kw22o.table.core.windows.net|Azure Storage Accounts|Pass|NA
40|AzureCloud|ASE|https://seapod1edg1monsa03kw22o.table.core.windows.net|Azure Storage Accounts|Pass|NA
41|AzureCloud|ASE|https://euspod01edg1monsa01pu53n.table.core.windows.net|Azure Storage Accounts|Pass|NA
42|AzureCloud|ASE|https://euspod01edg1monsa02pu53n.table.core.windows.net|Azure Storage Accounts|Pass|NA
43|AzureCloud|ASE|https://euspod01edg1monsa03pu53n.table.core.windows.net|Azure Storage Accounts|Pass|NA
44|AzureCloud|ASE|https://wus2pod1edg1monsa01qh26z.table.core.windows.net|Azure Storage Accounts|Pass|NA
45|AzureCloud|ASE|https://wus2pod1edg1monsa02qh26z.table.core.windows.net|Azure Storage Accounts|Pass|NA
46|AzureCloud|ASE|https://wus2pod1edg1monsa03qh26z.table.core.windows.net|Azure Storage Accounts|Pass|NA
47|AzureCloud|ASE|https://wepod01edg1monsa01hk23j.table.core.windows.net|Azure Storage Accounts|Pass|NA
48|AzureCloud|ASE|https://wepod01edg1monsa02hk23j.table.core.windows.net|Azure Storage Accounts|Pass|NA
49|AzureCloud|ASE|https://wepod01edg1monsa03hk23j.table.core.windows.net|Azure Storage Accounts|Pass|NA
50|AzureCloud|ASE|https://management.azure.com/|Azure Management Service|Pass|NA
51|AzureCloud|ASE|https://management.core.windows.net|Azure Management Service|Pass|NA
52|AzureCloud|ASE|https://azureprofilerfrontdoor.cloudapp.net|Azure Traffic Manager|Fail|Unsuccessful web request
53|AzureCloud|ASE|https://azstrpprod.trafficmanager.net/|Azure Traffic Manager|Fail|Unsuccessful web request
54|AzureCloud|ASE|http://mcr.microsoft.com/v2/_catalog|Azure Container Registry|Pass|NA
55|AzureCloud|ASE|https://browser.events.data.microsoft.com/OneCollector/1.0/|Azure Telemetry Service|Pass|NA
56|AzureCloud|ASE|http://windowsupdate.microsoft.com|Microsoft Update Server|Pass|NA
57|AzureCloud|ASE|http://update.microsoft.com|Microsoft Update Server|Pass|NA
58|AzureCloud|ASE|https://update.microsoft.com|Microsoft Update Server|Pass|NA
59|AzureCloud|ASE|http://download.microsoft.com|Microsoft Update Server|Pass|NA
60|AzureCloud|ASE|https://download.microsoft.com|Microsoft Update Server|Pass|NA
61|AzureCloud|ASE|http://download.windowsupdate.com|Microsoft Update Server|Pass|NA
62|AzureCloud|ASE|http://wustat.windows.com|Microsoft Update Server|Fail|Domain name does not exist
63|AzureCloud|ASE|http://ntservicepack.microsoft.com|Microsoft Update Server|Pass|NA

