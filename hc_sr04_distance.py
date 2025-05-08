#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        """初始化HC-SR04超声波传感器
        
        Args:
            trigger_pin: 触发信号引脚
            echo_pin: 回波信号引脚
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
        # 设置GPIO模式为BCM
        GPIO.setmode(GPIO.BCM)
        # 设置引脚模式
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # 确保触发引脚初始状态为低电平
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.1)  # 等待传感器稳定
    
    def measure_distance(self):
        """测量距离
        
        Returns:
            float: 测量到的距离（厘米），如果测量失败返回None
        """
        try:
            # 发送10us的触发信号
            GPIO.output(self.trigger_pin, True)
            time.sleep(0.00001)  # 10微秒
            GPIO.output(self.trigger_pin, False)
            
            # 等待回波信号
            pulse_start = time.time()
            timeout = pulse_start + 0.038  # 设置超时时间为38毫秒
            
            # 等待回波信号开始
            while GPIO.input(self.echo_pin) == 0:
                pulse_start = time.time()
                if pulse_start > timeout:
                    return None
            
            # 等待回波信号结束
            pulse_end = time.time()
            timeout = pulse_end + 0.038  # 重置超时时间
            
            while GPIO.input(self.echo_pin) == 1:
                pulse_end = time.time()
                if pulse_end > timeout:
                    return None
            
            # 计算时间差
            pulse_duration = pulse_end - pulse_start
            
            # 计算距离：声速为34300厘米/秒，来回距离需要除以2
            distance = pulse_duration * 34300 / 2
            
            # 返回距离，保留2位小数
            return round(distance, 2)
            
        except Exception as e:
            print(f"测量出错: {str(e)}")
            return None
    
    def cleanup(self):
        """清理GPIO设置"""
        GPIO.cleanup()

# 使用示例
def main():
    try:
        # 创建HCSR04实例，设置触发引脚为23，回波引脚为24
        sensor = HCSR04(trigger_pin=23, echo_pin=24)
        
        print("开始测量距离，按Ctrl+C退出...")
        
        while True:
            distance = sensor.measure_distance()
            if distance is not None:
                print(f"测量距离: {distance} 厘米")
            else:
                print("测量失败，请检查连接")
            
            # 等待0.5秒再次测量
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        sensor.cleanup()

if __name__ == "__main__":
    main()