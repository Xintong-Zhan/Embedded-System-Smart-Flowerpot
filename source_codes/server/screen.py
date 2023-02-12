from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306


# 创建 IIC 设备
serial = i2c(port=1, address=0x3C)

# 如果使用 SPI，换成这个
# serial = spi(device=0, port=0)

# 创建屏幕的驱动实例
device = ssd1306(serial,width=128,height=32)

def draw(x,y,text):
  # 开始往屏幕上绘图。draw 是 Pillow 的实例，它里面还有非常多的绘图 API。
  with canvas(device) as draw:
    #draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((x,y),text, fill="white")

# 这行是为了阻止程序退出，因为退出的时候会调用析构函数，清空屏幕。防止一闪而过，什么也看不到。
#while (True):
 # pass