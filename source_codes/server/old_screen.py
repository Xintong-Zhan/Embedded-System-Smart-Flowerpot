from machine import RTC,Pin, I2C, ADC,PWM
import ssd1306
import utime

#print(rtc.datetime())

#choose_mode
def buttonA_handler(p):
    global flag
    cnt=0
    while cnt<=20:
        if buttonA.value()==True:
            cnt+=1
        utime.sleep(0.01)
    flag+=1
    flag=flag%2
   
#choose:hour/min/sec
def buttonB_handler(p):
    global mode
    cnt=0
    while cnt<=20:
        if buttonB.value()==True:
            cnt+=1
        utime.sleep(0.01)
    mode+=1
    mode=mode%3

#add_time
def buttonC_handler(p):
   
    global flag
    global mode
    global set_time

    cnt=0
    while cnt<=20:
        if buttonC.value()==True:
            cnt+=1
        utime.sleep(0.01)
    if flag==0:
        tmp=rtc.datetime()
        if mode==0:
            new_rtctime=(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4]+1,tmp[5],tmp[6],tmp[7])
            rtc.datetime(new_rtctime)
        elif mode==1:
            new_rtctime=(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]+1,tmp[6],tmp[7])
            rtc.datetime(new_rtctime)
        else:
            new_rtctime=(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6]+1,tmp[7])
            rtc.datetime(new_rtctime)

    else:

        if mode==0:
            set_time[0]=set_time[0]+1
            if set_time[0]>=24:
                set_time[0]=0
        elif mode==1:
            set_time[1]=set_time[1]+1
            if set_time[1]>=60:
                set_time[1]=0        
        else:
            set_time[2]=set_time[2]+1
            if set_time[2]>=60:
                set_time[2]=0
           

  

flag=0
#flag==0:change rtc;flag==1:change set_time
mode=0
#mode==0:hour;mode==1:min;mode==2:sec

global set_time

buttonA=Pin(12,Pin.IN,Pin.PULL_UP)
buttonB=Pin(13,Pin.IN,Pin.PULL_UP)
buttonC=Pin(2,Pin.IN,Pin.PULL_UP)


buttonA.irq(trigger=Pin.IRQ_FALLING , handler=buttonA_handler)
buttonB.irq(trigger=Pin.IRQ_FALLING , handler=buttonB_handler)
buttonC.irq(trigger=Pin.IRQ_FALLING , handler=buttonC_handler)

rtc = RTC()
rtc.datetime((2022, 2, 1, 4, 15, 27, 0, 0)) # set a specific date and time

set_time=[0,0,1]

adc=ADC(0)
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

happy=[["rtc hour","rtc min","rtc sec"],["alarm hour","alarm min","alarm sec"]]
while True:
    display.fill(0)
    time2=rtc.datetime()[4:7]
    real_time="rtc "+str(time2[0])+':'+str(time2[1])+':'+str(time2[2])
    display.text(real_time, 0, 0, 1)
    set_time_str="alarm "+str(set_time[0])+':'+str(set_time[1])+':'+str(set_time[2])
    display.text(set_time_str,0,8,1)  
    adc_value=adc.read()
    
    display.text("brightness"+str(adc_value),0,24,1)
    display.contrast(adc_value)  # bright
    if time2[0]==set_time[0] and time2[1]==set_time[1]:
        motor = PWM(Pin(15),freq=512,duty=512)
        display.text(happy[flag][mode]+" alarm!!",0,16,3)

    else:
        motor = PWM(Pin(15),freq=0,duty=0)
        display.text(happy[flag][mode],0,16,3)

    display.show()
    utime.sleep(1)