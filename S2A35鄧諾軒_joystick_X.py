from machine import Pin, ADC
from time import sleep

# LED引腳配置
led_up = Pin(14, Pin.OUT)    
led_down = Pin(13, Pin.OUT)  
led_left = Pin(4, Pin.OUT)   
led_right = Pin(27, Pin.OUT) 

# 搖桿ADC引腳
adc_x = ADC(Pin(33))   # X軸
adc_x.atten(ADC.ATTN_11DB)

# 全域變數
CENTER = 2000
THRESHOLD = 500

def clear_leds():
    led_up.off()
    led_down.off()
    led_left.off()
    led_right.off()

while True:
    # 讀取搖桿
    x_val = adc_x.read()
    
    clear_leds()
    direction = "中心"  # 預設方向

    # 方向檢測
    if x_val < CENTER - THRESHOLD:
        led_left.on()
        direction = "左"
    elif x_val > CENTER + THRESHOLD:
        led_right.on()
        direction = "右"
    
    # 串口輸出
    print(f"方向: {direction}")
    
    sleep(0.1)
