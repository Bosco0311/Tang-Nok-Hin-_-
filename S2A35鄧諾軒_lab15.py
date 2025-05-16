import network
import time
from machine import Pin, PWM
from umqtt.robust import MQTTClient
import ubinascii

# 初始化蜂鸣器
buzzer = PWM(Pin(16))
buzzer.duty(0)

# 预定义的音调列表（频率Hz，持续时间毫秒）
tune_list = [
    (880, 857), (784, 214), (698, 429), (784, 429),
    (880, 429), (880, 429), (880, 429), (0, 429),
    (784, 429), (784, 429), (784, 429), (0, 429),
    (880, 429), (880, 429), (880, 429), (0, 429),
    (880, 857), (784, 214), (698, 429), (784, 429),
    (880, 429), (880, 429), (880, 429), (0, 429),
    (784, 429), (784, 429), (880, 429), (784, 429),
    (698, 857)
]

tune_length = len(tune_list)
tune_index = 0
buzzer_on = False

# WiFi连接函数
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)
    
    # 断开现有连接
    if sta_if.isconnected():
        sta_if.disconnect()
        time.sleep(1)
    
    print("正在連接WiFi...")
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            sta_if.connect("軒Hin", "63477640")
            # 等待连接，最多等待10秒
            for _ in range(20):
                if sta_if.isconnected():
                    print("WiFi已連接")
                    print("IP地址:", sta_if.ifconfig()[0])
                    return True
                time.sleep(0.5)
            print("WiFi連接超時，重試中...")
        except Exception as e:
            print("WiFi連接錯誤:", e)
        
        retry_count += 1
        if retry_count < max_retries:
            print(f"第{retry_count}次重試...")
            time.sleep(2)
    
    print("WiFi連接失敗")
    return False

# 尝试连接WiFi
if not connect_wifi():
    print("無法連接WiFi，程序終止")
    import sys
    sys.exit()

# 生成唯一的客户端ID
def get_unique_id():
    mac = ubinascii.hexlify(network.WLAN().config('mac')).decode()
    return f"esp32_{mac}"

# 初始化MQTT客户端
def connect_mqtt():
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            client_id = get_unique_id()
            print(f"使用客戶端ID: {client_id}")
            
            client = MQTTClient(
                client_id=client_id,
                server="io.adafruit.com",
                user="Bosco311",
                password="aio_NVUc91jT4lii4sLgZrKwCF5B1CO3",
                ssl=False)
            
            print("正在連接MQTT...")
            client.connect()
            client.set_callback(get_cmd)
            client.subscribe(client.user.encode() + b"/feeds/timer")
            print("MQTT已連接")
            return client
        except Exception as e:
            print(f"MQTT連接錯誤 (嘗試 {retry_count + 1}/{max_retries}):", e)
            retry_count += 1
            if retry_count < max_retries:
                print("等待5秒後重試...")
                time.sleep(5)
    
    print("MQTT連接失敗")
    return None

def get_cmd(topic, msg):
    global buzzer_on
    print(topic, msg)
    if msg == b"100":
        buzzer_on = True
        print('Times up!')
    else:
        buzzer_on = False
        print('CLEAR.')

# 尝试连接MQTT
client = connect_mqtt()
if client is None:
    print("無法連接MQTT，程序終止")
    import sys
    sys.exit()

while True:
    try:
        client.check_msg()
        if buzzer_on:
            freq, msec = tune_list[tune_index]
            if freq > 0:
                buzzer.freq(freq)
                buzzer.duty(512)
                time.sleep(msec * 0.001)
            buzzer.duty(0)
            time.sleep(0.05)
            tune_index += 1
            if tune_index >= tune_length:
                tune_index = 0
        else:
            buzzer.duty(0)
            tune_index = 0
    except Exception as e:
        print("運行錯誤:", e)
        # 尝试重新连接MQTT
        print("嘗試重新連接MQTT...")
        client = connect_mqtt()
        if client is None:
            print("重新連接失敗，等待30秒後重試...")
            time.sleep(30)
        else:
            print("重新連接成功") 
