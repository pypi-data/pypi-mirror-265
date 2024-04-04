# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material
"""This module stores the list of URLs needed to be validated."""


from typing import List, Optional

import pandas as pd


RegionAbbreviation = {
    "australiacentral": "acl",
    "australiacentral2": "acl2",
    "australiaeast": "ae",
    "australiasoutheast": "ase",
    "brazilsouth": "brs",
    "brazilsoutheast": "bse",
    "centraluseuap": "ccy",
    "canadacentral": "cnc",
    "canadaeast": "cne",
    "centralus": "cus",
    "eastasia": "ea",
    "eastus2euap": "ecy",
    "eastus": "eus",
    "eastus2": "eus2",
    "francecentral": "frc",
    "francesouth": "frs",
    "germanynorth": "gn",
    "germanywestcentral": "gwc",
    "centralindia": "inc",
    "southindia": "ins",
    "westindia": "inw",
    "italynorth": "itn",
    "japaneast": "jpe",
    "japanwest": "jpw",
    "jioindiacentral": "jic",
    "jioindiawest": "jiw",
    "koreacentral": "krc",
    "koreasouth": "krs",
    "northcentralus": "ncus",
    "northeurope": "ne",
    "norwayeast": "nwe",
    "norwaywest": "nww",
    "qatarcentral": "qac",
    "southafricanorth": "san",
    "southafricawest": "saw",
    "southcentralus": "scus",
    "swedencentral": "sdc",
    "swedensouth": "sds",
    "southeastasia": "sea",
    "switzerlandnorth": "szn",
    "switzerlandwest": "szw",
    "uaecentral": "uac",
    "uaenorth": "uan",
    "uksouth": "uks",
    "ukwest": "ukw",
    "westcentralus": "wcus",
    "westeurope": "we",
    "westus": "wus",
    "westus2": "wus2",
    "westus3": "wus3",
    "usdodcentral": "udc",
    "usdodeast": "ude",
    "usgovarizona": "uga",
    "usgoviowa": "ugi",
    "usgovtexas": "ugt",
    "usgovvirginia": "ugv",
    "usnateast": "exe",
    "usnatwest": "exw",
    "usseceast": "rxe",
    "ussecwest": "rxw",
    "chinanorth": "bjb",
    "chinanorth2": "bjb2",
    "chinanorth3": "bjb3",
    "chinaeast": "sha",
    "chinaeast2": "sha2",
    "chinaeast3": "sha3",
    "germanycentral": "gec",
    "germanynortheast": "gne",
}


