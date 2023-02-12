import temp_humid
import screen
import TCS34725
import TCS34725_2
import socket
import threading
import time
import buzzer
import pump
import motor

def get_host_ip():
	try:
	     s_for_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	     s_for_ip.connect(('8.8.8.8', 80))
	     ip = s_for_ip.getsockname()[0]
	finally:
	     s_for_ip.close()
	return ip

def get_light_1():
    light1=TCS34725.light_sensor1.get_value()
    return light1

def get_light_2():
    light2=TCS34725_2.light_sensor2.get_value()
    return light2

def create_socket(port):
    ip=get_host_ip() #Ip addr
    s = socket.socket()  # 创建 socket 对象
    s.bind((ip, port))  # 绑定端口
    print("Socket is listening!")
    s.listen(1)  # 等待客户端连接
    
    return s

def get_from_App():
    s=create_socket(80)
    global FLAG
    global rotate_FLAG
    while True:
        c,addr= s.accept()  # 建立客户端连接     
        tx_data="raspberry pi connected!"
        c.send(str.encode(tx_data))
        tx_response="HTTP/1.1 200 OK\r\n\r\n welcome!"
        c.send(str.encode(tx_response))
        rx_data=c.recv(1048).decode('utf-8')
        print(rx_data)
        begin=10
        for i in range(begin,len(rx_data)):
            if rx_data[i]==" ":
                end=i
                break
        info=rx_data[begin:end].replace("%20"," ")
        print(info)
        if info=="water flower":
            FLAG=1
        elif info =="show humidity":
            FLAG=2
        elif info =="show temperature":
            FLAG=3
        elif info =="rotate flower":
            FLAG=4
            rotate_FLAG=-rotate_FLAG
        else:
            FLAG=0
        time.sleep(2)

def start_buzzer():
    buzzer.main()

def get_temp_humid():
    temp,humid=temp_humid.dht11()
    return temp,humid

def draw_screen(x,y,text):
    screen.draw(x,y,text)

def start_pump():
    pump.main(3)

def start_motor(flag):
    motor.main(flag)

def detect_humid(humid):
    if humid>=50:
        print("Too wet!")
        draw_screen(0,20,"Too wet!")
    elif humid<=20 and humid>=0:
        print("Too dry!")
        draw_screen(0,20,"Too dry!")

def detect_temp(temp):
    global FLAG
    if temp>=28:
        print(temp)
        print(type(temp))
        print("Too hot!")
        draw_screen(0,20,"Too hot!")
        FLAG=5
    elif temp<=18 and temp>=0:
        print("Too cold!")    
        draw_screen(0,20,"Too cold!")

    elif FLAG==0:
        draw_screen(0,0,"Smart Flowerpot")


def detect_rotate(light1,light2):
    global FLAG
    global rotate_FLAG
    if abs(light1-light2)>=200:
        FLAG=4
        rotate_FLAG=-rotate_FLAG

def main():
    global rotate_FLAG
    global FLAG
    FLAG=0
    rotate_FLAG=-1
    t = threading.Thread(target=get_from_App)
    t.start()
    draw_screen(0,0,"Smart Flowerpot")
    while True:
        
        humid,temp=get_temp_humid()
        print("Humidity: "+str(humid))
        print("Temperature: "+str(temp))
        light1=get_light_1()
        light2=get_light_2()
        detect_temp(temp)
        detect_rotate(light1,light2)
        print("Light1: "+str(light1))
        print("Light2: "+str(light2))

        if FLAG==1:
            #water flower
            start_pump()
            FLAG=0
        elif FLAG==2:
            draw_screen(0,10,"Humid: "+str(humid)+"%")
            FLAG=0
        elif FLAG==3:
            draw_screen(0,10,"Temp: "+str(temp)+"C")
            FLAG=0
        elif FLAG==4:
            #rotate flower
            start_motor(rotate_FLAG)
            FLAG=0
        elif FLAG==5:
            start_buzzer()
            FLAG=0
        

        time.sleep(0.5)
if __name__ == "__main__":
    main()

    