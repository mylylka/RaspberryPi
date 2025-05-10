#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        """Initialize ultrasonic sensor
        
        Args:
            trigger_pin: Trigger pin (BCM numbering)
            echo_pin: Echo pin (BCM numbering)
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)
        time.sleep(2)  # Sensor stabilization time

    def measure(self):
        """Execute distance measurement

        引脚配置电平代码：GPIO.output(self.trigger_pin, GPIO.HIGH)
        探测引脚电平代码：GPIO.input(self.echo_pin) == GPIO.LOW
        
        """
        try:
            # 给传感器发送触发信号（10微秒高电平）
            
            # 等待回波开始（发出超声波）

            # 记录开始时间

            # 等待回波结束（接收到反射回来的超声波）

            # 记录结束时间

            # 计算距离
            return 0  # 返回距离
        
        except Exception as e:
            print(f"[ERROR] Measurement failed @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
            return None

    def __del__(self):
        """Automatically clean up GPIO on destruction"""
        GPIO.cleanup()

# 使用示例
if __name__ == '__main__':

    sensor = HCSR04(trigger_pin=23, echo_pin=24) 
    
    try:
        print("Ultrasonic distance measurement in progress...")
        while True:
            dist = sensor.measure()
            if dist > 400:
                print("Out of measurement range")
            elif dist is not None:
                print(f"Distance: {dist:.2f} cm")  # Keep image output format
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMeasurement ended")
