"""
Support for ha auto ali dns
# Author:
    baby7
# Created:
    2021-11-23
"""
import sys
import logging
from homeassistant.const import (CONF_NAME)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
import requests
from .alidns import AliDNS

_Log = logging.getLogger(__name__)

DEFAULT_NAME = 'ha_auto_ali_dns'
ACCESS_KEY_ID = 'access_key_id'
ACCESS_KEY_SECRET = 'access_key_secret'
RECOED_ID = 'record_id'
TYPE = 'type'
RR = 'rr'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(ACCESS_KEY_ID): cv.string,
    vol.Required(ACCESS_KEY_SECRET): cv.string,
    vol.Required(RECOED_ID): cv.string,
    vol.Required(TYPE): cv.string,
    vol.Required(RR): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    access_key_id = config.get(ACCESS_KEY_ID)
    access_key_secret = config.get(ACCESS_KEY_SECRET)
    record_id = config.get(RECOED_ID)
    type = config.get(TYPE)
    rr = config.get(RR)
    sensor_name = config.get(CONF_NAME)
    add_devices([AutoAliDNS("ali_dns_" + sensor_name, access_key_id, access_key_secret, record_id, type, rr)])


def get_ip(i):
    try:
        ip_url = ""
        if i == 1:
            ip_url = "https://api.ipify.org"
        elif i == 2:
            ip_url = "https://api.ip.sb/ip"
        elif i == 3:
            ip_url = "http://ip.3322.net"
        elif i == 4:
            ip_url = "http://ip.qaros.com"
        elif i == 5:
            ip_url = "http://ident.me"
        else:
            ip_url = "http://icanhazip.com"
        return str(requests.get(url=ip_url, timeout=3).text).replace("\n", "").replace("\r", "")
    except requests.exceptions.RequestException as e:
        print(e)
    return None


class AutoAliDNS(Entity):
    """Representation of a ha auto ali dns"""

    access_key_id = str
    access_key_secret = str
    record_id = str
    type = str
    rr = str
    index = 1

    def __init__(self, sensor_name: str, access_key_id: str, access_key_secret: str, record_id: str, type: str,rr: str):
        self.attributes = {}
        self._state = None
        self._name = sensor_name
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.record_id = record_id
        self.type = type
        self.rr = rr

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """返回mdi图标."""
        return 'mdi:script'

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.attributes

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return ""

    def update(self):
        self.index += 1
        if self.index == 7:
            self.index = 1
        public_ip = get_ip(self.index)
        if public_ip is None or len(public_ip) > 15:
            print("获取公网IP超时或失败,等待下次重试")
            return
        self._state = public_ip
        try:
            dns_ip = AliDNS.get_dns_info(self.access_key_id, self.access_key_secret, self.record_id)
            if public_ip != dns_ip:
                AliDNS.main(self.access_key_id, self.access_key_secret, self.record_id, public_ip, self.type, self.rr)
                print("成功修改解析，记录为的" + self.record_id + "域名解析从" + str(dns_ip) + "修改为" + str(public_ip))
        except ConnectionError:
            print("记录为的" + self.record_id + "域名解析连接错误...")
        except:
            _Log.error("记录为的" + self.record_id + "域名解析发生为止错误...:", sys.exc_info()[0])
        finally:
            self._state = public_ip
