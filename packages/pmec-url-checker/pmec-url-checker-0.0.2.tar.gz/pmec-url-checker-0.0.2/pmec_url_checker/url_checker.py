# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material
"""This module uses the dns server provided by the User to resolve the FQDN."""

import requests
from pmec_url_checker.dns_resolver import DnsResolver
from pmec_url_checker.url_db import URLDB
import logging
from typing import List, Optional
from urllib.parse import urlparse


class UrlChecker:
    """UrlChecker class to validate list of URLs are accessible or not."""

    def __init__(
        self,
        cloud: str,
        region: Optional[str],  # pylint: disable=E1136
        dnsserver: list,
        source_ip: Optional[str],  # pylint: disable=E1136
        custom_url: Optional[List[str]],  # pylint: disable=E1136
        skiptest: Optional[str],  # pylint: disable=E1136
    ) -> None:
        self.source_ip = source_ip
        self.cloud = cloud
        self.region = region
        self.dns_resolver = DnsResolver(dnsserver, source_ip)
        self._url_db = URLDB()
        self._url_db.load(cloud, region, custom_url, skiptest)

    def run(self) -> None:
        """Check the list of URLs are accessible or not."""
        # Retrieve the List from URL DB
        data = self._url_db.retrieve()
        logging.info("----------------------------------------------------")
        logging.info("Total URLs to be checked: %s", len(data))
        logging.info("----------------------------------------------------")
        for _, row in data.iterrows():
            logging.info("Checking the URL accessibility: %s", row["URL"])

            result, reason = self._check_url(row["URL"])
            if result:
                row["Status"] = "Pass"
            else:
                row["Status"] = "Fail"
                row["Reason"] = reason

            logging.info("----------------------------------------------------")

    def _check_url(self, url: str) -> tuple[bool, Optional[str]]:
        """Check the URL is accessible or not."""
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        result, answers = self.dns_resolver.resolve(hostname)
        if result:
            for resolved_ip in answers:
                if parsed_url.port is not None:
                    resolved_url = parsed_url._replace(
                        netloc=resolved_ip.address + ":" + str(parsed_url.port)
                    )
                else:
                    resolved_url = parsed_url._replace(netloc=resolved_ip.address)

                if self._trigger_http_request(resolved_url.geturl()):
                    logging.info("PASS: URL is accessible: %s", resolved_url.geturl())
                    return True, None
            return False, "Unsuccessful web request"
        else:
            logging.error(
                "Failed to resolve the FQDN: %s with error: %s", hostname, answers
            )
            return False, answers

    def _trigger_http_request(self, url: str) -> bool:
        """Trigger HTTP request to URL provided."""
        try:
            logging.debug("Testing Webrequest to: %s  Source: %s", url, self.source_ip)

            webrequest = self._create_session()  # Create TCP session
            r = webrequest.get(url, allow_redirects=False, timeout=10, verify=False)
            logging.debug("HTTP Status Code: %d", r.status_code)

            # any code between 100-599 is considered a success since it indicates that the
            # request is passed by firewall except the Timeout exception.
            if r.status_code not in range(100, 599):
                msg = (
                    "FAIL: Webrequest using Source IP {} received invalid status code for "
                    "{} and it is not within the acceptable range of 100-599. StatusCode={}".format(
                        self.source_ip, url, r.status_code
                    )
                )
                logging.debug(msg)
            else:
                msg = "PASS: Successfull webrequest using Source IP {} to: {}".format(
                    self.source_ip, url
                )
                logging.debug(msg)
                return True
        except requests.exceptions.RequestException as e:
            msg = "FAIL: Unsuccessfull webrequest using Source IP {} to: {}: Exception: {}".format(
                self.source_ip, url, str(e)
            )
            logging.debug(msg)
        return False

    def _create_session(self) -> requests.Session:
        """
        Create `Session` which will bind to the specified local address
        rather than auto-selecting it.
        # usage example:
        s = _create_session('100.64.246.10')
        s.get('https://login.microsoftonline.com')
        """
        session = requests.Session()
        for prefix in ("http://", "https://"):
            session.get_adapter(prefix).init_poolmanager(
                # those are default values from HTTPAdapter's constructor
                connections=requests.adapters.DEFAULT_POOLSIZE,
                maxsize=requests.adapters.DEFAULT_POOLSIZE,
                # This should be a tuple of (address, port). Port 0 means auto-selection.
                source_address=(self.source_ip if self.source_ip else "0.0.0.0", 0),
            )
        return session

    def dump_result(self, output: str) -> None:
        """Dump the result into file."""
        data = self._url_db.retrieve()
        data.to_csv(output)

    def get_urls_status(self) -> list[(str, str)]:
        """Get the status of all the URLs."""
        return self._url_db.get_urls_status()

    def get_time_server(self, time_server: str) -> Optional[List[str]]:
        """Get the IP address of Time Server."""
        result, answers = self.dns_resolver.resolve(time_server)
        if result:
            return [resolved_ip.address for resolved_ip in answers]
        else:
            return None
