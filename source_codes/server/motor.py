import RPi.GPIO as GPIO
import time
IN1=5
IN2=6
IN3=13
IN4=19

def setStep(h1,h2,h3,h4):
    GPIO.output(IN1,h1)
    GPIO.output(IN2,h2)
    GPIO.output(IN3,h3)
    GPIO.output(IN4,h4)
def setup():
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)

def stop():
    setStep(0,0,0,0)

def forward(delay, steps):
    for i in range(0,steps):
        setStep(1,0,0,0)
        time.sleep(delay)
        setStep(0,1,0,0)
        time.sleep(delay)
        setStep(0,0,1,0)
        time.sleep(delay)
        setStep(0,0,0,1)
        time.sleep(delay)

def backward(delay, steps):
    for i in range(0,steps):
        setStep(0,0,0,1)
        time.sleep(delay)
        setStep(0,0,1,0)
        time.sleep(delay)
        setStep(0,1,0,0)
        time.sleep(delay)
        setStep(1,0,0,0)
        time.sleep(delay)

def destroy():
    GPIO.cleanup()



def main(flag):
    setup()
    if flag==1:
        forward(0.008,256)
    else:
        backward(0.008,256)

if __name__ =='__main__':
    main(1)
    
