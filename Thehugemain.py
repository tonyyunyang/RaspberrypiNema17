# Libraries
import RPi.GPIO as GPIO
import time
import array as arr

# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER1 = 14
GPIO_TRIGGER2 = 18
GPIO_TRIGGER3 = 24
GPIO_TRIGGER4 = 8
GPIO_ECHO1 = 15
GPIO_ECHO2 = 23
GPIO_ECHO3 = 25
GPIO_ECHO4 = 7
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)  # set GPIO (IN / OUT)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER4, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_ECHO3, GPIO.IN)
GPIO.setup(GPIO_ECHO4, GPIO.IN)
# Above is the definition for ultrasonic sensors

# Below is the definition for motor movement and signal receiving and processing
GPIO.setup(5, GPIO.IN)  # input channel 3 for left right
GPIO.setup(6, GPIO.IN)  # input channel 4 for front back

GPIO.setup(17, GPIO.OUT)  # output pin 27 for motor 1 enable
GPIO.setup(27, GPIO.OUT)  # output pin 27 for motor 1 direction
GPIO.setup(22, GPIO.OUT)  # output pin 22 for motor 1 step
# Ground above GPIO.17 reserved for motor 1
GPIO.setup(16, GPIO.OUT)  # output pin 27 for motor 2 enable
GPIO.setup(20, GPIO.OUT)  # output pin 27 for motor 2 direction
GPIO.setup(21, GPIO.OUT)  # output pin 22 for motor 2 step
# Ground above GPIO.16 reserved for motor 2

# Below is value definition for ultrasonic sensors
# starttime4 = 0
# stoptime4 = 0
# timeelapsed4 = 0
# distance4 = 0
# count4 = 0
# av4 = arr.array('f', [0]*10)
# average4 = 0
# flag4 = False
# waittime = 0.0001

# Below is value definition for crawler movement
sig1 = False
sig2 = False
sig3 = False
sig4 = False
T1 = 0.0001
T2 = 0.000199
ch3start = 0
ch3high = False
ch3dif = 0
ch3div = 0
ch3val = 0  # stable value channel 3

ch4start = 0
ch4high = False
ch4dif = 0
ch4div = 0
ch4val = 0  # stable value channel 4

asize = 10
c3 = 0  # counter for array3
a3 = arr.array('f', [0] * asize)
s3 = 0  # sum for array3

c4 = 0  # counter for array4
a4 = arr.array('f', [0] * asize)
s4 = 0  # sum for array4

steppulseduration = 0.0001

motor1pulsestart = 0
motor1minsteptime = 0.0004  # maximum speed
motor1steptime = 0.0004  # actual speed
motor1endval = 0
motor1speed = 0

motor2pulsestart = 0
motor2minsteptime = 0.0004  # maximum speed
motor2steptime = 0.0004  # actual speed
motor2endval = 0
motor2speed = 0

# Below is the code for the ultrasonic sensors detecting


def length1():
    GPIO.output(GPIO_TRIGGER1, True)  # Set trigger to HIGH
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER1, False)  # Set trigger after 0.01ms to LOW
    starttime1 = time.time()
    stoptime1 = time.time()
    if GPIO.input(GPIO_ECHO1) == 0:  # The if case was while before, lets see what will happen with if
        starttime1 = time.time()
    if GPIO.input(GPIO_ECHO1) == 1:  # The if case was while before, lets see what will happen with if
        stoptime1 = time.time()
    timeelapsed1 = stoptime1 - starttime1
    distance1 = (timeelapsed1 * 34300) / 2  # Multiply with the sonic speed 34300cm/s
    return distance1


def length2():
    GPIO.output(GPIO_TRIGGER2, True)  # Set trigger to HIGH
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER2, False)  # Set trigger after 0.01ms to LOW
    starttime2 = time.time()
    stoptime2 = time.time()
    if GPIO.input(GPIO_ECHO2) == 0:  # The if case was while before, lets see what will happen with if
        starttime2 = time.time()
    if GPIO.input(GPIO_ECHO2) == 1:  # The if case was while before, lets see what will happen with if
        stoptime2 = time.time()
    timeelapsed2 = stoptime2 - starttime2
    distance2 = (timeelapsed2 * 34300) / 2  # Multiply with the sonic speed 34300cm/s
    return distance2


def length3():
    GPIO.output(GPIO_TRIGGER3, True)  # Set trigger to HIGH
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER3, False)  # Set trigger after 0.01ms to LOW
    starttime3 = time.time()
    stoptime3 = time.time()
    if GPIO.input(GPIO_ECHO3) == 0:  # The if case was while before, lets see what will happen with if
        starttime3 = time.time()
    if GPIO.input(GPIO_ECHO3) == 1:  # The if case was while before, lets see what will happen with if
        stoptime3 = time.time()
    timeelapsed3 = stoptime3 - starttime3
    distance3 = (timeelapsed3 * 34300) / 2  # Multiply with the sonic speed 34300cm/s
    return distance3


def length4():
    GPIO.output(GPIO_TRIGGER4, True)  # Set trigger to HIGH
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER4, False)  # Set trigger after 0.01ms to LOW
    starttime4 = time.time()
    stoptime4 = time.time()
    if GPIO.input(GPIO_ECHO4) == 0:  # The if case was while before, lets see what will happen with if
        starttime4 = time.time()
    if GPIO.input(GPIO_ECHO4) == 1:  # The if case was while before, lets see what will happen with if
        stoptime4 = time.time()
    timeelapsed4 = stoptime4 - starttime4
    distance4 = (timeelapsed4 * 34300) / 2  # Multiply with the sonic speed 34300cm/s
    return distance4


