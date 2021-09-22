# GPS-denied_positioning
This project is aim to position the drone under GPS-denied environment
## initialize
Check whether broker ip is available
\anchor\transferGps.py line 49
```python
    client.connect("192.168.0.107", 1883, 60)
```

\tag\readGps.py line 84
```python 
    client.connect("192.168.0.106", 1883, 60)
```
## anchor
check comport
```python 
comPort = '/dev/ttyUSB0'
```
check anchor number
```python 
            mqtt_client.publish('gps/a0',data)

```
run transferGps.py

## tag
run main
specify UWB port
