import RPi.GPIO as GPIO
import time
from time import sleep
import pygame
import urllib.request

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

        
# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed, stat):
    if ch == CH1:
        #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        #pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmB, IN3, IN4, speed, stat)
  

GPIO.setmode(GPIO.BCM) # GPIO mode setting


#핀 설정후 PWM 핸들 얻어옴
GPIO.setwarnings(False)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

GPIO.setup(Button1, GPIO.IN) # BUtton1 Input
GPIO.setup(Button2, GPIO.IN) # BUtton2 Input

# --- setting -- 
client_id = ""
client_secret = ""

# --- 파일 저장 ---
def file_Save(text):
    print('file_Save() 함수 호출')
    encText = urllib.parse.quote(text) # tts 문자열

    data = "speaker=mijin&speed=0&text=" + encText;

    url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"

    request = urllib.request.Request(url)

    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)

    request.add_header("X-NCP-APIGW-API-KEY",client_secret)

    response = urllib.request.urlopen(request, data=data.encode('utf-8'))

    rescode = response.getcode()

    if(rescode==200):

        print("TTS mp3 저장")

        response_body = response.read()

        with open('checkingpic.mp3', 'wb') as f:

            f.write(response_body)

    else:

        print("Error Code:" + rescode)

    f.close()

    play()

# 파일 실행
def play():
    print('play() 함수 호출')
    print('음성 실행')
    music_file = "checkingpic.mp3"   # mp3 or mid file

    freq = 16000    # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)

    bitsize = -16   # signed 16 bit. support 8,-8,16,-16

    channels = 1   # 1 is mono, 2 is stereo

    buffer = 2048   # number of samples (experiment to get right sound) 


    pygame.mixer.init(freq, bitsize, channels, buffer)
    
    pygame.mixer.music.load(music_file)

    pygame.mixer.music.play()
     
    clock = pygame.time.Clock()

    while pygame.mixer.music.get_busy():

        clock.tick(30)

    pygame.mixer.quit()

# --- main ---
now = time.localtime(time.time()) # 현재 시간
pre_time1 = [now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour-1, now.tm_min]
pre_time2 = [now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour-1, now.tm_min]

def button_check(btn_str):
    print("button_check function")
    print("btn_str: ", btn_str)

    if btn_str == 'button1':
        if pre_time1[0]==now_time[0] and pre_time1[1]==now_time[1] and pre_time1[2]==now_time[2]:
            if now_time[3]-pre_time1[3]>=1 and now_time[4]>=pre_time1[4]:
                text = "한시간이 지났음"
                print(text)
                file_Save(text)
                return True
        
            else:
                text = "1번 간식을 먹은지 1시간이 지나지 않았습니다."
                print(text)
                file_Save(text)
                return False
                
    elif btn_str == 'button2':
        if pre_time2[0]==now_time[0] and pre_time2[1]==now_time[1] and pre_time2[2]==now_time[2]:
            if now_time[3]-pre_time2[3]>=1 and now_time[4]>=pre_time2[4]:
                print("한시간이 지났음")
                text = "한시간이 지났음"
                file_Save(text)
                return True
            
            else:
                text = "2번 간식을 먹은지 1시간이 지나지 않았습니다."
                print(text)
                file_Save(text)
                return False

try:
    while True:
        if GPIO.input(Button1)==0 or GPIO.input(Button2)==0:
            print("Button pressed!")
            now = time.localtime(time.time()) # 현재 시간
            now_time = [now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min]
            print("now: ", now_time)

        
            if GPIO.input(Button1)==0:
                print(pre_time1)
                print("Button1 pressed!")
                if button_check("button1") == True:
                    setMotor(CH1, 40, FORWARD)
                    sleep(3)
                    pre_time1 = now_time
                else:
                    setMotor(CH1, 80, STOP)

            elif GPIO.input(Button2)==0:
                print(pre_time2)
                print("Button2 pressed!")
                if button_check("button2") == True:
                    setMotor(CH2, 40, FORWARD)
                    sleep(3)
                    pre_time2 = now_time
                else:
                    setMotor(CH2, 80, STOP)
            
            setMotor(CH1, 80, STOP)
            setMotor(CH2, 80, STOP)
            sleep(1)
        else:
            print("Button not pressed!")
            sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