class URLDB:
    """URL DB class to store the list of URLs needed to be validated."""

    def __init__(self) -> None:
        self.cloud = ""
        self.region = ""
        self.__data = pd.DataFrame(
            columns=[
                "Cloud Environment",
                "Layer",
                "URL",
                "Service",
                "Status",
                "Reason",
            ]
        )

    def load(
        self,
        cloud: str,
        region: Optional[str],  # pylint: disable=E1136
        custom_url: Optional[List[str]],  # pylint: disable=E1136
        skiptest: Optional[str],  # pylint: disable=E1136
    ) -> None:
        """Load the list of URLs from the file."""
        self.cloud = cloud
        self.region = region.replace(" ", "").lower() if region else ""

        # PMEc URLs
        if skiptest != "PMEC":
            self.load_pmec_specific_urls()

        # ARC URL
        if skiptest != "ARC":
            self.load_arc_specific_urls()

        # NFM URLs
        if skiptest != "NFM":
            self.load_nfm_specific_urls()

        # ASE URLs
        if skiptest != "ASE":
            self.load_ase_specific_urls()

        if custom_url and len(custom_url) > 0:
            self.load_custom_urls(custom_url)

    def load_pmec_specific_urls(self) -> None:
        """Load the AP5GC specific URLs."""

        # URLs for Docker Registery
        self.__data = pd.concat(
            [
                self.__data,
                pd.DataFrame(
                    {
                        "Cloud Environment": self.cloud,
                        "Layer": "PMEC",
                        "URL": [
                            "https://privatemecprivatemecartifactstore4ab6cc42d9.azurecr.io/v2/_catalog",
                            "https://privatemecdevpublisherprivatemecdevartifactstore1c.azurecr.io/v2/_catalog",
                            "https://privatemecdevpublishereastus2euapprivatea803a14a92.azurecr.io/v2/_catalog",
                            "https://privatemecdevpublishercentraluseuappriva6b3529cad4.azurecr.io/v2/_catalog",
                            "https://privatemeceastus2euapprivatemecartifactsf14e732aab.azurecr.io/v2/_catalog",
                            "https://privatemeccentraluseuapprivatemecartifac166168b140.azurecr.io/v2/_catalog",
                            "https://pcmeprodeastusacr.azurecr.io/v2/_catalog",  # For PCME pod
                        ],
                        "Service": "Azure Container Registry",
                        "Status": "Not Tested",
                        "Reason": "NA",
                    },
                ),
            ],
            ignore_index=True,
        )

        # URLs for  Geneva Monitoring and Telemetry service
        self.__data = pd.concat(
            [
                self.__data,
                pd.DataFrame(
                    {
                        "Cloud Environment": self.cloud,
                        "Layer": "PMEC",
                        "URL": [
                            "https://global.prod.microsoftmetrics.com/",
                            "https://global.int.microsoftmetrics.com/",
                            "https://global.ppe.microsoftmetrics.com/",
                            "https://prod.hot.ingestion.msftcloudes.com/",
                        ],
                        "Service": "Monitoring and telemetry",
                        "Status": "Not Tested",
                        "Reason": "NA",
                    }
                ),
            ],
            ignore_index=True,
        )

    def load_ase_specific_urls(self) -> None:
        """Load the ASE specific URLs."""

        if self.cloud.lower() == "azurecloud":
            # URLs for service Authentication Service - Microsoft Entra ID
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://login.microsoftonline.com",
                            ],
                            "Service": "Authentication Service - Microsoft Entra ID",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://pod01-edg1.eus.databoxedge.azure.com/",
                                "https://pod01-edg1.wus2.databoxedge.azure.com/",
                                "https://pod01-edg1.sea.databoxedge.azure.com/",
                                "https://pod01-edg1.we.databoxedge.azure.com/",
                            ],
                            "Service": "Azure Stack Edge Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://euspod01edg1sbcnpu53n.servicebus.windows.net/",
                                "https://wus2pod01edg1sbcnqh26z.servicebus.windows.net/",
                                "https://seapod01edg1sbcnkw22o.servicebus.windows.net/",
                                "https://wepod01edg1sbcnhk23j.servicebus.windows.net/",
                                "https://azgnrelay-eastus-l1.servicebus.windows.net",
                            ],
                            "Service": "Azure Service Bus",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://crl.microsoft.com/pki/",  # DevSkim: ignore DS137138
                                "http://www.microsoft.com/pki/",  # DevSkim: ignore DS137138
                            ],
                            "Service": "Certificate Revocation",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://seapod1edg1monsa01kw22o.table.core.windows.net",
                                "https://seapod1edg1monsa02kw22o.table.core.windows.net",
                                "https://seapod1edg1monsa03kw22o.table.core.windows.net",
                                "https://euspod01edg1monsa01pu53n.table.core.windows.net",
                                "https://euspod01edg1monsa02pu53n.table.core.windows.net",
                                "https://euspod01edg1monsa03pu53n.table.core.windows.net",
                                "https://wus2pod1edg1monsa01qh26z.table.core.windows.net",
                                "https://wus2pod1edg1monsa02qh26z.table.core.windows.net",
                                "https://wus2pod1edg1monsa03qh26z.table.core.windows.net",
                                "https://wepod01edg1monsa01hk23j.table.core.windows.net",
                                "https://wepod01edg1monsa02hk23j.table.core.windows.net",
                                "https://wepod01edg1monsa03hk23j.table.core.windows.net",
                                # "http://*.msftncsi.com", # Use absolute URL here
                            ],
                            "Service": "Azure Storage Accounts",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://management.azure.com/",
                                "https://management.core.windows.net",
                            ],
                            "Service": "Azure Management Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://azureprofilerfrontdoor.cloudapp.net",
                                "https://azstrpprod.trafficmanager.net/",
                            ],
                            "Service": "Azure Traffic Manager",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://mcr.microsoft.com/v2/_catalog",  # DevSkim: ignore DS137138
                            ],
                            "Service": "Azure Container Registry",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://browser.events.data.microsoft.com/OneCollector/1.0/",
                            ],
                            "Service": "Azure Telemetry Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://windowsupdate.microsoft.com",  # DevSkim: ignore DS137138
                                "http://update.microsoft.com",  # DevSkim: ignore DS137138
                                "https://update.microsoft.com",
                                "http://download.microsoft.com",  # DevSkim: ignore DS137138
                                "https://download.microsoft.com",
                                "http://download.windowsupdate.com",  # DevSkim: ignore DS137138
                                "http://wustat.windows.com",  # DevSkim: ignore DS137138
                                "http://ntservicepack.microsoft.com",  # DevSkim: ignore DS137138
                                # "http://*.windowsupdate.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.windowsupdate.microsoft.com",  # Use absolute URL here
                                # "http://*.update.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.update.microsoft.com",  # Use absolute URL here
                                # "http://*.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.download.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.ws.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.ws.microsoft.com",  # Use absolute URL here
                                # "http://*.mp.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                            ],
                            "Service": "Microsoft Update Server",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                ],
                ignore_index=True,
            )

        elif self.cloud.lower() == "azureusgovernmentcloud":
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://management.usgovcloudapi.net",
                            ],
                            "Service": "Azure Management Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://crl.microsoft.com/pki/",  # DevSkim: ignore DS137138
                                "http://www.microsoft.com/pki/",  # DevSkim: ignore DS137138
                            ],
                            "Service": "Certificate Revocation",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://login.microsoftonline.us",
                            ],
                            "Service": "Authentication Service - Microsoft Entra ID",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://pod01-edg1.ugv.databoxedge.azure.us/",
                            ],
                            "Service": "Azure Stack Edge Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://ugvpod1edg1monsa01hx7pv.table.core.usgovcloudapi.net",
                                "https://ugvpod1edg1monsa02hx7pv.table.core.usgovcloudapi.net",
                                "https://ugvpod1edg1monsa03hx7pv.table.core.usgovcloudapi.net",
                            ],
                            "Service": "Azure Storage Accounts",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://ugvpod01edg1sbcnhx7pv.servicebus.usgovcloudapi.net/",
                                "https://azgns-usgovvirginia-fairfax-1p-public.servicebus.usgovcloudapi.net",
                            ],
                            "Service": "Azure Service Bus",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://crl.microsoft.com/pki/",  # DevSkim: ignore DS137138
                                "http://www.microsoft.com/pki/",  # DevSkim: ignore DS137138
                            ],
                            "Service": "Certificate Revocation",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://windowsupdate.microsoft.com",  # DevSkim: ignore DS137138
                                "http://update.microsoft.com",  # DevSkim: ignore DS137138
                                "https://update.microsoft.com",
                                "http://download.microsoft.com",  # DevSkim: ignore DS137138
                                "https://download.microsoft.com",
                                "http://download.windowsupdate.com",  # DevSkim: ignore DS137138
                                "http://wustat.windows.com",  # DevSkim: ignore DS137138
                                "http://ntservicepack.microsoft.com",  # DevSkim: ignore DS137138
                                # "http://*.windowsupdate.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.windowsupdate.microsoft.com",  # Use absolute URL here
                                # "http://*.update.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.update.microsoft.com",  # Use absolute URL here
                                # "http://*.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.download.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.ws.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.ws.microsoft.com",  # Use absolute URL here
                                # "http://*.mp.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                            ],
                            "Service": "Microsoft Update Server",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://browser.events.data.microsoft.com/OneCollector/1.0/",
                            ],
                            "Service": "Azure Telemetry Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://mcr.microsoft.com/v2/_catalog",  # DevSkim: ignore DS137138
                            ],
                            "Service": "Azure Container Registry",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://azstrpffprod.usgovtrafficmanager.net/",
                            ],
                            "Service": "Remote Management",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://browser.events.data.microsoft.com/OneCollector/1.0/",
                            ],
                            "Service": "Azure Telemetry Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                ],
                ignore_index=True,
            )

        elif self.cloud.lower() == "azurechinacloud":
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://management.chinacloudapi.cn",
                            ],
                            "Service": "Azure Management Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://login.chinacloudapi.cn",
                            ],
                            "Service": "Authentication Service - Microsoft Entra ID",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://windowsupdate.microsoft.com",  # DevSkim: ignore DS137138
                                "http://update.microsoft.com",  # DevSkim: ignore DS137138
                                "https://update.microsoft.com",
                                "http://download.microsoft.com",  # DevSkim: ignore DS137138
                                "https://download.microsoft.com",
                                "http://download.windowsupdate.com",  # DevSkim: ignore DS137138
                                "http://wustat.windows.com",  # DevSkim: ignore DS137138
                                "http://ntservicepack.microsoft.com",  # DevSkim: ignore DS137138
                                # "http://*.windowsupdate.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.windowsupdate.microsoft.com",  # Use absolute URL here
                                # "http://*.update.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.update.microsoft.com",  # Use absolute URL here
                                # "http://*.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.download.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.ws.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.ws.microsoft.com",  # Use absolute URL here
                                # "http://*.mp.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                            ],
                            "Service": "Microsoft Update Server",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                ],
                ignore_index=True,
            )
        elif self.cloud.lower() == "azuregermancloud":
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://management.microsoftazure.de",
                                "https://management.core.cloudapi.de",
                            ],
                            "Service": "Azure Management Service",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "https://login.microsoftonline.de",
                            ],
                            "Service": "Authentication Service - Microsoft Entra ID",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ASE",
                            "URL": [
                                "http://windowsupdate.microsoft.com",  # DevSkim: ignore DS137138
                                "http://update.microsoft.com",  # DevSkim: ignore DS137138
                                "https://update.microsoft.com",
                                "http://download.microsoft.com",  # DevSkim: ignore DS137138
                                "https://download.microsoft.com",
                                "http://download.windowsupdate.com",  # DevSkim: ignore DS137138
                                "http://wustat.windows.com",  # DevSkim: ignore DS137138
                                "http://ntservicepack.microsoft.com",  # DevSkim: ignore DS137138
                                # "http://*.windowsupdate.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.windowsupdate.microsoft.com",  # Use absolute URL here
                                # "http://*.update.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.update.microsoft.com",  # Use absolute URL here
                                # "http://*.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.download.windowsupdate.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "http://*.ws.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                                # "https://*.ws.microsoft.com",  # Use absolute URL here
                                # "http://*.mp.microsoft.com",  # Use absolute URL here # DevSkim: ignore DS137138
                            ],
                            "Service": "Microsoft Update Server",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        }
                    ),
                ],
                ignore_index=True,
            )

    def load_nfm_specific_urls(self) -> None:
        """Load the NFM specific URLs."""
        # URLs for Geneva Monitoring and Telemetry service
        self.__data = pd.concat(
            [
                self.__data,
                pd.DataFrame(
                    {
                        "Cloud Environment": self.cloud,
                        "Layer": "NFM",
                        "URL": [
                            "https://" + self.region + "-prod.mecdevice.azure.com",
                        ],
                        "Service": "NFM Service",
                        "Status": "Not Tested",
                        "Reason": "NA",
                    }
                ),
            ],
            ignore_index=True,
        )

    def load_arc_specific_urls(self) -> None:
        """Load the ARC specific URLs."""
        if self.cloud.lower() == "azurecloud":
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://"
                                + self.region
                                + ".dp.kubernetesconfiguration.azure.com",
                            ],
                            "Service": "Data Plane Endpoint",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://login.windows.net",
                                "https://" + self.region + ".login.microsoft.net",
                                "https://" + self.region + ".login.microsoft.com",
                            ],
                            "Service": "To Update ARM tokens",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://"
                                + self.region
                                + ".data.mcr.microsoft.com/v2/_catalog",
                            ],
                            "Service": "Container service for ARC Agent",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://gbl.his.arc.azure.com",
                                "https://"
                                + RegionAbbreviation[self.region]
                                + ".his.arc.azure.com",
                            ],
                            "Service": "System Assigned Managed Identity",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://k8connecthelm.azureedge.net",
                                "https://guestnotificationservice.azure.com",
                                "https://sts.windows.net",
                            ],
                            "Service": "For Cluster Connect and for Custom Location",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://graph.microsoft.com/",
                                "https://graph.windows.net",
                            ],
                            "Service": "Required when Azure RBAC is configured",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://" + self.region + ".obo.arc.azure.com:8084/",
                            ],
                            "Service": "Container service for ARC Agent",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://dl.k8s.io",
                            ],
                            "Service": "For Automatic Agent Upgrade",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                ],
                ignore_index=True,
            )
        elif self.cloud.lower() == "azureusgovernmentcloud":
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://"
                                + self.region
                                + ".dp.kubernetesconfiguration.azure.us",
                            ],
                            "Service": "Data Plane Endpoint",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://" + self.region + ".login.microsoftonline.us",
                            ],
                            "Service": "To Update ARM tokens",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://"
                                + self.region
                                + ".data.mcr.microsoft.com/v2/_catalog",
                            ],
                            "Service": "Container service for ARC Agent",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://gbl.his.arc.azure.com",
                                "https://usgv.his.arc.azure.us",
                            ],
                            "Service": "System Assigned Managed Identity",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://k8connecthelm.azureedge.net",
                                "https://guestnotificationservice.azure.us",
                                "https://sts.windows.net",
                                "https://k8sconnectcsp.azureedge.net",
                            ],
                            "Service": "For Cluster Connect and for Custom Location",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://graph.microsoft.com/",
                                "https://graph.windows.net",
                            ],
                            "Service": "Required when Azure RBAC is configured",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://usgovvirginia.obo.arc.azure.us:8084/",
                            ],
                            "Service": "Cluster Connect",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://dl.k8s.io",
                            ],
                            "Service": "For Automatic Agent Upgrade",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                ],
                ignore_index=True,
            )

        elif self.cloud.lower() == "azurechinacloud":
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://"
                                + self.region
                                + "dp.kubernetesconfiguration.azure.cn",
                            ],
                            "Service": "Data Plane Endpoint",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://" + self.region + ".login.chinacloudapi.cn",
                                "https://login.partner.microsoftonline.cn",
                            ],
                            "Service": "To Update ARM tokens",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://mcr.azk8s.cn/v2/_catalog",
                            ],
                            "Service": "Container service for ARC Agent",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://gbl.his.arc.azure.cn",
                                "https://sha.his.arc.azure.cn",
                            ],
                            "Service": "System Assigned Managed Identity",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://k8connecthelm.azureedge.net",
                                "https://guestnotificationservice.azure.cn",
                                "https://sts.chinacloudapi.cn",
                                "https://k8sconnectcsp.azureedge.net",
                            ],
                            "Service": "For Cluster Connect and for Custom Location",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://graph.chinacloudapi.cn",
                            ],
                            "Service": "Required when Azure RBAC is configured",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://" + self.region + ".obo.arc.azure.cn:8084/",
                            ],
                            "Service": "Cluster Connect",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://dl.k8s.io",
                            ],
                            "Service": "For Automatic Agent Upgrade",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://quay.azk8s.cn",
                                "https://registryk8s.azk8s.cn",
                                "https://k8sgcr.azk8s.cn",
                                "https://usgcr.azk8s.cn",
                                "https://dockerhub.azk8s.cn",
                            ],
                            "Service": "Container Registry for proxy server",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                ],
                ignore_index=True,
            )
        elif self.cloud.lower() == "azuregermancloud":
            self.__data = pd.concat(
                [
                    self.__data,
                    pd.DataFrame(
                        {
                            "Cloud Environment": self.cloud,
                            "Layer": "ARC",
                            "URL": [
                                "https://graph.cloudapi.de",
                            ],
                            "Service": "Required when Azure RBAC is configured",
                            "Status": "Not Tested",
                            "Reason": "NA",
                        },
                    ),
                ],
                ignore_index=True,
            )

    def load_custom_urls(self, urls: List[str]) -> None:
        """Load custom URLs provided by User."""

        # URLs for Microsoft Update Server
        self.__data = pd.concat(
            [
                self.__data,
                pd.DataFrame(
                    {
                        "Cloud Environment": self.cloud,
                        "Layer": "Custom URL",
                        "URL": urls,
                        "Service": "NA",
                        "Status": "Not Tested",
                        "Reason": "NA",
                    },
                ),
            ],
            ignore_index=True,
        )

    def retrieve(self) -> pd.DataFrame:
        """Retrieve the list of URLs."""
        return self.__data

    def get_urls_status(self) -> list[(str, str)]:
        """Retrieve the list of URLs with status."""

        status: list = []

        for layer in ["ASE", "ARC", "NFM", "PMEC"]:
            urls = self.__data[self.__data["Layer"] == layer]
            if urls.empty:
                status.append((layer, "Not Tested"))
            else:
                status_count = urls["Status"].value_counts()
                if "Fail" not in status_count:
                    status.append((layer, "Pass"))
                elif "Pass" not in status_count:
                    status.append((layer, "Fail"))
                else:
                    status.append((layer, "Partially Pass"))
        return status
