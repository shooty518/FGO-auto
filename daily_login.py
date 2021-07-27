



import threading

import cv2
import os
import random
import numpy as np
import time



def get_randtime(a, b):
    """产生a,b间的随机时间延迟"""
    time.sleep(random.uniform(a, b))

def get_screen(x):
    #截屏口令
    cmd_get = 'adb -s {} shell screencap -p /sdcard/screen_img{}.png'.format(x,x)
    #发送图片口令
    cmd_send = 'adb -s {} pull sdcard/screen_img{}.png C:/Users/kai/Downloads/YYS-master'.format(x,x)
    #截屏和发送操作
    os.system(cmd_get)
    os.system(cmd_send)
    img = cv2.imread('C:/Users/kai/Downloads/YYS-master/screen_img{}.png'.format(x),0)
    return img

def click(addr,x,y):
    cmd_click = 'nox_adb -s {} shell input tap {} {}'.format(addr,x,y)
    os.system(cmd_click)

    

def matchEnd(imgin, template):
    """img1代表待匹配图像, img2代表模板"""
    res = cv2.matchTemplate(imgin,template,cv2.TM_CCOEFF_NORMED)
    # print(res.max())
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    left_top = max_loc  # 左上角
    return left_top , max_val
    # print(left_top,'\n')
    
    
def open_Simulator(x):
    cmd_open = "Nox.exe -clone:Nox_{}".format(x) #x 就是編號
    os.popen(cmd_open)



def Simulator_check(number,addr):
    text="{}\tdevice\n".format(addr)
    devices_check=os.popen("adb devices").readlines()
    while(True):
        if text in devices_check:
            print("ok")
            get_randtime(5, 10)
            break
        else:
            open_Simulator(number)
            get_randtime(20, 50)
            text="{}\tdevice\n".format(addr)
            devices_check=os.popen("adb devices").readlines()

class Daily_longin_check:

            
    def game_check(self,addr,threadhold):
        
        os.system("nox_adb -s {} shell am start -n com.komoe.fgomycard/jp.delightworks.Fgo.player.AndroidPlugin".format(addr))
        get_randtime(10,20)
        print("1")
        while(True):#進入遊戲
            get_randtime(1,10)
            res=get_screen(addr)
            template = cv2.imread("./allimg/update.png", 0)
            left_top , max_val =matchEnd(res,template)
            if max_val>threadhold:
                click(addr,left_top[0],left_top[1])
                get_randtime(10,20)
            else:
                get_randtime(1,3)
            res=get_screen(addr)
            template = cv2.imread("./allimg/first_scr.png", 0)
            left_top , max_val =matchEnd(res,template)
            if max_val>threadhold:
                click(addr,left_top[0],left_top[1])
                get_randtime(1,3)
                break
            else:
                get_randtime(5,20)
                continue
        print("2")#主畫面
        while(True):
            get_randtime(1,3)
            res=get_screen(addr)
            template = cv2.imread("C:/Users/kai/Downloads/YYS-master/allimg/change.png", 0)
            left_top , max_val =matchEnd(res,template)
            if max_val>threadhold:
                get_randtime(1,3)
            else:
                pass
            get_randtime(5,10)
            res=get_screen(addr)
            template = cv2.imread("C:/Users/kai/Downloads/YYS-master/allimg/sec_scr.png", 0)
            left_top , max_val =matchEnd(res,template)
            if max_val>threadhold:
                click(addr,left_top[0],left_top[1])
                
                break
            else:
                continue
            
        print("3")#關公告
        while(True):
            get_randtime(5,10)
            res=get_screen(addr)
            template = cv2.imread("C:/Users/kai/Downloads/YYS-master/allimg/announcement_close.png", 0)
            left_top , max_val =matchEnd(res,template)
           
            if max_val>threadhold:
                click(addr,left_top[0],left_top[1])
                break
            else:
                continue
        while(True):
            get_randtime(1,3)
            res=get_screen(addr)
            template = cv2.imread("C:/Users/kai/Downloads/YYS-master/allimg/close.png", 0)
            left_top , max_val =matchEnd(res,template)
           
            if max_val>threadhold:
                click(addr,left_top[0],left_top[1])
                break
            else:
                res=get_screen(addr)
                template = cv2.imread("C:/Users/kai/Downloads/YYS-master/allimg/man.png", 0)
                left_top , max_val =matchEnd(res,template)
                if max_val>threadhold:
                    click(addr,left_top[0],left_top[1])
                break
                
# addrs = ["127.0.0.1:62001","127.0.0.1:62025","127.0.0.1:62026"]

# def job(num):
#     print("Thread", num)
#     Simulator_check(num,addrs[num])
#     text.game_check(addrs[num],0.8)

# # 建立 5 個子執行緒
# threads = []

# # get_randtime(20,30)


# text=Daily_longin_check()


# for i in range(3):
#   threads.append(threading.Thread(target = job, args = (i,)))
#   threads[i].start()

# # # 主執行緒繼續執行自己的工作
# # # ...

# # 等待所有子執行緒結束
# for i in range(3):
#   threads[i].join()

# print("Done.")

get_randtime(20,30)

Simulator_check(0,"127.0.0.1:62001")
Simulator_check(1,"127.0.0.1:62025")
Simulator_check(2,"127.0.0.1:62026")

text=Daily_longin_check()

text.game_check("127.0.0.1:62001",0.8)
text.game_check("127.0.0.1:62025",0.8)
text.game_check("127.0.0.1:62026",0.8)