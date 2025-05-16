import network, time
from machine import Pin, PWM
from umqtt.robust import MQTTClient

buzzer = PWM(Pin(5))
buzzer.duty(0)

# Predefined tune list (frequency in Hz, duration in milliseconds)
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

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("軒Hin", "63477640")

while not sta_if.isconnected():
    pass
print("控制板已連線")

client = MQTTClient(
    client_id="",
    server="io.adafruit.com",
    user="Bosco311",
    password="aio_fFvk47sYW7SIzwC4SVOOAz5VYaEe",
    ssl=False)

def get_cmd(topic, msg):
    global buzzer_on
    print(topic, msg)
    if msg == b"100":
        buzzer_on = True
        print('Times up!')
    else:
        buzzer_on = False
        print('CLEAR.')

client.connect()
client.set_callback(get_cmd)
client.subscribe(client.user.encode() + b"/feeds/timer")

while True:
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