def signal1():
    count1 = 0
    av1 = []
    while count1 < 10:
        av1[count1] = length1()
        count1 = count1 + 1
        waittime = 0.0001
        time.sleep(waittime)
    average1 = sum(av1) / len(av1)
    if average1 < 50:
        flag1 = False
    else:
        flag1 = True
    return flag1


def signal2():
    count2 = 0
    av2 = []
    while count2 < 10:
        av2[count2] = length2()
        count2 = count2 + 1
        waittime = 0.0001
        time.sleep(waittime)
    average2 = sum(av2) / len(av2)
    if average2 < 50:
        flag2 = False
    else:
        flag2 = True
    return flag2


def signal3():
    count3 = 0
    av3 = []
    while count3 < 10:
        av3[count3] = length3()
        count3 = count3 + 1
        waittime = 0.0001
        time.sleep(waittime)
    average3 = sum(av3) / len(av3)
    if average3 < 50:
        flag3 = False
    else:
        flag3 = True
    return flag3


def signal4():
    count4 = 0
    av4 = []
    while count4 < 10:
        av4[count4] = length4()
        count4 = count4 + 1
        waittime = 0.0001
        time.sleep(waittime)
    average4 = sum(av4) / len(av4)
    if average4 < 50:
        flag4 = False
    else:
        flag4 = True
    return flag4


while True:
    if GPIO.input(5) == True:
        if ch3high == False:
            ch3start = time.time()
            ch3high=True
    else:
        if ch3high == True:
            ch3high = False
            ch3dif = ((time.time() - ch3start)*1000)-1.5 + ch3div
            if ch3dif > 0.6:
                ch3dif = a3[c3]
            if ch3dif < -0.6:
                ch3dif = a3[c3]
            s3 = s3 - a3[c3] + ch3dif
            a3[c3] = ch3dif

            c3 = c3+1
            if c3 > (asize-1):
                c3 = 0
            ch3val = 2*s3/asize

            if -1 < (ch4val+ch3val) < 1:
                motor1speed = ch4val+ch3val
            else:
                if (ch4val + ch3val) > 0:
                    motor1speed = 1
                else:
                    motor1speed = -1

            if -1 < (ch4val-ch3val) < 1:
                motor2speed = ch4val-ch3val
            else:
                if (ch4val - ch3val) > 0:
                    motor2speed = 1
                else:
                    motor2speed = -1
            print ('%.4f'% ch3val, '%.4f'% ch4val)

    if GPIO.input(6) == True:
        if ch4high == False:
            ch4start = time.time()
            ch4high=True
    else:
        if ch4high == True:
            ch4high = False
            ch4dif = ((time.time() - ch4start)*1000)-1.5 + ch4div
            if ch4dif > 0.6:
                ch4dif = a4[c4]
            if ch4dif < -0.6:
                ch4dif = a4[c4]
            s4 = s4 - a4[c4] + ch4dif
            a4[c4] = ch4dif

            c4 = c4+1
            if c4 > (asize-1):
                c4 = 0
            ch4val = 2*s4/asize
            if -1 < (ch4val+ch3val) < 1:
                motor1speed = ch4val+ch3val
            else:
                if (ch4val + ch3val) > 0:
                    motor1speed = 1
                else:
                    motor1speed = -1

            if -1 < (ch4val-ch3val) < 1:
                motor2speed = ch4val-ch3val
            else:
                if (ch4val - ch3val) > 0:
                    motor2speed = 1
                else:
                    motor2speed = -1

            print ('%.4f'% ch3val, '%.4f'% ch4val)

    #sig1 = signal1()
    #sig2 = signal2()
    #sig3 = signal3()
    #sig4 = signal4()
    if motor1speed < 0:
        GPIO.output(27,GPIO.HIGH) # LOW for backwards & HIGH for forward
    else:
        GPIO.output(27,GPIO.LOW) # LOW for backwards & HIGH for forward

    if motor2speed < 0:
        GPIO.output(20,GPIO.HIGH) # LOW for backwards & HIGH for forward
    else:
        GPIO.output(20,GPIO.LOW) # LOW for backwards & HIGH for forward

    if -0.2 < motor1speed < 0.2: #disables when the joystick is in the middle
        GPIO.output(17,GPIO.HIGH) # LOW for enable & HIGH for disable
    else:
        GPIO.output(17,GPIO.LOW) # LOW for enable & HIGH for disable
        motor1steptime = motor1minsteptime/abs(motor1speed)

    if -0.2 < motor2speed < 0.2: #disables when the joystick is in the middle
        GPIO.output(16,GPIO.HIGH) # LOW for enable & HIGH for disable
    else:
        GPIO.output(16,GPIO.LOW) # LOW for enable & HIGH for disable
        motor2steptime = motor2minsteptime/abs(motor2speed)
    # the two motor turns in the same direction, but when you put them opposite to each other
    # ,they rotate reversely, the solution is to reversly one phase physically
    if (time.time() - motor1pulsestart) > motor1steptime:
        GPIO.output(22,GPIO.HIGH) # motor 1 step
        GPIO.output(21,GPIO.HIGH) # motor 2 step
        motor1pulsestart = time.time()
    if (time.time() - motor1pulsestart) > steppulseduration:
        GPIO.output(22,GPIO.LOW) # motor 1 step
        GPIO.output(21,GPIO.LOW) # motor 2 step

GPIO.cleanup() # cleanup all GPIO
