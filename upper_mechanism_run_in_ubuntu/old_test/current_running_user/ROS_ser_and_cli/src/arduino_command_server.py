#!/usr/bin/env python
# this program get the msg sended from client ,which we manually input ,and then send it to arduino

#####################
### command guide ###
#####################

# topStepper  21 stop, 22 forward, 23 backward
# downStepper 31 stop, 32 forward, 33 backward
# Pusher      41 stop, 42 forward, 43 backward
# flywheel    51 stop, 52 shoot

# 0 , standard position
# 1 , taking basketball
# 2 , throwing basketball
# 3 , taking bowling
# 4 , relasing bowling

import rospy
from std_msgs.msg import Int8
import serial 
from time import sleep
from upper_control.srv import action,actionResponse 



def callback(request):
    actions = [0,1,21,22,23,31,32,33,41,42,43,51,52,53]
    if(request.request in actions): 
        
        # 如果 client 的 request 滿足要求 , send it to arduino
        ser.write(bytes(str(request.request), 'utf-8'))
        arduino_echo = ''
        while arduino_echo == '' :
            arduino_echo = ser.readline().decode('utf').strip()
        print("Arduino :" , arduino_echo)
    else :
        print('Arduino :invalid command')
        request.request = -1
        
    # 回傳response 給 client
    return actionResponse(request.request) 


if __name__ == '__main__':

    rospy.init_node('upper_mechanism')
    
    # connect to arduino board
    ser = serial.Serial('/dev/ttyUSB0',57600)
    ser.timeout = 3
    sleep(3)
    print('arduino board connected')
    
    try:
        while True:

            # client 丟了一個 request 進來 , 呼叫callback
            rospy.Service('upper_mechanism',action,callback) 
            rospy.spin()

    except rospy.ROSInterruptException:
        ser.close()
        print('\nend')
        exit()
