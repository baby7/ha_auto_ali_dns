# ha_auto_ali_dns

Homeassistant的阿里云域名DDNS插件

配置文件:
```yml
sensor:
  - platform: ha_auto_ali_dns
    access_key_id: xxxxxxxxxxxxx
    access_key_secret: xxxxxxxxxxxxxxxx
    record_id: xxxxxxxxxxxxx
    type: A
    rr: xxxxxx
```
