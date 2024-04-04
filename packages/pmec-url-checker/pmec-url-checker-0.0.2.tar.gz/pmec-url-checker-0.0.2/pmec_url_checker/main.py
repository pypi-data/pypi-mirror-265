# Copyright (c) Microsoft Corporation. All rights reserved.
# Highly Confidential Material
"""URL checker tool to validate the reqired URLs accessible for AP5GC orject which were added in Firewall rules added."""

from __future__ import print_function

import argparse
import logging
import os
import socket
import struct
import time

import urllib3

from pmec_url_checker.url_checker import UrlChecker

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
REPORT_FILE_DIR = os.path.expanduser("~")
REPORT_FILE_NAME = "url_checker_report.csv"
REPORT_FILE_PATH = os.path.join(REPORT_FILE_DIR, REPORT_FILE_NAME)


VERSION = "0.0.2"


def get_version() -> str:
    return (
        "URL Checker tool version: "
        + VERSION
        + "\n CopyRight (c) 2024 Microsoft Corporation. All rights reserved."
    )


def getNTPTime(hosts: list[str]):
    """Get the time from NTP Server."""
    port = 123
    buf = 1024
    msg = "\x1b" + 47 * "\0"

    for host in hosts:
        address = (host, port)

        # reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800  # 1970-01-01 00:00:00

        # connect to server
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(20)
        try:
            client.sendto(msg.encode("utf-8"), address)
            msg, address = client.recvfrom(buf)
        except socket.timeout:
            logging.debug(
                "FAIL: Timeout occured while connecting to NTP Server, check for other server endpoint"
            )
            continue
        except socket.error as e:
            logging.debug(
                "FAIL: Error occured while connecting to NTP Server: %s",
                e,
            )
            logging.debug("FAIL: check for other server endpoint.")
            continue
        else:
            logging.info("PASS: NTP Server is accessible.")
            client.close()
            t = struct.unpack("!12I", msg)[10]
            t -= TIME1970
            return time.ctime(t).replace("  ", " ")

    logging.info("FAIL: Unable to connect to NTP Server.")
    return None


def main() -> None:
    """Entry point for URL checker script."""

    parser = argparse.ArgumentParser(description="URL Checker tool for AP5GC")
    parser.add_argument(
        "-c",
        "--cloud",
        default="AzureCloud",
        metavar="<Azure Cloud type>",
        choices=[
            "AzureCloud",
            "AzureChinaCloud",
            "AzureUSGovernmentCloud",
            "AzureGermanCloud",
        ],
        help="Indicates the Azure environment. Required if the device is deployed to an environment other "
        "than the Azure public cloud (Azure Cloud). Supported values are [ AzureCloud | AzureChinaCloud | AzureUSGovernmentCloud | AzureGermanCloud ]",
    )
    parser.add_argument(
        "--custom-url",
        nargs="+",
        help="List ofs other URLs that you want to test HTTP access to.",
    )
    parser.add_argument(
        "-d",
        "--dns-server",
        required=True,
        nargs="+",
        metavar="<List of DNS Server>",
        help="IP addresses of the DNS servers (for example, your primary and secondary DNS servers) used for name resolution of URLs.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="<Output File Path>",
        default=REPORT_FILE_PATH,
        help="Dump the Result into file.",
    )
    parser.add_argument(
        "-r",
        "--region",
        type=str,
        default="eastus",
        metavar="<Region in small case without space>",
        help="Deployment Region ( default to eastus).",
    )
    parser.add_argument(
        "--skip-test",
        type=str,
        metavar="<Skip Test>",
        choices=[
            "ASE",
            "ARC",
            "NFM",
            "PMEC",
        ],
        nargs="+",
        help="skip checking URLs ( Supported values are [ASE, ARC, NFM, PMEC]).",
    )
    parser.add_argument(
        "-s",
        "--source-ip",
        type=str,
        metavar="<Source IP>",
        help="Source IP address to be used for querying the HTTP request.",
    )

    parser.add_argument(
        "-t",
        "--time-server",
        nargs="+",
        metavar="<List of NTP Server>",
        help="FQDN of one or more Network Time Protocol (NTP) servers used in ASE",
    )
    parser.add_argument(
        "-v",
        "--Verbose",
        action="count",
        default=0,
        help="Increase verbosity level",
    )

    parser.add_argument("--version", action="version", version=get_version())

    args = parser.parse_args()

    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

    if args.Verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.Verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.ERROR)

    is_ntp_server_accessible = []

    url_checker = UrlChecker(
        args.cloud,
        args.region if args.region else None,
        args.dns_server,
        args.source_ip if args.source_ip else None,
        args.custom_url if args.custom_url else None,
        args.skip_test if args.skip_test else None,
    )

    print("\nTesting the URL Endpoints.")

    # Now run the URL checker and check all the URLs presents in the URL DB class.
    url_checker.run()

    print("\n")

    # Now get the status of the URLs.
    status = url_checker.get_urls_status()
    for items in status:
        print("\tURL Endpoints for {}: {}".format(items[0], items[1]))

    # Now Dump the result into CSV file.
    url_checker.dump_result(args.output)

    print("\nTesting the NTP Server.")
    if args.time_server:
        logging.info("Checking the NTP Server")
        for time_server in args.time_server:
            resolved_ips = url_checker.get_time_server(time_server)
            if resolved_ips:
                received_time = getNTPTime(resolved_ips)
                if received_time is not None:
                    logging.debug("Time from NTP Server: %s", received_time)
                    is_ntp_server_accessible.append((time_server, True))
                else:
                    logging.error("Failed to get time from NTP Server.")
                    is_ntp_server_accessible.append((time_server, False))
            else:
                logging.error("Failed to resolve the NTP Server: %s", time_server)
                is_ntp_server_accessible.append((time_server, False))

    for items in is_ntp_server_accessible:
        print("\tNTP Server {}: {}".format(items[0], "PASS" if items[1] else "FAIL"))

    print("\nURL Checker completed successfully.")
    print(
        "To view the complete URL status in detail, View the Report at Location: {}".format(
            args.output
        )
    )


if __name__ == "__main__":
    main()
