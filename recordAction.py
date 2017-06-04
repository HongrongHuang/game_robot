import pythoncom, pyHook

from help_xml import *

from par import default_game_rect as window

import ImageGrab
from PIL import Image
import time


screen_image = ImageGrab.grab()
mouse_global_pos = (0,0)
mouse_local_pos = (0,0)
previous_mouse_local_pos = mouse_local_pos

sceneRecorder = screen_recorder()
scene_global_id_counter = 0
scene_name_gl = "temp"
scene_save_image_path = "img//element//temp//"
scene_record_active = True
scene_save_xml_path = "img//element//" + scene_name_gl + ".xml"

actionRecorder = action_recorder()
action_global_id_counter = 0

def check_mouse_is_moved():
    global previous_mouse_local_pos
    retval = False
    if previous_mouse_local_pos == mouse_local_pos:
        retval = False
    else:
        retval = True            
    previous_mouse_local_pos = mouse_local_pos    
    return retval
    
def scene_ref_img_name_gen(scene_name,scene_id,ref_img_nr=None):
    retval = ""
    retval += scene_save_image_path
    retval += scene_name
    retval += "_"
    retval += str(scene_id)
    if ref_img_nr is not None:
        retval += "_"
        retval += str(ref_img_nr)
    retval += ".png"
    return retval
    
def scene_name_gen(scene_name,scene_id=None):
    retval = ""
    retval += scene_name
    retval += "_"
    if scene_id is not None:
        retval += str(scene_id)
    return retval
    
def save_point_img(point,path):
    left   = point[0] - 5 + window[0]
    top    = point[1] - 5 + window[1]
    right  = point[0] + 5 + window[0]
    bottom = point[1] + 5 + window[1]
    rect = (left,top,right, bottom )
    ImageGrab.grab().crop(rect).save(path)

def save_point_img_no_screengrap(point,path):
    left   = point[0] - 5 + window[0]
    top    = point[1] - 5 + window[1]
    right  = point[0] + 5 + window[0]
    bottom = point[1] + 5 + window[1]
    rect = (left,top,right, bottom )
    screen_image.crop(rect).save(path)



def write_screen_given_point():
    global scene_global_id_counter
    
    zhanyi_scene_checkpoint = [(77,158),(350,160),(550,160),(600,160),(650,160),(700,160)]

    sceneRecorder.add_screen(scene_name_gen(scene_name_gl,scene_global_id_counter))

    for ref_img_nr in range(0,len(zhanyi_scene_checkpoint)) :
        ref_img_path = scene_ref_img_name_gen(scene_name_gl,scene_global_id_counter,ref_img_nr)
        sceneRecorder.add_ref_img_in_screen(zhanyi_scene_checkpoint[ref_img_nr],ref_img_path)
        save_point_img(zhanyi_scene_checkpoint[ref_img_nr],ref_img_path)
    
    scene_global_id_counter += 1
    
def write_screen_mouse_point(point_position):
    global scene_global_id_counter
     
    sceneRecorder.add_screen(scene_name_gen(scene_name_gl,scene_global_id_counter))

    ref_img_path = scene_ref_img_name_gen(scene_name_gl,scene_global_id_counter)
    sceneRecorder.add_ref_img_in_screen(point_position,ref_img_path)
    save_point_img(point_position,ref_img_path)
    
    scene_global_id_counter += 1
    

def write_screen_multy_mouse_point(point_list):
    global scene_global_id_counter
    global screen_image
         
    sceneRecorder.add_screen(scene_name_gen(scene_name_gl,scene_global_id_counter))

    screen_image = ImageGrab.grab()
    for ref_img_nr in range(0,len(point_list)) :
        ref_img_path = scene_ref_img_name_gen(scene_name_gl,scene_global_id_counter,ref_img_nr)
        sceneRecorder.add_ref_img_in_screen(point_list[ref_img_nr],ref_img_path)
        save_point_img_no_screengrap(point_list[ref_img_nr],ref_img_path)
    
    scene_global_id_counter += 1

def OnMouseEvent(event):
    global mouse_global_pos
    global mouse_local_pos
    if event.Message == 512 :
        mouse_global_pos = event.Position
        mouse_local_pos = (event.Position[0]-window[0],event.Position[1]-window[1])
    return True

scene_point_set = []
def OnKeyboardEvent(event):
    global scene_point_set
    if event.Message == 256:
        if event.Key == "Q":
            print "press q"
            
            
            #main = action_recorder()
            #main.add_act(action_str("",(1000,2000),"image1.png"))
            #main.add_action((300,400),"image2.png")
            #main.save_action("output.xml")
            
        if event.Key == "W":
            if check_mouse_is_moved() and 0:
                print "press w write 1 scene"
                write_screen_given_point()
                #write_screen_mouse_point(mouse_local_pos)
            
            
            
        
        if event.Key == "E":
            print "press e"
        
        if scene_record_active:
            if event.Key == "Z":
                if check_mouse_is_moved():
                    print "press Z save one image in scene", mouse_local_pos
                    #test_post = (1212,734)
                    #scene_point_set.append(test_post)
                    scene_point_set.append(mouse_local_pos)
            
            if event.Key == "X":
                print "press X save one scene", scene_global_id_counter
                #zhanyi_scene_checkpoint = [(77,158),(350,160),(550,160),(600,160),(650,160),(700,160)]
                
                #write_screen_multy_mouse_point(zhanyi_scene_checkpoint)
                write_screen_multy_mouse_point(scene_point_set)
                print "saved"
                scene_point_set = []
            '''
            if event.Key == "V":
                print "press V save one scene", scene_global_id_counter
                zhanyi_scene_checkpoint = [(77,158),(350,160),(550,160),(600,160),(650,160),(700,160)]
                write_screen_multy_mouse_point(zhanyi_scene_checkpoint)
                print "saved"
                scene_point_set = []
            '''
            if event.Key == "C":
                print "press C save all scene"
                sceneRecorder.save_screen(scene_save_xml_path)
                #time.sleep(1)
                
    return True


# create a hook manager
hm = pyHook.HookManager()
hm.MouseAll = OnMouseEvent
hm.HookMouse()
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()