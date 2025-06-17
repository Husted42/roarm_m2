# roarm_m2
### Pre-requisites
 1. Create python env and download requirments file

### Roboarm setup
 1. Connect arm to internet `{"T":402,"ssid":"RoArm-M2","password":"12345678"}`

 ### raspberry pi
    1. Setup static ip adress at 192.168.0.1
    1. Connet to raspberry `ssh username@your_pi_ip_address`
    1. Find the port used to connect to robarm: In `/dev/` search for USB `ls ttyUSB`. In our case it's `ttyUSB0`