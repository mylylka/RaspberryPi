#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
超声波测距系统 - 使用HC-SR04传感器与蜂鸣器报警

该程序通过HC-SR04超声波传感器测量距离，并根据设定的阈值控制蜂鸣器报警。

硬件连接：
- HC-SR04传感器触发引脚(TRIG)连接到GPIO23
- HC-SR04传感器回声引脚(ECHO)连接到GPIO24
- 有源蜂鸣器控制引脚连接到GPIO25
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
        """执行距离测量
        返回:
            测量的距离值(厘米)，超出范围返回无穷大
        """
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
            return (t2 - t1) * 34300 / 2  # 单位: 厘米
        
        except Exception as e:
            print(f"[ERROR] Measurement failed @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
            return None

    def control_buzzer(self, distance, threshold=20):
        """根据距离控制蜂鸣器
        
        参数:
            distance: 测量的距离(厘米)
            threshold: 报警阈值(厘米)，默认20厘米
        """
        if distance is not None:
            if distance > threshold:
                GPIO.output(self.buzzer_pin, GPIO.HIGH)  # 激活蜂鸣器
            else:
                GPIO.output(self.buzzer_pin, GPIO.LOW)   # 关闭蜂鸣器

    def __del__(self):
        """销毁对象时自动清理GPIO资源
        确保程序结束时正确释放GPIO引脚
        """
        GPIO.cleanup()

# 使用示例
if __name__ == '__main__':
    # 初始化传感器，设置触发引脚为23，回声引脚为24，蜂鸣器引脚为25
    sensor = HCSR04(trigger_pin=23, echo_pin=24, buzzer_pin=25)
    
    try:
        print("Ultrasonic distance measurement with buzzer alarm in progress...")
        while True:
            # 测量距离
            dist = sensor.measure()
            # 根据距离和阈值控制蜂鸣器
            sensor.control_buzzer(dist, threshold=20)
            
            if dist == float('inf') or dist > 400:
                print("Out of measurement range")
            elif dist is not None:
                # 根据距离与阈值比较显示状态
                status = "ALARM" if dist > 20 else "NORMAL"
                print(f"Distance: {dist:.2f} cm [{status}]")
            
            # 每隔0.5秒测量一次
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMeasurement ended")