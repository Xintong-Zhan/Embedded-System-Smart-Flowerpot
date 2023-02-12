import RPi.GPIO as GPIO
import time
 
Buzzer = 23 #蜂鸣器接在第18管脚上
 
# 定义低中高频率
CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes
 
CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes
 
CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes
 
song_2 = [	CM[1], CM[1], CM[2], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
			CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
			CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
			CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]
 
beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			# Beats of song 2, 1 means 1/8 beats
			1, 1, 2, 2, 1, 1, 3, 1, 
			1, 2, 2, 1, 1, 2, 2, 1, 
			1, 2, 2, 1, 1, 3 ]
 
# 一些初始化操作
def setup():
    GPIO.setwarnings(False)         # 先关掉警告，因为操作io口会有警告
    GPIO.setmode(GPIO.BCM)		# Numbers GPIOs by physical location 树莓派有很多编码模式，这里采用BCM编码模式
    GPIO.setup(Buzzer, GPIO.OUT)	# Set pins' mode is output Buzzer = 11 #蜂鸣器接在第11管脚上
    global Buzz						# Assign a global variable to replace GPIO.PWM
    Buzz = GPIO.PWM(Buzzer, 440)	# 440 is initial frequency.440HZ初试频率
    Buzz.start(50)					# Start Buzzer pin with 50% duty ration 
 
def destroy():
	Buzz.stop()					# Stop the buzzer
	GPIO.output(Buzzer, 1)		# Set Buzzer pin to High
 

def main():
    setup()
	#Buzz.ChangeFrequency(500)
    #for i in range(1,len(song_2)):
        #Buzz.ChangeFrequency(song_2[i])
    time.sleep(3)
    destroy()


# 释放资源

if __name__ == '__main__':		# Program start from here

	try:
		main()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()