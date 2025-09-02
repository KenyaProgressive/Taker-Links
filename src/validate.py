import ipaddress
from urllib.parse import urlparse

from logger import logger


def is_ip_address_valid(address: str) -> bool:
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        logger.warning("Got string is not a IPAddress")
        return False

def is_url_valid(address: str) -> bool:
    try:
        urlparse(address)
        return True
    except ValueError:
        logger.warning("Got string is not a URL")
        return False
