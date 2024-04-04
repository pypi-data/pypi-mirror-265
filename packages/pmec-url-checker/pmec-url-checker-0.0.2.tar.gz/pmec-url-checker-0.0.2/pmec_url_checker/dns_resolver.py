# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material
"""This module uses the dns server provided by the User to resolve the FQDN."""
import logging
from typing import Optional, Union

import dns.exception
import dns.resolver


class DnsResolver:
    """DnsResolver class to resolve the FQDN using the provided DNS server."""

    def __init__(
        self, dnsserver: list, source_ip: Optional[str]  # pylint: disable=E1136
    ) -> None:
        self.dnsserver = dnsserver
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = self.dnsserver
        self.source_ip = source_ip

    def resolve(
        self, hostname: str
    ) -> tuple[bool, Union[list, str]]:  # pylint: disable=E1136
        logging.info(
            "Resolving the FQDN (%s) using the provided DNS server\n\n", hostname
        )
        failure_reason = ""
        try:
            answers = self.resolver.query(hostname, "A", source=self.source_ip)
            logging.debug("Received DNS Response:")
            logging.debug("Server:\t %s", answers.nameserver)
            logging.debug("Address:\t %s#%s\n", answers.nameserver, answers.port)
            logging.debug("Source Ip:")
            logging.debug("Answers:")
            for data in answers:
                logging.debug("\tIP:  %s\tType:  %s", data.address, data.rdtype)

            if len(answers) != 0:
                return (True, answers)
        except dns.resolver.NoAnswer as e:
            logging.error("No Answer received for the Query: %s", e)
            failure_reason = "No Answer received"
        except dns.resolver.NXDOMAIN as e:
            logging.error("The Domain name does not exist: %s", e)
            failure_reason = "Domain name does not exist"
        except dns.resolver.YXDOMAIN as e:
            logging.error("The Domain name is too long: %s", e)
            failure_reason = "Domain name is too long"
        except dns.resolver.NoNameservers as e:
            logging.error("No Name Servers are found: %s", e)
            failure_reason = "No Name Servers are found"
        except dns.resolver.LifetimeTimeout as e:
            logging.error("Timeout occured while resolving the Domain name: %s", e)
            failure_reason = "Timeout"
        except dns.exception.DNSException as e:
            logging.error("Exception occured while resolving the FQDN: %s", e)
            failure_reason = "Unexpected Error"
        return (False, failure_reason)
