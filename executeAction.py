#import pythoncom, pyHook
from help_xml import *
from image_process import *

import os
import time
import win32api, win32con
from PIL import Image

from par import default_game_rect as win_rect

action_path_name = "action1"
repeat_time = 3
x_offset = win_rect[0]
y_offset = win_rect[1]

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print "Click"
    
def mousePos(cord):    
    win32api.SetCursorPos((x_offset+cord[0],y_offset+cord[1]))
    
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_offset
    y = y - y_offset
    print x,y

def set_cords(x,y):
    win32api.SetCursorPos(x,y)
    print x,y


#test_img = Image.open("img//event//action1.png")
#test_img.show()
'''
win2 = gameWindow()
win2.game_screen()
obj_img = Image.open("img//event//action1.png")
#obj_img.show()
win2.find_obj_in_point_old_screen(obj_img, (332,665))
'''
def main():
    win = gameWindow()
    win.game_screen()
      


    load = action_loader("img//event//"+"action1"+"//action.xml")
    all_action = load.get_all_action()
    for i in range(repeat_time):
        for action in all_action:
            obj_img = Image.open(action.get_image_path()).convert("L")
            point = action.get_position()
            while win.find_obj_in_point_old_screen(obj_img, point,(5,5)) is False:
                time.sleep(3)
            mousePos(action.position)
            leftClick()
            time.sleep(3)

    load = action_loader("img//event//"+"action2"+"//action.xml")
    all_action = load.get_all_action()
    for i in range(repeat_time):
        for action in all_action:
            obj_img = Image.open(action.get_image_path()).convert("L")
            point = action.get_position()
            while win.find_obj_in_point_old_screen(obj_img, point,(5,5)) is False:
                time.sleep(3)
            mousePos(action.position)
            leftClick()
            time.sleep(3)

    load = action_loader("img//event//"+"action3"+"//action.xml")
    all_action = load.get_all_action()
    for i in range(repeat_time):
        for action in all_action:
            obj_img = Image.open(action.get_image_path()).convert("L")
            point = action.get_position()
            while win.find_obj_in_point_old_screen(obj_img, point,(5,5)) is False:
                time.sleep(3)
            mousePos(action.position)
            leftClick()
            time.sleep(3)

    load = action_loader("img//event//"+"action4"+"//action.xml")
    all_action = load.get_all_action()
    for i in range(repeat_time):
        for action in all_action:
            obj_img = Image.open(action.get_image_path()).convert("L")
            point = action.get_position()
            while win.find_obj_in_point_old_screen(obj_img, point,(5,5)) is False:
                time.sleep(3)
            mousePos(action.position)
            leftClick()
            time.sleep(3)

    load = action_loader("img//event//"+"action5"+"//action.xml")
    all_action = load.get_all_action()
    for i in range(repeat_time):
        for action in all_action:
            obj_img = Image.open(action.get_image_path()).convert("L")
            point = action.get_position()
            while win.find_obj_in_point_old_screen(obj_img, point,(5,5)) is False:
                time.sleep(3)
            mousePos(action.position)
            leftClick()
            time.sleep(3)
            
    load = action_loader("img//event//"+"action6"+"//action.xml")
    all_action = load.get_all_action()
    for i in range(repeat_time):
        for action in all_action:
            obj_img = Image.open(action.get_image_path()).convert("L")
            point = action.get_position()
            while win.find_obj_in_point_old_screen(obj_img, point,(5,5)) is False:
                time.sleep(3)
            mousePos(action.position)
            leftClick()
            time.sleep(3)

if __name__ == '__main__':
    main()