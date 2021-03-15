# Video Test Program.

#### Introduction

This project is aim to test different video/Image processing, such as target detection, image encode/decode for data transfer.

##### Test_case 1: Use Iperf3 to test the network throughputs

link:  https://www.tecmint.com/test-network-throughput-in-linux/

Server side:  $ iperf3 -s

Client side: $ iperf3 -c 173.31.123.202



------

##### Test_case 2: Camera Echo Test Program

##### 2.1 Introduction

This program will create a camera/video viewer which used to test the image/data transfer latency between 2 nodes in a network. It will display the camera view/video in one window the send the data to the other side of the network. The other side <camEchoClient.py> will echo send the data back, then the sent back data will show on another window.

###### Program work flow:

![](doc/img/testCase7.gif)

###### Program user interface view:

![](doc/img/echo_ui_view.png)

##### 2.2 Program Setup

###### Development Environment

> Python 3.7.4

###### Additional Lib Need

Camera server side: Opencv: https://pypi.org/project/opencv-python/

```
pip install opencv-python
```

###### File Structure

| Server side         | Client Side      |
| ------------------- | ---------------- |
| camEchoServer.py    | camEchoClient.py |
| udpCpom.py          | udpCpom.py       |
| camServerConfig.txt |                  |
| test.mp4            |                  |

###### Program File List 

| Program File        | Execution Env | Description                                                  |
| ------------------- | ------------- | ------------------------------------------------------------ |
| camEchoClient.py    | python3.7     | This module will create UDP echo server program which will send back the data back to the source on port 5005. |
| camEchoServer.py    | python3.7     | This module will create a camera/video viewer which used to test the image/data transfer latency between 2 nodes in a network. It will display the camera view/video in one window the send the data to the other side of the network. |
| udpCom.py           | python3.7     | This module will provide a UDP client and server communication API. |
| udpComTest.py       | python3.7     | This module will provide a muti-thread test case program to test  the UDP communication modules by using port 5005. |
| camServerConfig.txt |               | The configuration file used to set the camEchoClient ipaddress, video frame rate and other parameters. |
| test.mp4            |               | H264 video used to test the video data transfer.             |



##### 2.3 Program Usage

Run the Program on Client machine(The client machine needs to run first): 

```
python3 camEchoClient.py
```

Run the Program on server machine(The client machine needs to run first): 

```
1. Set the test mode flag [TEST_MD]in camEchoServer.py line 29: 
True - use pre-saved video
False - capture from camera.
2. Change the IP addres in camServerConfig.txt to the client machine's IP and adjust the sending frame rate.
3. python3 camEchoServer.py
```



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 15/03/2021

