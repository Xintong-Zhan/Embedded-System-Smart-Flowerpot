# DHT11 湿度温度传感器 驱动
# 使用方法： 接线 DHT11的三个引脚(如果是四个引脚NC不连接) VCC接5V GND接地 数据D接任意树莓派GPIO口
# 并将数据D接的树莓派GPIO口BCM编号设置为下面的pin
# 然后你可以直接运行本文件得到数值，也可以使用import dht11_drive导入模块
# 导入后使用 dht11_drive.dht11() 函数获取湿度与温度 返回值是一个元组

import RPi.GPIO as GPIO
import time

#############################################################
pin = 17 # 这里填写GPIO号（BCM引脚编号模式）    手动改变此行
#############################################################

GPIO.setmode(GPIO.BCM)  # 设置使用BCM引脚编号模式

def main(pin):
    GPIO.setup(pin,GPIO.OUT)  # 設置引腳輸出
    GPIO.output(pin,True)  # 高电平

    # 树莓派下拉19ms
    GPIO.output(pin,False)
    time.sleep(0.02)
    #GPIO.output(pin,True)

    GPIO.setup(pin,GPIO.IN)  # 设置引腳输入

    time_data_list = []  # 保存数据（高电平持续）时间的列表

    pan_duan = 1  #判断数据是否正确

    end_times = 0  # 数据是否接收完毕 决定是否结束大循环
    start_time = 0  # 防止start_time未定义
    end_time = 0  # 防止end_time未定义
    while 1:
        start_time_total = time.time()  # 记录每次运行循环开始时间

        if end_times == 1: # 数据接收完毕
            break

        while GPIO.input(pin) == 0:  # 等待电平不为低
            start_time = time.time()  # 得到高电平开始时间
            if (start_time - start_time_total) > 0.1 :  # 判断循环时间过长 电平已经不再变化
                end_times = 1
                break

        while GPIO.input(pin) == 1:  # 等待电平不为高
            end_time = time.time()  # 得到高电平结束时间
            if (end_time - start_time_total) > 0.1 :  # 判断循环时间过长 电平已经不再变化
                end_times = 1
                break

        time_data = end_time - start_time  # 计算出高电平持续时间

        time_data_list.append(time_data)  # 高电平持续时间数据写入列表
        # print(str(time_data)+',   ', end='')

    # print(time_data_list)
    # print(len(time_data_list))

    new_time_data_list = []  # 保存筛选过的时间

    for i in range(len(time_data_list)):
        if (time_data_list[i] > 1.9e-5 ) and (time_data_list[i] < 7.8e-5):
            new_time_data_list.append(time_data_list[i])

    #print(new_time_data_list)
    #print(len(new_time_data_list))

    if len(new_time_data_list) != 40:
        pan_duan = 0  #判断数据是否正确
        return 0, -1

    if pan_duan == 1:  #判断数据是否正确
        Binary_list = []  # 保存二进制数据
        for i in new_time_data_list:
            if i > 5.0e-5 :
                Binary_list.append(1)
            elif i < 5.0e-5 :
                Binary_list.append(0)
        if len(Binary_list) != 40 :
            pan_duan = 0  #判断数据是否正确 
            return 0, -1

        #print(Binary_list)
        #print(len(Binary_list))


    if pan_duan == 1:  #判断数据是否正确
    # 转字符串格式
        str_Binary_list = []
        for i in Binary_list:
            str_Binary_list.append(str(i))


    if pan_duan == 1:  #判断数据是否正确

        # 分割数据 并合并成字符串
        # 共40位数据 0-8为湿度整数 9-16为湿度小数 17-24为温度整数 25-32为湿度小数 33-40为校验和（前四个数据直接相加）
        str_shidu_zhengshu = ''.join(str_Binary_list[0:8])
        str_shidu_xiaoshu = ''.join(str_Binary_list[8:16])
        str_wendu_zhengshu = ''.join(str_Binary_list[16:24])
        str_wendu_xiaoshu = ''.join(str_Binary_list[24:32])
        str_yanzheng = ''.join(str_Binary_list[32:40])

        # 转换为十进制
        int_shidu_zhengshu = int(str_shidu_zhengshu,2)
        int_shidu_xiaoshu = int(str_shidu_xiaoshu,2)
        int_wendu_zhengshu = int(str_wendu_zhengshu,2)
        int_wendu_xiaoshu = int(str_wendu_xiaoshu,2)
        int_yanzheng = int(str_yanzheng,2)

        if int_yanzheng != (int_shidu_zhengshu + int_shidu_xiaoshu + int_wendu_zhengshu + int_wendu_xiaoshu):
            pan_duan = 0  # 数据不正确
            return 0, -1

        if int_yanzheng == (int_shidu_zhengshu + int_shidu_xiaoshu + int_wendu_zhengshu + int_wendu_xiaoshu):
            pan_duan = 1  # 数据正确
            str_shidu = str(int_shidu_zhengshu) + '.' + str(int_shidu_xiaoshu)
            str_wendu = str(int_wendu_zhengshu) + '.' + str(int_wendu_xiaoshu)
            float_shidu = float(str_shidu)
            float_wendu = float(str_wendu)
            return 1, (float_shidu, float_wendu)  # 返回 湿度 温度


def dht11():  # 循环五次
    for i in range(8):
        pan_duan_01, return_data = main(pin)
        if pan_duan_01 == 1:
            return return_data
        time.sleep(0.2)
    print('error')
    return return_data, return_data


if __name__ =='__main__':
    shidu, wendu = dht11()
    print('Humidity' + str(shidu) + '%')
    print('Temperature' + str(wendu) + 'C') 