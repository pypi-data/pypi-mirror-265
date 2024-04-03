This is an IMU quaternion data visualization tool for xkit.

### History
- V0.3.0
  - Implementing 3D visualization with OpenGL
  - STL file included(jet.stl)
  - UDPServer or MulticastReceiver

### Install
```sh
pip install quat
```

### Dependencies
- PySide6
- PyOpenGL
- pyqtgraph
- numpy-stl
- genlib


### Running
**UDP Server (port 7321)**
```sh
quat
```
**MulticastReceiver (group 239.8.7.6, port 7321)**
```sh
quat --mcast
```
**etc**  
--group=\<group\>  
--iport=\<port\>  
--log=\<stream | file>

### Client Implementations
- UDPClient or MulticastSender

**quaternion data format**
  ```sh
  w, x, y, z
  ```

**Example**
  ```python
  import time
  from genlib.upd import UDPClient
  from pop.ext import IMU

  imu = IMU()
  udp = UDPClient()
  
  QUAT_IP = '192.168.0.100'
  QUAT_PORT = 7321

  while True:
      w, x, y, z = imu.read(IMU.QUATERNION)
      udp.sendTo(f"{w}, {x}, {y}, {z}".encode(), (QUAT_IP, QUAT_PORT))
      time.sleep(20/1000)  
  ```