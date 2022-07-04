#Korea Sejong Science High School 14th generation Exploring 2022
#Apply Doppler Effect - 조현진

# -*- coding: utf-8 -*-

# 0. 코드

#파이썬 버전 확인하기
#python -V (터미널)

#pip install ursina (터미널)

INPUT_INDEX = 17

import time
import math
from re import I
import pipes

print('pipes list')

import numpy as np
import scipy.io as sio
import scipy.io.wavfile
import matplotlib.pyplot as plt
import sounddevice as sd

from ursina import *

#1. 공간 및 개체 생성

if __name__ == '__main__':
        app = Ursina()

window.fps_counter.enabled = False

#공간
Sky()
ground = Entity(model='plane', texture='white_cube', scale=(100,1,100), collide='box')
ground.position=(0,-1,-1)

#개체1(관찰자)
player1 = Entity(model='cube', color=color.random_color(), scale=(1,2,1))
player1.position = (-5,0,0)

#개체2(파원)
player2 = Entity(model='cube', color=color.random_color(), scale=(1,2,1))
player2.position = (5,0,0)

speed1 = player1.speed =  100
speed2 = player2.speed =  100

#음성파일 재생
voice = Audio('voice')

#온도에 따른 음속
#0℃의 공기 중에서의 음속은 331.5m/s로 1℃ 상승할 때마다 0.6m/s씩 증가
T = 0
season = str(input('season: ')) 

if season == 'spring':
    T = 20
if season == 'summer':
    T = 36
if season == 'fall':
    T = 20
if season == 'winter':
    T = -10

vf = 331.5

if T > 0:
    vf = 331.5 + 0.6*T
if T == 0:
    vf = 331.5
if T < 0:
    vf = 331.5 + 0.6*T

distance = float()

distance_case = "거리의 증감"
decrease = "거리의 감소"
increase = "거리의 증가"

def update():

    global speed1
    global speed2

    player1.x += held_keys['d'] * time.dt * speed1
    player1.x -= held_keys['a'] * time.dt * speed1
    player1.y += held_keys['space'] * time.dt * speed1
    player1.y -= held_keys['shift'] * time.dt * speed1
    player1.z += held_keys['w'] * time.dt * speed1
    player1.z -= held_keys['s'] * time.dt * speed1

    player2.x += held_keys['k'] * time.dt * speed2
    player2.x -= held_keys['h'] * time.dt * speed2
    player2.y += held_keys['m'] * time.dt * speed2
    player2.y -= held_keys['n'] * time.dt * speed2
    player2.z += held_keys['u'] * time.dt * speed2
    player2.z -= held_keys['j'] * time.dt * speed2

    global x1
    global x2
    global y1
    global y2
    global z1
    global z2

    x1 = player1.x
    x2 = player2.x
    y1 = player1.y
    y2 = player2.y
    z1 = player1.z
    z2 = player2.z

    #좌표가 안변할때 speed를 0으로 만들기.
    xyz1 = "1의 좌표의 변화"
    xyz2 = "2의 좌표의 변화"
    if player1.x == 0:
       if player1.y == 0:
           if player1.z == 0:
               xyz1 = "no"

    if player2.x == 0:
        if player2.y == 0:
            if player2.z == 0:
                xyz2 = "no"
    
    if xyz1 == "no":
        speed1 = 0
    if xyz2 == "no":
        speed2 =0

    elif xyz1 is not "no":
        speed1 = 100
    elif xyz2 is not "no":
        speed2 = 100
        

    distance = math.sqrt(2*(x2-x1)+2*(y2-y1)+2*(z2-z1))

    distance_prev = distance

    #distance - distance_prev는 거리 변화량 : 도플러 효과

    class child_class(Entity):
        def dtc(self):
            if distance - distance_prev >0:
                distance_case == decrease
            if distance - distance_prev <0:
                distance_case == increase

    #2. 거리에 따른 소리의 크기

    #diameter: 배율
    diameter = int(distance/distance_prev)
    diameter_prev = diameter

    #diameter-diameter_prev는 거리변화 비율의 변화량

    n = int()

    if (diameter-diameter_prev)==n:
        voice.volume = voice.volume-n*0.6
    if (diameter-diameter_prev)>n:
        for i in range(diameter-diameter_prev):
            voice.volume = voice.volume-n*0.6

    if held_keys['p']:
        voice.play()
        
#Sample rate
#print( 'sampling rate: ', samplerate)

samplerate, data = sio.wavfile.read('voice.wav')
times = np.arange(len(data))/float(samplerate)
sd.play(data, samplerate)

plt.fill_between(times, data)
plt.xlim(times[0], times[-1])
plt.xlabel('time (s)')
plt.ylabel('amplitude')
plt.show()

# 3. 도플러 효과 적용 (소리의 높낮이)
#f는 파동의 진동수, bf는 바뀐 파동의 진동수이다.
#vf는 파동의 속도, vs는 파원의 속도, v0은 관찰자의 속도, 

f = samplerate

#vf는 위에 온도에 따른 음속에서 정의.

#3차원 공간 내에서의 개체의 속력은 일정하다.
player1.speed = player2.speed = vs = v0 = 10

#파원이 다가갈때, 관찰자가 다가갈때, 파원과 관찰자 모두 움직이는 경우

#파원이 이동할때
if player2.speed == 100:
    if distance_case == decrease:
        bf = f*(vf/vf-vs)
    if  distance_case == increase:
        bf = f*(vf/vf+vs)

#관찰자가 이동할때
if player1.speed == 100:
    if distance_case == decrease:
        bf = f*(vf-v0/vf)
    if  distance_case == increase:
        bf = f*(vf+v0/vf)

#둘 다 움직일때
if player1.speed == 100:
     if player2.speed == 100:
        if  distance_case == decrease:
            bf = f*(vf-v0/vf+vs)
        if  distance_case == increase:
            bf = f*(vf+v0/vf-vs)

bf = f = samplerate

#압력에 따른 한계 설정
P1 = 1
P2 = 1

if y1 <= 100:
    P1 = 1
else:
    P1 = 0
    
if y2 <= 100:
    P2 = 1
else:
    P2 = 0

if P1==0:
    voice.volume = 0
if P2==0:
    voice.volume = 0

if P1==1:
    voice.volume = 5
if P2==1:
    voice.volume = 5

app.run()
