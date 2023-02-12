# Embedded-System-Smart-Flowerpot
Smart Flowerpot | Temperature &amp; Humidity Detection | Automatic Watering | App Remote Control | Automatic Base Rotation based on Sunlight Direction

## System Structure:

![alt text](https://github.com/Xintong-Zhan/Embedded-System-Smart-Flowerpot/blob/main/project_website/images/system.png)

The main components of the system include the smart flowerpot hardware and a cloud control system. Raspberry Pi is chosen as the hardware platform to monitor the plant with different sensors and to interact with the plant with various actuators, whereas the cloud control system analyzes the information received from the hardware with an algorithm, allowing the user to remotely control the product. The two main components communicate via Socket.


## Hardware:

<img src="https://github.com/Xintong-Zhan/Embedded-System-Smart-Flowerpot/blob/main/project_website/images/system.png", width = "10" ,height = "10">
The sensors in the hardware component include a DHT11 temperature humidity sensor and two TCS34725 light sensors. These sensors constantly monitor the temperature and humidity inside the pot and the light received by two opposite sides of the flowerpot and send the measured data to the cloud control platform.

Three different actuators are used in this project: an LCD screen, a buzzer, a motor, and a water pump. 

LCD screen: displays measurements.

Buzzer: alerts the user when the plant is under undesirable conditions.

Motor: rotates the plant to receive light evenly.

Water pump: pumps water from a container to water the plant.



## Software:
![alt text](https://github.com/Xintong-Zhan/Embedded-System-Smart-Flowerpot/blob/main/project_website/images/Software.png)
The software component consists of a server and an app. We implemented multithreading to create a sub-thread dedicated to socket communication with the app so that it will not congest the main control module. With multithreading, we allow the server to simultaneously receive data from sensors, send commands to actuators, and receive commands from the remote app.

It includes the following control logic of the entire system:

LCD screen displays the text “smart flowerpot” unless other commands are received.

When the temperature received from the temperature (°C) sensor exceeds 29, the buzzer is instantly enabled. The LCD screen displays the text “too hot!”.[1]
When humidity is below 20%, the water pump is instantly enabled.

When the difference in measurements from the two light sensors exceeds 200, the motor is instantly enabled (rotates the pot by 180°). Every other time the motor is triggered, it changes direction, so that the wires in the flowerpot do not get tangled.

When the server receives the string “rotate flower” from the app, the motor is instantly enabled. It functions in the same way as described in the previous bullet.

When the server receives the string “water flower” from the app, the water pump is instantly enabled.

When the server receives the string “show temperature” from the app, the LCD screen displays the current temperature measured by the temperature humidity sensor.

When the server receives the string “show humidity” from the app, the LCD screen displays the current humidity measured by the temperature humidity sensor.

We use Ngrok to perform intranet penetration and provide a public server IP for the server. The app would interact with the server by this public IP. The app uses speech recognition technology[3] to translate the spoken commands from the user to a string and sends the string to the server.

## 3D Printing Flowerpot:
Using Solidworks, we drew and 3D printed three separate parts of the form factor: the shell, the platform, and the pot.
![alt text](https://github.com/Xintong-Zhan/Embedded-System-Smart-Flowerpot/blob/main/project_website/images/assembly.png)
