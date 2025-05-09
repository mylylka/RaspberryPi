#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin, buzzer_pin=25):
        """Initialize ultrasonic sensor and buzzer
        
        Args:
            trigger_pin: Trigger pin (BCM numbering)
            echo_pin: Echo pin (BCM numbering)
            buzzer_pin: Buzzer control pin (BCM numbering), default 25
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.buzzer_pin = buzzer_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.buzzer_pin, GPIO.OUT, initial=GPIO.LOW)  # Initialize buzzer pin
        
        time.sleep(2)  # Sensor stabilization time

    def measure(self):
        """Execute distance measurement"""
        try:
            # Send trigger signal
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)  # 10μs pulse
            GPIO.output(self.trigger_pin, GPIO.LOW)
            t0 = time.time()
            
            # Wait for echo to go out
            while GPIO.input(self.echo_pin) == GPIO.LOW:
                if time.time() - t0 > 0.038:
                    return float('inf')
            
            # Record emission time
            t1 = time.time()

            # Wait for echo to return
            while GPIO.input(self.echo_pin) == GPIO.HIGH:
                if time.time() - t0 > 0.038:
                    return float('inf')
            
            t2 = time.time()
            
            # Calculate distance
            return (t2 - t1) * 34300 / 2  # Unit: centimeters
        
        except Exception as e:
            print(f"[ERROR] Measurement failed @ {time.strftime('%Y-%m-%d %H:%M:%S')}: {str(e)}")
            return None

    def control_buzzer(self, distance, threshold=20):
        """Control buzzer based on distance
        
        Args:
            distance: Measured distance (cm)
            threshold: Alarm threshold (cm), default 20cm
        """
        if distance is not None:
            if distance > threshold:
                GPIO.output(self.buzzer_pin, GPIO.HIGH)  # Activate buzzer
            else:
                GPIO.output(self.buzzer_pin, GPIO.LOW)   # Deactivate buzzer

    def __del__(self):
        """Automatically clean up GPIO on destruction"""
        GPIO.cleanup()

# 使用示例
if __name__ == '__main__':
    sensor = HCSR04(trigger_pin=23, echo_pin=24, buzzer_pin=25)
    
    try:
        print("Ultrasonic distance measurement with buzzer alarm in progress...")
        while True:
            dist = sensor.measure()
            sensor.control_buzzer(dist, threshold=20)  # Control buzzer
            
            if dist == float('inf') or dist > 400:
                print("Out of measurement range")
            elif dist is not None:
                status = "ALARM" if dist > 20 else "NORMAL"
                print(f"Distance: {dist:.2f} cm [{status}]")
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMeasurement ended")    