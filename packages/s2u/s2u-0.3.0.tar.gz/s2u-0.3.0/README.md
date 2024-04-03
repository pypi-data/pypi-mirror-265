This is a kind of bridge that exchanges serial streams and UDP packets for xkit.

```sh
[Device A] <---SLIP data---> [(serial) <---Exchange Serial2UDP---> (network)] <---UDP packet---> [Device B]
                             |--------------------s2u-----------------------| |------local or remote------|
```

### History
- V0.3.0
  - Supports SLIP serial data
  - Supports UDP and Multicast

### Install
```sh
pip install s2u
```

### Dependencies
- pyserial
- genlib

### Run

**Window**
```sh
s2u --sport=com1
```
**linux**
```sh
s2u --sport=/dev/stty1
```

**options**  
--sport=\<serial port\>  
--baud=\<baud\>     (default 115200)  
--ip=\<server ip\>  (default 127.0.0.1)  
--mcast  
--group=\<group\>   (default 239.8.7.6)  
--iport=\<port\>    (default 7321)  
--log=\<stream | file\>  
