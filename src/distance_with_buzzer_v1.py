#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
超声波测距系统 - 使用HC-SR04传感器与蜂鸣器报警

该程序通过HC-SR04超声波传感器测量距离，并根据设定的阈值控制蜂鸣器报警。

使用低电平触发蜂鸣器

硬件连接：
- HC-SR04传感器触发引脚(TRIG)连接到GPIO23
- HC-SR04传感器回声引脚(ECHO)连接到GPIO24
- 有源蜂鸣器控制引脚连接到GPIO25
"""

import RPi.GPIO as GPIO
import time

# 定义引脚
TRIG_PIN = 23
ECHO_PIN = 24
BUZZER_PIN = 25

# 设置GPIO模式和引脚
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.HIGH)

# 传感器稳定时间
time.sleep(2)

# 测量距离的函数
def measure():
    try:
        # 发送触发信号
        GPIO.output(TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)  # 10微秒脉冲
        GPIO.output(TRIG_PIN, GPIO.LOW)
        t0 = time.time()
        
        # 等待回声信号发出
        while GPIO.input(ECHO_PIN) == GPIO.LOW:
            if time.time() - t0 > 0.038:
                return float('inf')
        
        # 记录发射时间
        t1 = time.time()

        # 等待回声信号返回
        while GPIO.input(ECHO_PIN) == GPIO.HIGH:
            if time.time() - t0 > 0.038:
                return float('inf')
        
        t2 = time.time()
        
        # 计算距离（声速在空气中约为343米/秒）
        return (t2 - t1) * 34300 / 2  # 单位: 厘米
    except Exception as e:
        print(f"[ERROR] Measurement failed @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
        return None

# 根据距离控制蜂鸣器的函数
def control_buzzer(distance, threshold=20):
    if distance is not None:
        if distance < threshold:
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # 激活蜂鸣器
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)   # 关闭蜂鸣器
            # print(f"Buzzer: OFF (Actual GPIO state: {GPIO.input(BUZZER_PIN)})")
            # print("Buzzer: OFF")

# 主程序部分
print("Ultrasonic distance measurement with buzzer alarm in progress...")
try:
    while True:
        # 测量距离
        dist = measure()
        # 根据距离和阈值控制蜂鸣器
        control_buzzer(dist, threshold=20)
        # input("按Enter继续...")
        if dist == float('inf') or dist > 400:
            print("Out of measurement range")
        elif dist is not None:
            # 根据距离与阈值比较显示状态
            status = "ALARM" if dist < 20 else "NORMAL"
            print(f"Distance: {dist:.2f} cm [{status}]")
        
        # 每隔0.5秒测量一次
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nMeasurement ended")
finally:
    print("Cleaning up GPIO...")
    GPIO.cleanup()