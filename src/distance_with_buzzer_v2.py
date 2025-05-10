#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于HC-SR04超声波传感器的距离测量系统
该程序通过超声波传感器测量距离，并根据距离控制蜂鸣器报警
不同距离范围蜂鸣器会发出不同频率的警报声

硬件连接:
- 超声波传感器触发引脚(TRIG)连接到GPIO23
- 超声波传感器回声引脚(ECHO)连接到GPIO24
- 蜂鸣器控制引脚连接到GPIO25
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
# 等待传感器稳定
time.sleep(2)

# 定义测量距离的函数
def measure_distance():
    """执行距离测量"""
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
        
        # 计算距离
        return (t2 - t1) * 34300 / 2  # 单位: 厘米
    
    except Exception as e:
        print(f"[ERROR] Measurement failed @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
        return None

# 定义控制蜂鸣器的函数
def control_buzzer(distance):
    """根据距离控制蜂鸣器"""
    if distance is not None:
        if distance < 5:  # 近距离
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.01)
        elif distance < 10:  # 中距离
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.05)
        elif distance < 20:  # 远距离
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
        else:  # 超过20厘米不报警
            GPIO.output(BUZZER_PIN, GPIO.HIGH)


# 主程序
print("Ultrasonic distance measurement in progress...")

try:
    while True:
        dist = measure_distance()
        control_buzzer(dist)  # 控制蜂鸣器
        
        if dist == float('inf') or dist > 400:
            print("Out of measurement range")
        elif dist is not None:
            status = "ALARM" if dist < 20 else "NORMAL"
            print(f"Distance: {dist:.2f} cm [{status}]")
        
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nMeasurement ended")
finally:
    # 确保清理GPIO资源
    print("Cleaning up GPIO...")
    GPIO.cleanup()

