#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gpiozero import DistanceSensor
from time import sleep

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        """初始化HC-SR04超声波传感器
        
        Args:
            trigger_pin: 触发信号引脚
            echo_pin: 回波信号引脚
        """
        # 使用gpiozero的DistanceSensor类初始化传感器
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)
    
    def measure_distance(self):
        """测量距离
        
        Returns:
            float: 测量到的距离（厘米），如果测量失败返回None
        """
        try:
            # 获取距离（米）并转换为厘米
            distance = self.sensor.distance * 100
            # 返回距离，保留2位小数
            return round(distance, 2)
            
        except Exception as e:
            print(f"测量出错: {str(e)}")
            return None
    
    def cleanup(self):
        """清理传感器资源"""
        self.sensor.close()

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
            sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        sensor.cleanup()

if __name__ == "__main__":
    main()