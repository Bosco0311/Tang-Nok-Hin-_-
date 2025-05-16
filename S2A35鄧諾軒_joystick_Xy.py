from machine import Pin, ADC
from time import sleep

# LED引腳配置
led_up = Pin(14, Pin.OUT)    
led_down = Pin(13, Pin.OUT)  
led_left = Pin(4, Pin.OUT)   
led_right = Pin(27, Pin.OUT) 

# 搖桿ADC引腳
adc_x = ADC(Pin(33))   # X軸
adc_y = ADC(Pin(15))   # Y軸
adc_x.atten(ADC.ATTN_11DB)
adc_y.atten(ADC.ATTN_11DB)

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
    y_val = adc_y.read()
    
    clear_leds()
    direction = "中心"  # 預設方向

    # 方向檢測
    if x_val < CENTER - THRESHOLD and y_val < CENTER - THRESHOLD:
        led_left.on()
        led_up.on()
        direction = "左上"
    elif x_val < CENTER - THRESHOLD and y_val > CENTER + THRESHOLD:
        led_left.on()
        led_down.on()
        direction = "左下"
    elif x_val > CENTER + THRESHOLD and y_val < CENTER - THRESHOLD:
        led_right.on()
        led_up.on()
        direction = "右上"
    elif x_val > CENTER + THRESHOLD and y_val > CENTER + THRESHOLD:
        led_right.on()
        led_down.on()
        direction = "右下"
    elif x_val < CENTER - THRESHOLD:
        led_left.on()
        direction = "左"
    elif x_val > CENTER + THRESHOLD:
        led_right.on()
        direction = "右"
    elif y_val < CENTER - THRESHOLD:
        led_up.on()
        direction = "上"
    elif y_val > CENTER + THRESHOLD:
        led_down.on()
        direction = "下"
    
    # 串口輸出
    print(f"方向: {direction}")
    
    sleep(0.1)
