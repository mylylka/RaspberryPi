#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
该Python程序主要用于实现基于Raspberry Pi的HC-SR04超声波传感器距离测量功能。
"""

import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        """初始化超声波传感器
        
        参数:
            trigger_pin: 触发引脚（BCM编号）
            echo_pin: 回声引脚（BCM编号）
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)
        time.sleep(2)  # 传感器稳定时间

    def measure(self):
        """执行距离测量"""
        try:
            # 发送触发信号
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)  # 10微秒脉冲
            GPIO.output(self.trigger_pin, GPIO.LOW)
            t0 = time.time()
            # 等待回声信号发出
            while GPIO.input(self.echo_pin) == GPIO.LOW:
                if time.time() - t0 > 0.038:
                    return float('inf')
            # 记录发射时间
            t1 = time.time()

            # 等待回声信号返回
            while GPIO.input(self.echo_pin) == GPIO.HIGH:
                if time.time() - t0 > 0.038:
                    return float('inf')
            t2 = time.time()
            
            # 计算距离（声速在空气中约为343米/秒）
            return (t2 - t1) * 34300 / 2  # 单位：厘米
        
        except Exception as e:
            print(f"[错误] 测量失败 @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
            return None

    def __del__(self):
        """对象销毁时自动清理GPIO资源"""
        GPIO.cleanup()

# 使用示例
if __name__ == '__main__':
    # 初始化传感器，设置触发引脚为23，回声引脚为24
    sensor = HCSR04(trigger_pin=23, echo_pin=24) 
    
    try:
        print("Ultrasonic distance measurement in progress...")
        while True:
            dist = sensor.measure()
            if dist == float('inf') or dist > 400:
                print("Out of measurement range")
            elif dist is not None:
                print(f"Distance: {dist:.2f} cm")  # Keep image output format
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMeasurement ended")
