# 典型应用
![典型应用](./pics/usage.GIF)
# 超声波
蝙蝠发射超声波，遇到目标后产生回波。通过分析回波时间和强度，可以精确判断目标位置。
![回声定位](https://ts1.tc.mm.bing.net/th/id/R-C.4edea0a3749ec417b9e6bc3985db5adb?rik=i4TZ5eLrkpyjig&riu=http%3a%2f%2fn.sinaimg.cn%2fsinakd20123%2f98%2fw1098h600%2f20210119%2fac13-khxeamv6555224.jpg&ehk=E3miaUbFGpNv7bA0ejWbwbnTovzi%2bUhHetPddhJ9sLk%3d&risl=&pid=ImgRaw&r=0)

## 什么是超声波？
超声波是一种高音调声波，其频率超出了人类听觉的可听范围。

人类可以听到每秒振动约20次（低沉的隆隆声）至每秒20,000次（高音调的哨声）的声波。然而，超声波的频率超过20,000Hz，因此人类听不见。

### 超声波频率范围频谱
![超声波频率范围](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5EQAe1jusBQSgNOJQbR0Qib9H2g5iclyiaibbM92a3LRppjLPCHrgkp3yKFw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)
# Raspberry Pi GPIO教程-超声波传感器

本文介绍HC-SR04超声波传感器的原理和如何使用Raspberry Pi的GPIO来使用该传感器。

HC-SR04超声波距离传感器可以报告最远4米外的物体范围。当您试图防止机器人撞到墙壁时，这是一件好事。它们功率低（适用于电池供电的设备）、价格实惠、易于连接，并且非常受业余爱好者的欢迎。


## HC-SR04硬件概述
HC-SR04超声波距离传感器实际上由两个超声波换能器(Transducer)组成。一个用作发射器，将电信号转换为40KHz超声波脉冲。另一个用作接收器，监听发射的脉冲。当接收器接收到这些脉冲时，它会产生一个输出脉冲，其宽度与前方物体的距离成正比。

该传感器可提供2厘米至400厘米之间出色的非接触式范围检测，精度为3毫米。

由于它采用5伏电压运行，因此可以直接连接到Raspberry Pi或其他5V的逻辑微控制器。

### 技术规格
|操作电压|DC 5V|
|----|----|
|操作电流|15mA|
|操作频率|40KHz|
|最大检测范围|4m|
|最小检测范围|2cm|
|精度|3mm|
|量测角度|15 degree|
|触发输入信号|10µS TTL pulse|
|尺寸|45 x 20 x 15mm|

### HC-SR04超声波传感器引脚

![超声波传感器引脚](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5Eib4eS6vJPUnulx9DA3xTHdgfW6uOAmicwpQx4OArcpD6g1EH4tfUAWog/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)

VCC —— 为HC-SR04超声波传感器供电。您可以将其连接到Raspberry Pi的5V输出。

Trig —— 用于触发超声波脉冲。通过将此引脚设置为高电平10µs，传感器将启动超声波脉冲。

Echo —— 当超声波脉冲发射时，Echo引脚变为高电平，并保持高电平直到传感器接收到回声，之后变为低电平。通过测量Echo引脚保持高电平的时间，可以计算出距离。

GND —— 接地引脚。可以将其连接到Raspberry Pi的接地。

## HC-SR04超声波距离传感器如何工作？
当触发引脚设置为高电平10µs时，一切就开始了。作为响应，传感器以40kHz的频率发射八个脉冲的超声波脉冲。这种8脉冲模式经过特殊设计，以便接收器能够区分发射脉冲和环境超声波噪声。

这八个超声波脉冲通过空气传播，远离发射器。同时，回声引脚变为高电平以启动回声信号。

如果这些脉冲没有被反射回来，回波信号就会超时并在38ms（38毫秒）后变低。因此，38ms的脉冲表示传感器范围内没有障碍物。

![无障碍物](https://mmbiz.qpic.cn/sz_mmbiz_gif/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5EHVnDy0veaIYrGdrI4BQtnARuuMia02icbuW2ccVJPALG3UszMvMr2w8Q/640?wx_fmt=gif&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)

如果这些脉冲被反射回来，回声引脚在收到信号后会立即变低。这会在回声引脚上产生一个脉冲，其宽度具体取决于接收信号所需的时间。

![有障碍物](https://mmbiz.qpic.cn/sz_mmbiz_gif/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5E9ZhOTsqia0NcJatP58Eb2qW5xfDHWjz4QL0NjopNMqsPiaLu3Yk8pRUg/640?wx_fmt=gif&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)

## 计算距离
接收脉冲的宽度用于计算与反射物体的距离。这可以使用我们在高中学到的简单的距离-速度-时间方程来计算。记住这个方程的一个简单方法是将字母放在三角形中。

![距离三角形](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5Eg8g9klNznbYqYU5Rg7C89IEDuiaDniaDh9W22KYG4icGBxoKataEf1iagA/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)  

让我们举个例子来更清楚一点。假设我们在传感器前面有一个距离未知的物体，我们在回声引脚上接收到一个宽度为500µs的脉冲。现在让我们计算一下物体与传感器之间的距离。为此，我们将使用以下公式。

距离 = 速度 x 时间

这里我们有时间值，即500µs，我们知道速度。当然是声速！它是340m/s。要计算距离，我们需要将声速转换为cm/µs。它是0.034cm/μs。有了这些信息，我们现在可以计算距离了！

距离 = 0.034 cm/µs x 500 µs

但我们还没有完成！请记住，回声脉冲表示信号发送和反射回来所需的时间。因此，要得到距离，您必须将结果除以二。

距离 = (0.034 cm/µs x 500 µs) / 2 = 8.5cm

## 接线
将HC-SR04连接到Pi非常简单。将VCC引脚连接到Pi的5V引脚，将GND引脚连接到接地引脚。现在将触发和回声引脚分别连接到GPIO引脚23和24。
![接线示例图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5E20DKOayz822gsPyQV5RANkVC0oN9RibwcvpEYLAJtgcJMicFo5jpZwpQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)

## 超声波测距核心代码
输入以下代码：
```python
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

    # 计算距离：声速为34300厘米/秒（室温20°C），来回距离需要除以2
    distance = pulse_duration * 34300 / 2

    # 返回距离，保留2位小数
    return round(distance, 2)

```
### 运行结果示意(用手靠近远离传感器）

## 添加蜂鸣器报警功能
为了增加一个简单的报警功能，我们可以在超声波传感器的基础上添加一个蜂鸣器模块。当检测到的距离超过20厘米时，蜂鸣器将发出报警声。

### 蜂鸣器接线说明
蜂鸣器模块有两个引脚：
- VCC：连接到树莓派的5V电源
- GND：连接到树莓派的地线（GND）
- SIGNAL：信号线，连接到GPIO 25（BCM编号）

### 完整接线图
![接线示意图](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5EQAe1jusBQSgNOJQbR0Qib9H2g5iclyiaibbM92a3LRppjLPCHrgkp3yKFw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)

### 使用带蜂鸣器的代码
新的Python代码文件`hc_sr04_distance_with_buzzer.py`在原有测距功能的基础上增加了蜂鸣器控制。当检测到的距离超过20厘米时，蜂鸣器会发出报警声。

运行方法：
```bash
python3 hc_sr04_distance_with_buzzer.py
```

## 有哪些局限性？
HC-SR04超声波传感器在精度和整体可用性方面确实非常出色，尤其是与其他低成本超声波传感器相比。这并不意味着HC-SR04传感器将会一直很好地工作。下图显示了HC-SR04的一些局限性：
1. 传感器与物体/障碍物之间的距离大于4米(13ft)。
![示例图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5EDl8ibKcPzTaQ7MDBqrJr6cfYOtMcCfGRouWnQEMggRXl2hYgotiblyYA/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)
2. 物体的反射面角度较小，因此声音不会反射回传感器。
![示例图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5EGF8WkEwbjktJVXgd4bJUgkhticMRib3ssv1ja39QjZ1NbVcrTyql1Uicw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)
3. 物体太小，无法将足够多的声音反射回传感器。另外，如果您的HC-SR04传感器安装在设备上较低位置，则可能接收到从地板反射的声音。
![示例图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5E8wzgLna1kElLdicWpAqJ7Q9DDzwmPJmJ7icAsWFOp6CCMDPwXA3RIiaAQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)
4. 一些表面柔软、不规则的物体（例如毛绒动物）会吸收声音而不是反射声音，因此HC-SR04传感器可能难以检测到此类物体。
![示例图片](https://mmbiz.qpic.cn/sz_mmbiz_png/Ao0SjpaEmUK9SEA4ROibx8e1rVcDPuL5E74ibmeyk4eib1raka3GXR4ic084NtQFWLC70e3avEyxoPF24PRv0Bdjicw/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1)
