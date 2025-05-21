from machine import Pin, I2C, ADC, PWM
import ssd1306
import time
import random

# ===== 硬體設定 =====
# OLED 設定 (I2C)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 搖桿腳位 (ADC)
joy_x = ADC(Pin(34))
joy_y = ADC(Pin(35))
joy_x.atten(ADC.ATTN_11DB)
joy_y.atten(ADC.ATTN_11DB)

# 蜂鳴器 (PWM)
buzzer = PWM(Pin(14), freq=1000, duty=0)

# 啟動按鈕 (GPIO16)
start_btn = Pin(16, Pin.IN, Pin.PULL_UP)

# LED 設定
led_pins = [Pin(17, Pin.OUT), Pin(18, Pin.OUT), Pin(19, Pin.OUT), Pin(23, Pin.OUT),
            Pin(5, Pin.OUT), Pin(1, Pin.OUT), Pin(3, Pin.OUT), Pin(2, Pin.OUT)]

# ===== 遊戲參數 =====
PLAYER_SIZE = 10
BLOCK_SIZE = 10
player = {"x": 64, "y": 54, "dx": 0, "dy": 0}
blocks = [{"x": 0, "y": 0} for _ in range(5)]
score = 0
game_active = False
last_score = 0  # Track last score for buzzer

# ===== 遊戲速度控制 =====
MOVE_DELAY = 0.03
BLOCK_SPEED = 0.5
PLAYER_SPEED = 1  # 玩家速度保持不變

# 初始死區值
initial_deadzone = 1000
min_deadzone = 100  # 最小死區值
score_threshold = 5  # 每增加5分減少死區

# ===== 初始化方塊 =====
def init_blocks():
    for block in blocks:
        block["x"] = random.randint(0, 127 - BLOCK_SIZE)
        block["y"] = random.randint(-200, -50)

# ===== 碰撞檢測 =====
def check_collision(rect1, rect2):
    return (rect1["x"] < rect2["x"] + BLOCK_SIZE and
            rect1["x"] + PLAYER_SIZE > rect2["x"] and
            rect1["y"] < rect2["y"] + BLOCK_SIZE and
            rect1["y"] + PLAYER_SIZE > rect2["y"])

# ===== 遊戲結束處理 =====
def game_over():
    global game_active
    if game_active:  # Only show if the game was active
        game_active = False
        oled.fill(0)
        oled.text("GAME OVER", 20, 20)
        oled.text("Score: " + str(score), 30, 40)
        oled.show()
        buzzer.duty(512)
        time.sleep(0.5)
        buzzer.duty(0)
        time.sleep(2)

        # Show the score for 3 seconds
        for _ in range(30):  # 30 iterations for ~3 seconds
            oled.fill(0)
            oled.text("Score: " + str(score), 30, 20)
            oled.show()
            time.sleep(0.1)

# ===== LED 燈光處理 =====
def update_leds():
    for i in range(8):
        if score >= (i + 1) * 5:  # 每5分亮一個LED
            led_pins[i].on()
        else:
            led_pins[i].off()

def win_sequence():
    for _ in range(10):  # Sound buzzer 10 times
        buzzer.duty(512)  # Activate buzzer
        time.sleep(0.2)   # Duration of the sound
        buzzer.duty(0)    # Turn off buzzer
        time.sleep(0.1)   # Short pause between sounds

# ===== 重置遊戲 =====
def reset_game():
    global score, BLOCK_SPEED, last_score
    score = 0
    BLOCK_SPEED = 0.5  # 重置方塊速度
    player["x"], player["y"] = 64, 54
    init_blocks()
    update_leds()
    last_score = 0  # Reset last score

# ===== 顯示歡迎畫面 =====
def show_welcome_screen():
    oled.fill(0)
    oled.text("Welcome to the", 15, 20)
    oled.text("Game!", 40, 40)
    oled.text("Press Button", 15, 50)
    oled.show()

# ===== 開始畫面 =====
def show_start_screen():
    oled.fill(0)
    oled.text("Press Button", 15, 20)
    oled.text("to Start", 30, 40)
    oled.show()

# ===== 主程式 =====
while True:
    if not game_active:
        show_welcome_screen()  # Show welcome until the game starts
        if start_btn.value() == 0:  # 按下按鈕時啟動遊戲
            game_active = True
            reset_game()
        continue

    # 根據分數動態調整死區
    deadzone = max(min_deadzone, initial_deadzone - (score // score_threshold) * 100)

    # 讀取搖桿數值
    x_val = joy_x.read()
    y_val = joy_y.read()

    # 計算移動方向
    player["dx"] = 0
    player["dy"] = 0

    if game_active:
        if abs(x_val - 2048) > deadzone:
            if x_val < 2048 - deadzone:
                player["dx"] = -PLAYER_SPEED
            elif x_val > 2048 + deadzone:
                player["dx"] = PLAYER_SPEED

        if abs(y_val - 2048) > deadzone:
            if y_val < 2048 - deadzone:
                player["dy"] = -PLAYER_SPEED
            elif y_val > 2048 + deadzone:
                player["dy"] = PLAYER_SPEED

    # 保存原本位置
    original_position = (player["x"], player["y"])

    # 更新玩家位置
    player["x"] = max(0, min(128 - PLAYER_SIZE, player["x"] + player["dx"]))
    player["y"] = max(0, min(64 - PLAYER_SIZE, player["y"] + player["dy"]))

    # 檢查是否移動
    if (player["x"], player["y"]) != original_position:
        print("Moved to X:", player["x"], "Y:", player["y"])
    else:
        print("No movement")

    # 更新方塊位置
    for block in blocks:
        block["y"] += BLOCK_SPEED
        if block["y"] >= 64:
            block["y"] = random.randint(-50, -10)
            block["x"] = random.randint(0, 127 - BLOCK_SIZE)
            score += 1
            
            # Check for buzzer activation
            if score // 5 > last_score // 5:  # Check if score increased by 5
                buzzer.duty(512)  # Activate buzzer
                time.sleep(0.2)   # Duration of the sound
                buzzer.duty(0)    # Turn off buzzer

            # Update last_score
            last_score = score

            # 隨著分數增加方塊速度
            BLOCK_SPEED += 0.05  # 每次得分增加方塊速度

            # 更新 LED
            update_leds()

            # 檢查是否獲勝
            if score >= 45:  # 獲勝條件
                oled.fill(0)
                oled.text("YOU WIN!", 20, 20)
                oled.show()
                win_sequence()  # Play winning sound sequence
                game_active = False  # 遊戲結束，不自動重啟

    # 碰撞檢測
    for block in blocks:
        if check_collision(player, block):
            game_over()
            break

    # 顯示玩家位置和搖桿值
    print("Player X:", player["x"], "Player Y:", player["y"])
    print("Joystick X:", x_val, "Joystick Y:", y_val)

    # 繪製畫面
    oled.fill(0)
    # Draw the player with a color pattern (simulate color)
    oled.fill_rect(player["x"], player["y"], PLAYER_SIZE, PLAYER_SIZE, 1)  # Main color
    oled.fill_rect(player["x"] + 1, player["y"] + 1, PLAYER_SIZE - 2, PLAYER_SIZE - 2, 0)  # Inner color

    for block in blocks:
        oled.fill_rect(int(block["x"]), int(block["y"]), BLOCK_SIZE, BLOCK_SIZE, 1)

    oled.text("Score: " + str(score), 0, 0)
    oled.show()

    time.sleep(MOVE_DELAY)  # 控制整體速度
