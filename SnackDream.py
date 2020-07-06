import RPi.GPIO as GPIO
from time import sleep

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWORD = 2

# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 26  #37 pin
ENB = 0   #27 pin

#GPIO PIN
IN1 = 19  #37 pin
IN2 = 13  #35 pin
IN3 = 6   #31 pin
IN4 = 5   #29 pin

Button1 = 18
Button2 = 15

#핀 설정 함수
def setPinConfig(EN, INA, INB):        
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100khz 로 PWM 동작 시킴 
    pwm = GPIO.PWM(EN, 100) 
    # 우선 PWM 멈춤.   
    pwm.start(0) 
    return pwm

# 모터 제어 함수
def setMotorContorl(pwm, INA, INB, speed, stat):

    #모터 속도 제어 PWM
    pwm.ChangeDutyCycle(speed)  
    
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
        
    #뒤로
    elif stat == BACKWORD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
        
    #정지
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)

        
# 모터 제어함수 간단하게 사용하기 위해 한번 더 래핑
def setMotor(ch, speed, stat):
    if ch == CH1:
        #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        #pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값
        setMotorContorl(pwmB, IN3, IN4, speed, stat)
  

GPIO.setmode(GPIO.BCM) # GPIO mode setting


#핀 설정후 PWM 핸들 얻어옴
GPIO.setwarnings(False)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

GPIO.setup(Button1, GPIO.IN) # BUtton1 Input
GPIO.setup(Button2, GPIO.IN) # BUtton2 Input

try:
    while True:
        if GPIO.input(Button1)==0:
            print("Button1 pressed!")
            setMotor(CH1, 40, FORWARD)
            sleep(3)
        elif GPIO.input(Button2)==0:
            print("Button2 pressed!")
            setMotor(CH2, 40, FORWARD)
            sleep(3)
        else:
            print("Button not pressed")
            setMotor(CH1, 80, STOP)
            setMotor(CH2, 80, STOP)
        sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
