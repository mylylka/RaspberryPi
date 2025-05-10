#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于HC-SR04超声波传感器的距离测量系统
该程序通过超声波传感器测量距离，并根据距离控制蜂鸣器报警
测量范围约为2cm-400cm，测量精度约为3mm
不同距离范围蜂鸣器会发出不同频率的警报声

硬件连接:
- 超声波传感器触发引脚(TRIG)连接到GPIO23
- 超声波传感器回声引脚(ECHO)连接到GPIO24
- 蜂鸣器控制引脚连接到GPIO25
"""

import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin, buzzer_pin=25):
        """初始化超声波传感器和蜂鸣器
        
        参数:
            trigger_pin: 触发引脚 (BCM编号)
            echo_pin: 回声引脚 (BCM编号)
            buzzer_pin: 蜂鸣器控制引脚 (BCM编号), 默认25
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.buzzer_pin = buzzer_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.buzzer_pin, GPIO.OUT, initial=GPIO.LOW)  # 初始化蜂鸣器引脚
        
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
            
            # 计算距离
            return (t2 - t1) * 34300 / 2  # 单位: 厘米
        
        except Exception as e:
            print(f"[ERROR] Measurement failed @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
            return None

    def control_buzzer(self, distance):
        """根据距离控制蜂鸣器
        """
        if distance is not None:
            if distance < 30:  # 近距离（0-30厘米）
                GPIO.output(self.buzzer_pin, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(self.buzzer_pin, GPIO.LOW)
                time.sleep(0.1)
            elif distance < 60:  # 中距离（30-60厘米）
                GPIO.output(self.buzzer_pin, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(self.buzzer_pin, GPIO.LOW)
                time.sleep(0.2)
            elif distance < 100:  # 远距离（60-100厘米）
                GPIO.output(self.buzzer_pin, GPIO.HIGH)
                time.sleep(0.4)
                GPIO.output(self.buzzer_pin, GPIO.LOW)
                time.sleep(0.4)
            else:  # 超过100厘米不报警
                GPIO.output(self.buzzer_pin, GPIO.LOW)

    def __del__(self):
        """销毁对象时自动清理GPIO资源"""
        GPIO.cleanup()

# 使用示例
if __name__ == '__main__':
    # 初始化传感器，设置触发引脚为23，回声引脚为24，蜂鸣器引脚为25
    sensor = HCSR04(trigger_pin=23, echo_pin=24, buzzer_pin=25)
    
    try:
        print("带蜂鸣器报警的超声波测距正在进行中...")
        while True:
            dist = sensor.measure()
            sensor.control_buzzer(dist)  # 控制蜂鸣器
            
            if dist == float('inf') or dist > 400:
                print("Out of measurement range")
            elif dist is not None:
                status = "Alarm" if dist < 20 else "Normal"  # 修正判断逻辑
                print(f"Distance: {dist:.2f} cm [{status}]")
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMeasurement ended")