from machine import Pin, ADC, PWM
from time import sleep, ticks_ms

# LED引腳配置
led_up = Pin(14, Pin.OUT)    # 上
led_down = Pin(13, Pin.OUT)  # 下
led_left = Pin(4, Pin.OUT)   # 左
led_right = Pin(27, Pin.OUT) # 右

# 搖桿ADC引腳
adc_x = ADC(Pin(33))   # X軸
adc_y = ADC(Pin(15))   # Y軸
adc_x.atten(ADC.ATTN_11DB)
adc_y.atten(ADC.ATTN_11DB)

# 蜂鳴器和開關
buzzer = PWM(Pin(12))  # GPIO12
buzzer.duty(0)         # 初始關閉
switch = Pin(16, Pin.IN, Pin.PULL_UP)  # 開關接GPIO16

# 全域變數
CENTER = 2000
THRESHOLD = 500
buzzer_on = False
last_switch_time = 0
debounce_delay = 200  # 防抖時間(ms)
current_freq = 0      # 當前頻率(Hz)

def clear_leds():
    led_up.off()
    led_down.off()
    led_left.off()
    led_right.off()

def toggle_buzzer():
    global buzzer_on
    buzzer_on = not buzzer_on
    if buzzer_on:
        buzzer.duty(512)  # 50%佔空比
    else:
        buzzer.duty(0)    # 關閉
    print(f"蜂鳴器: {'開啟' if buzzer_on else '關閉'}")

while True:
    # 讀取搖桿
    x_val = adc_x.read()
    y_val = adc_y.read()
    
    clear_leds()
    direction = "中心"  # 預設方向
    new_freq = 0       # 新計算的頻率

    # 方向檢測（帶頻率設置）
    if x_val < CENTER - THRESHOLD and y_val < CENTER - THRESHOLD:zzz
        led_left.on()
        led_up.on()
        direction = "左上"
        new_freq = 523  # C5
    elif x_val < CENTER - THRESHOLD and y_val > CENTER + THRESHOLD:
        led_left.on()
        led_down.on()
        direction = "左下"
        new_freq = 587  # D5
    elif x_val > CENTER + THRESHOLD and y_val < CENTER - THRESHOLD:
        led_right.on()
        led_up.on()
        direction = "右上"
        new_freq = 659  # E5
    elif x_val > CENTER + THRESHOLD and y_val > CENTER + THRESHOLD:
        led_right.on()
        led_down.on()
        direction = "右下"
        new_freq = 698  # F5
    elif x_val < CENTER - THRESHOLD:
        led_left.on()
        direction = "左"
        new_freq = 392  # G4
    elif x_val > CENTER + THRESHOLD:
        led_right.on()
        direction = "右"
        new_freq = 440  # A4
    elif y_val < CENTER - THRESHOLD:
        led_up.on()
        direction = "上"
        new_freq = 494  # B4
    elif y_val > CENTER + THRESHOLD:
        led_down.on()
        direction = "下"
        new_freq = 330  # E4
    
    # 更新頻率（蜂鳴器開啟時）
    if buzzer_on and new_freq != 0:
        if new_freq != current_freq:  # 頻率變化時才更新
            buzzer.freq(new_freq)
            current_freq = new_freq
    
    # 開關檢測（帶防抖）
    current_time = ticks_ms()
    if switch.value() == 0 and (current_time - last_switch_time) > debounce_delay:
        toggle_buzzer()
        last_switch_time = current_time
    
    # 串口輸出（永遠顯示蜂鳴器狀態）
    status = f"方向: {direction} | 蜂鳴器: {'開啟' if buzzer_on else '關閉'}"
    if buzzer_on and current_freq > 0:
        status += f" | 頻率: {current_freq}Hz"
    print(status)
    
    sleep(0.1)
