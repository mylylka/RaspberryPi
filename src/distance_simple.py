#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
该Python程序主要用于实现基于Raspberry Pi的HC-SR04超声波传感器距离测量功能。
"""

import RPi.GPIO as GPIO
import time

# 硬件引脚配置
TRIG_PIN = 23  # 触发引脚（BCM编号）
ECHO_PIN = 24  # 回声引脚（BCM编号）

# 初始化传感器
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO_PIN, GPIO.IN)
time.sleep(2)  # 传感器稳定时间

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
        
        # 计算距离（声速在空气中约为343米/秒）
        return (t2 - t1) * 34300 / 2  # 单位：厘米
    
    except Exception as e:
        print(f"[ERROR] Measurement failed @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
        return None

def cleanup():
    print("Cleaning up GPIO...")
    GPIO.cleanup()

# 主程序
print("Ultrasonic distance measurement in progress...")
try:
    while True:
        dist = measure_distance()
        if dist == float('inf') or dist > 400:
            print("Out of measurement range")
        elif dist is not None:
            print(f"Distance: {dist:.2f} cm")  # 保持原输出格式
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nMeasurement ended")
finally:
    cleanup()