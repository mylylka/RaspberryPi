#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        """初始化超声波传感器
        
        Args:
            trigger_pin: 触发引脚（BCM编号）
            echo_pin: 回波引脚（BCM编号）
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
            time.sleep(0.00001)  # 10μs脉冲
            GPIO.output(self.trigger_pin, GPIO.LOW)
            
            # 记录发射时刻
            t1 = time.time()
            
            # 等待回波到达
            while GPIO.input(self.echo_pin) == 0:
                if time.time() - t1 > 0.038:
                    return float('inf')
            
            # 等待回波结束
            t2 = time.time()
            while GPIO.input(self.echo_pin) == 1:
                if time.time() - t1 > 0.038:
                    return float('inf')
                t2 = time.time()
            
            # 计算距离
            return (t2 - t1) * 34300 / 2  # 单位：厘米
        
        except Exception as e:
            print(f"[ERROR] 测量失败 @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
            return None

    def __del__(self):
        """析构时自动清理GPIO"""
        GPIO.cleanup()

# 使用示例
if __name__ == '__main__':

    sensor = HCSR04(trigger_pin=23, echo_pin=24) 
    
    try:
        print("超声波测距中...")
        while True:
            dist = sensor.measure()
            if dist == float('inf'):
                print("超出测量范围")
            elif dist is not None:
                print(f"距离: {dist:.2f} cm")  # 保持图片输出格式
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n测量结束")