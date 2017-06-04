#import pythoncom, pyHook
from help_xml import *
from image_process import *
from mouse import *
from keypress import *
from system_manager import *
from qq_msg import *
from get_time_info import *
from action_info import *

import os
import time
import win32api, win32con
from PIL import Image
import random


class act_manager():
    def __init__(self):
        self.win = gameWindow()
        self.win.game_screen()
        self.screenloader = screen_loader("img//element//yuanzheng.xml")
        self.screenloader.read_action_in_new_xml("img//element//allscene.xml")
        self.screenloader.read_action_in_new_xml("img//element//zhanyi.xml")
        self.screenloader.read_action_in_new_xml("img//element//loginout.xml")
        self.screenloader.read_action_in_new_xml("img//element//zhandou.xml")
        self.screenloader.read_action_in_new_xml("img//element//hero.xml")
        self.screenloader.read_action_in_new_xml("img//element//cangbao.xml")
        self.screenloader.read_action_in_new_xml("img//element//gonghui.xml")
        self.screenloader.read_action_in_new_xml("img//element//qiandao.xml")
        self.screenloader.read_action_in_new_xml("img//element//baoxiang.xml")
        self.screenloader.read_action_in_new_xml("img//element//mengjing.xml")
        #self.screenloader.read_action_in_new_xml("img//element//temp.xml")
        
        self.current_id  = start_user_id
        self.local_event_error_flag = False
        self.global_fatal_error_flag = False
        self.action_point = True
        self.get_tili_flag = "NoGetTili"
        self.previous_mouse_pos = get_cords()
        self.current_mouse_pos = get_cords()
        self.action_timeout_timer = start_warting_time + 3600
        self.sleep_time(start_warting_time)
        self.action_timeout_counter = 0
        self.acount_cycle_counter = 0
        self.get_tili_start_id = -1
        self.error_tolerance = 100
        self.qq = myQQ()
        self.last_tuandui_fuben = None
        if activate_qq_message == True:
            pass

    def not_timeout(self):
        if self.action_timeout_timer < 0 :
            self.detected_fatal_error()
            return False
        return True
    def is_timeout(self):
        if self.action_timeout_timer < 0 :
            self.detected_fatal_error()
            return True
        return False
    def sleep_time(self, sleep_time):
        if self.is_timeout():
            return
        if mouse_move_block_action == True:
            self.previous_mouse_pos = get_cords()
            time.sleep(sleep_time)
            self.current_mouse_pos = get_cords()
            while self.previous_mouse_pos != self.current_mouse_pos:
                self.previous_mouse_pos = self.current_mouse_pos
                time.sleep(1)
                self.current_mouse_pos = get_cords()
        else:
            time.sleep(sleep_time)
        self.action_timeout_timer -= sleep_time
        if self.is_timeout():
            error_screen_grab_and_save()
    def set_action_duration(self, time):
        if self.not_timeout():
            self.action_timeout_timer = time
    def is_event_error(self):
        return self.local_event_error_flag
    def is_fatal_error(self):
        return self.global_fatal_error_flag
    def detected_event_error(self):
        self.local_event_error_flag = True
    def detected_fatal_error(self):
        self.global_fatal_error_flag = True
    def clean_event_error(self):
        self.local_event_error_flag = False
    def clean_fatal_error(self):
        self.global_fatal_error_flag = False
            
    def error_connect_again(self):
        if self.is_timeout():
            return
        
        error_img = Image.open("img//element//error//connection_error_1.png").convert("L")
        error_retry_pos = (708,447)
        if self.win.find_obj_in_point_new_screen(error_img, error_retry_pos,(5,5)) is not None:
                mouseLeftClickPoint(error_retry_pos)
                self.sleep_time(2)
              
        error_img = Image.open("img//element//error//teamviewer_0_0.png").convert("L")
        error_retry_pos = (628,456)
        if self.win.find_obj_in_point_new_screen(error_img, error_retry_pos,(5,5)) is not None:
                mouseLeftClickPoint((1037,535))
                self.sleep_time(2)
        
        
        '''        
        error_img = Image.open("img//element//error//connection_error_1_1.png").convert("L")
        error_retry_pos = (727,453)
        if self.win.find_obj_in_point_new_screen(error_img, error_retry_pos,(5,5)) is not None:
                mouseLeftClickPoint(error_retry_pos)
                self.sleep_time(2)
        '''
                
    def scene_dectector(self):
        if self.is_timeout():
            return screen_str()
        #self.screenloader = screen_loader("img//element//mainscreen.xml")
        self.win.get_new_screen()   
        for screen in self.screenloader.screen_list:
            match_img_nr = 0
            for image in screen.image_list:
                point_img_path = image.path
                point_img = Image.open(point_img_path).convert("L")
                #print point_img_path
                point_pos = image.pos
                if self.win.find_obj_in_point_old_screen(point_img, point_pos,(5,5)) is None:
                    #print "not scene 1"
                    break
                match_img_nr += 1
            
            
            if match_img_nr == len(screen.image_list) and match_img_nr !=0:
                print_action = str(self.action_timeout_timer)
                for action in screen.action_list:
                    print_action = print_action+","+action.name
                print screen.name + ": " + print_action
                return screen
            
        return None
         

    def scene_wait_to_dectect_scene(self):
        if self.is_timeout():
            return screen_str()
        retval = self.scene_dectector()
        while retval == None and self.not_timeout():
            self.sleep_time(1)
            retval = self.scene_dectector()
            #self.error_connect_again()
        return retval
    
    def scene_wait_defined_scenes(self, input):
        if self.is_timeout():
            return None
        retval = None
        
        while retval == None and self.not_timeout():
            self.sleep_time(1)
            cur_scene = self.scene_wait_to_dectect_scene()
            self.error_connect_again()
            for index in range(len(input)):
                if input[index] == cur_scene.name:
                    retval = index
        return retval
    
    def scene_wait_scenes_with_string(self, input, time_step = 1000):
        if self.is_timeout():
            return None
        retval = None
        
        while retval == None and self.not_timeout():
            self.sleep_time(1)
            time_step -= 1
            print time_step
            cur_scene = self.scene_wait_to_dectect_scene()
            self.error_connect_again()
            for index in range(len(input)):
                if input[index] in cur_scene.name:
                    retval = index
            if time_step <= 0:
                return -1
        return retval
    
    def scene_auto_action_manager(self): 
        self.auto_check_init_scene()
        
        if 0:
            #self.manage_jingying_fuben(12)
            self.yuanzheng_event_do_all()
            
                        
        self.manage_day_event()
        
    def auto_check_init_scene(self):      
        current_scene = self.scene_wait_to_dectect_scene()
        if "mainscreen" in current_scene.name:  
            pass
        elif current_scene.name == "bluestacks_main_win":
            self.dota_login(self.current_id)
    
    def manage_day_event(self):
        while 1:
            self.qq_message_sender()
            
            try:
                self.action_one_cycle()
                
                
                #self.manage_tuandui_fuben()
                #self.huodong_reward_check()
                #self.saodang_jingying_fuben(15)
            except:
                pass

            self.switch_account_function()
            
    def qq_message_sender(self):
        if activate_qq_message == True:
            try:
                self.qq.login()
                time.sleep(2)
                self.qq.send_msg("Id: "+ str(self.current_id) + "start")
                time.sleep(2)
                self.qq.logout()
            except:
                pass
        
    def action_one_cycle(self):
        self.action_point = True
        
        if  china_time().hour in [1,2,3,4] and self.current_id not in [0,1,2,3,4,5,6,7,8,9,10,11,12,13]:
            self.shuipian_hecheng(500) 
        
        if dotaTime_is_gotTili() is False or self.get_tili_flag != "GetTili" or get_tili_is_active == False:
            for event in user_account_action_list[self.current_id]:
                if event == "jingjichang":
                    self.tiaozhan_jingjichang()
                elif event == "shiguang":
                    self.fuben_event_shiguang()
                elif event == "shilian":
                    self.fuben_event_shilian()
                elif event == "mengjing":
                    self.fuben_event_mengjing()
                elif event == "yuanzheng":
                    self.yuanzheng_event_do_all()
                elif event == "putong":
                    self.manage_putong_fuben(12)
                elif event == "jingying":
                    if  china_time().hour in [0,1,2,3,4]:
                        
                        #self.baoxiang_check()
                        #self.yuanzheng_event_do_all()
                        #self.saodang_jingying_fuben(20)
                        #self.cangbao_kaicai_and_search_once()
                        #self.putongshangren_buy()  
                        
                        #self.cangbao_kaicai_and_search_once()
                        #self.saodang_jingying_fuben(20)
                        #self.wangzuozhita()
                        #self.shuipian_hecheng(500)
                        self.manage_tuandui_fuben(fuben_tuandui_2)
                        #self.yuanzheng_event_do_all()
                        #self.saodang_jingying_fuben(10)  
                        #self.manage_jingying_fuben(12)
                    #else:
                        #self.saodang_jingying_fuben(10) 
                        pass
                    #if self.current_id in [9, 10, 11, 12, 13]:
                        #self.manage_jingying_fuben(12)
                    self.saodang_jingying_fuben(20)
                elif event == "saodang":
                    self.saodang_jingying_fuben(12)   
                elif event == "tuandui":
                    self.manage_tuandui_fuben()
                elif event == "dianjing":
                    self.dianjin_check()
                elif event == "shangren":
                    self.putongshangren_buy()
                elif event == "baoxiang":
                    self.baoxiang_check()
                elif event == "cangbao":
                    self.cangbao_kaicai_and_search_once()
                elif event == "gonghui":
                    self.gonghui_event()
                elif event == "xingxiang":
                    self.xingxiang_check()
                elif event == "hecheng":
                    self.shuipian_hecheng(500)
                elif event == "huodong":
                    self.huodong_reward_check()
                elif event == "dailyonce":
                    if self.get_tili_flag == "NoGetTili" or block_daily_once_event == False:
                        self.daily_once_event()
                        #self.daily_once_event()
             
        elif dotaTime_is_gotTili() is True:
            #self.saodang_jingying_fuben(30)
            self.baoxiang_check()
            self.huodong_reward_check()     
             
            if  china_time().hour in [9,10]:
                
                current_scene = self.scene_wait_to_dectect_scene()
                if "mainscreen_0_init" not in current_scene.name:
                    self.manage_tuandui_fuben(fuben_tuandui_1)
                self.cangbao_kaicai_and_search_once()
                self.putongshangren_buy()
                pass
            
            if  china_time().hour in [12,13]:   
                self.saodang_jingying_fuben(12)  
                self.putongshangren_buy()  
                pass
            
            if  china_time().hour in [18,19]:   
                self.saodang_jingying_fuben(12)
                self.putongshangren_buy()  
                pass
            
            if  china_time().hour in [21,22,23]:
                self.manage_tuandui_fuben(fuben_tuandui_3)
                #self.saodang_jingying_fuben(20)
                self.cangbao_kaicai_and_search_once()
                self.putongshangren_buy()  
                pass
            #self.saodang_jingying_fuben(5)
            
        if get_tili_is_active == True:
            if self.get_tili_flag == "NoGetTili" and dotaTime_is_gotTili() == True:
                self.get_tili_flag = "GetTili"
                self.get_tili_start_id = self.current_id
                self.action_timeout_timer = 50;
                #self.current_id = (self.current_id+1) % user_account_number
                
            elif self.get_tili_flag == "GetTili" and self.current_id == self.get_tili_start_id:
                self.get_tili_flag = "GotTili"
                
            elif self.get_tili_flag != "NoGetTili"  and dotaTime_is_gotTili() == False:
                self.get_tili_flag = "NoGetTili" 
            
    def switch_account_function(self):
        if self.is_timeout():
            
            #if self.current_id >= 4 and self.error_tolerance <= 0: 
            if self.error_tolerance <= 0: 
                self.current_id += 1
                self.error_tolerance = 1
                if self.current_id >= user_account_number:
                    self.acount_cycle_counter += 1
                    self.current_id = 0
            else:
                self.error_tolerance -= 1
            self.action_timeout_counter += 1
            relaunch_bluestacks(event_max_time['restart'])
            self.action_timeout_timer = 3600
            self.sleep_time(20)
            self.dota_login(self.current_id)
        else:            
            #self.yuanzheng_event_do_all()
            self.current_id += 1
            if self.current_id < 4:
                self.error_tolerance = 3
            else:
                self.error_tolerance = 1                
            if self.current_id >= user_account_number:
                self.acount_cycle_counter += 1
                self.current_id = 0
            self.action_point = True
            self.change_account(self.current_id)
            
        print "==================================="
        print "restart times:",self.action_timeout_counter
        print "success cycle:",self.acount_cycle_counter
        print "==================================="
        
    def daily_once_event(self):
        if self.is_timeout():
            return
        
        current_scene = self.scene_wait_to_dectect_scene()
        
        if "mainscreen_0_init" in current_scene.name:
            
            self.dianjin_check()
            #self.putongshangren_buy()
            
            self.baoxiang_check()
            self.tiaozhan_jingjichang()
            
            self.fuben_event_shiguang()
            self.fuben_event_shilian()
            
            #if self.current_id not in [14,15]:
            self.yuanzheng_event_do_all()
            #self.yuanzheng_event_do_all()
            
            
            if  china_time().hour not in [5,6,7]:
                self.manage_tuandui_fuben(fuben_tuandui_1)
                pass
                
            self.baoxiang_check()
            self.tiaozhan_jingjichang()
            
            self.qiandao_reward_check()
            
            #self.xingxiang_check()
            
            self.hero_update_skill()
            self.wangzuozhita()
            
            if  china_time().hour not in [0,1,2,3,4, 22,23,24]:
                self.fuben_event_mengjing()
            #self.cangbao_kaicai_and_search_once()
            
            if self.current_id == 0:# or self.current_id==2:
                return
            
            #self.gonghui_event()
            
                
    def daily_once_event_2(self):
        if self.is_timeout():
            return
        
        current_scene = self.scene_wait_to_dectect_scene()
        
        if "mainscreen_0_init" in current_scene.name:
            self.dianjin_check()
            #self.putongshangren_buy()
            self.hero_update_skill()
            self.baoxiang_check()
            self.fuben_event_shiguang()
            self.yuanzheng_event_do_all(False)
            #self.baoxiang_check()
            #self.xingxiang_check()
            #self.qiandao_reward_check()
            #self.cangbao_kaicai_and_search_once()
            #if self.current_id == 0 or self.current_id==2:
                #return
            #self.gonghui_event()
                
            
    def dota_login(self,target_account):
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['login'])
        
        self.scene_action_excecute("bluestacks_main_win","login")
        
        self.sleep_time(5)
        mouseLeftClickPoint((808, 492))
        self.sleep_time(2)
            
        if 0 == self.scene_wait_defined_scenes(['login_longtu_firstview_0','change_account_wait_login_info']):
            print "found previous account!"
            self.scene_action_excecute("login_longtu_firstview_0","userlist")
            self.scene_action_excecute("login_userlist","delete")
            self.scene_action_excecute("delete_account","yes")
        else:
            print "not found previous account!"
        
        self.sleep_time(0.5)
        type_user_login_info(user_account_info[target_account][0],user_account_info[target_account][1])
        
        #self.scene_action_excecute("change_account_wait_login_info","login")
        
        current_scene = self.scene_wait_to_dectect_scene()
        while "mainscreen" not in current_scene.name and self.not_timeout():
            self.scene_action_excecute(current_scene.name,"login")
            current_scene = self.scene_wait_to_dectect_scene()
    
    def dota_logout(self):
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['logout'])
        
        self.mainscreen_action_excecute("logout")
        current_scene = self.scene_wait_to_dectect_scene()
        if "logout_main_win" in current_scene.name:
            self.scene_action_excecute(current_scene.name,"logout")
        
    def change_account(self, target_account):
        if self.is_timeout():
            return
        self.dota_logout()
        self.sleep_time(5)
        self.dota_login(target_account)
        
    def yuanzheng_event_do_all(self, doAll = True):
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['yuanzheng'])
        
        current_scene = self.scene_wait_to_dectect_scene()
        if "mainscreen_0" not in current_scene.name:
            return
        
        while self.not_timeout():
            self.mainscreen_action_excecute("yuanzheng")
            self.scene_wait_scenes_with_string(['yuanzheng'])
            
            current_scene = self.scene_wait_to_dectect_scene()
            if "yuanzheng_screen_position_baoxiang" in current_scene.name:
                current_screen_actionlist = current_scene.action_list
                curent_screen_name = current_scene.name
                for action in current_screen_actionlist:
                    current_scene = self.scene_wait_to_dectect_scene()
                    if current_scene.name != curent_screen_name:
                        continue
                    
                    self.set_action_duration(event_max_time['yuanzheng'])
                    
                    if "zhan" in action.name or "bao" in action.name:
                        self.scene_action_excecute(curent_screen_name,action.name)
                    
                    if "zhan" in action.name:
                        for counter_i in range(3):
                            zhan_hit_ret_val = self.scene_wait_scenes_with_string(['yuanzheng_screen_zhandou_done','yuanzheng_zhandou_preview','yuanzheng_baoxiang'], 20)
                            if zhan_hit_ret_val == 0 or zhan_hit_ret_val == 1:
                                current_scene = self.scene_wait_to_dectect_scene()
                                if "yuanzheng_screen_zhandou_done" in current_scene.name:
                                    self.scene_action_excecute(current_scene.name,"return")
                                elif "yuanzheng_zhandou_preview" in current_scene.name:
                                    self.scene_action_excecute(current_scene.name,"zhandou")
                                    self.yuanzheng_zhandou_fuben()
                                    if doAll == False and self.not_timeout():
                                        current_scene = self.scene_wait_to_dectect_scene()
                                        self.scene_action_excecute(current_scene.name,"return")
                                        return
                                break
                            elif zhan_hit_ret_val == 2:
                                self.current_scene_action_excecute("return1")
                                self.current_scene_action_excecute("return2")
                                self.current_scene_action_excecute("return3")
                                self.current_scene_action_excecute("queding")
                                click_list = [(700,470),(700,530),(700,600)]
                                self.unknown_screen_mouse_click(click_list)
                                
                                self.scene_action_excecute(curent_screen_name,action.name)
                            
                    elif "bao" in action.name:
                        self.sleep_time(1)
                        self.current_scene_action_excecute("return1")
                        self.current_scene_action_excecute("return2")
                        self.current_scene_action_excecute("return3")
                        self.current_scene_action_excecute("queding")
                        click_list = [(700,470),(700,530),(700,600)]
                        self.unknown_screen_mouse_click(click_list)
                    '''
                    if "zhan" in action.name:
                        #self.scene_action_excecute(curent_screen_name,action.name)
                        
                        current_scene = self.scene_wait_to_dectect_scene()
                        if "yuanzheng_screen_zhandou_done" in current_scene.name:
                            self.scene_action_excecute(current_scene.name,"return")
                        elif "yuanzheng_zhandou_preview" in current_scene.name:
                            self.scene_action_excecute(current_scene.name,"zhandou")
                            self.yuanzheng_zhandou_fuben()
                            if doAll == False and self.not_timeout():
                                current_scene = self.scene_wait_to_dectect_scene()
                                self.scene_action_excecute(current_scene.name,"return")
                                return
                    elif "bao" in action.name:
                        #self.scene_action_excecute(curent_screen_name,action.name)
                        self.sleep_time(1)
                        #self.check_got_yingxiong()
                        self.current_scene_action_excecute("return1")
                        self.current_scene_action_excecute("return2")
                        self.current_scene_action_excecute("return3")
                        click_list = [(700,470),(700,530),(700,600)]
                        self.unknown_screen_mouse_click(click_list)
                        current_scene = self.scene_wait_to_dectect_scene()
                        if current_scene.name == "baoxiang_yingxiong_0":
                            self.scene_action_excecute("baoxiang_yingxiong_0","queding")
                            self.scene_action_excecute("yuanzheng_baoxiang","queding")
                        if "yuanzheng_baoxiang" in current_scene.name:
                            self.scene_action_excecute(current_scene.name,"queding")
                            #if "bao15" in action.name:
                                #current_scene = self.scene_wait_to_dectect_scene()
                                #self.scene_action_excecute(current_scene.name,"return")
                                #return
                    '''            
                    
                
            current_scene = self.scene_wait_to_dectect_scene()
            if "yuanzheng_screen_position_baoxiang15_end_has_refresh" in current_scene.name:
                self.scene_action_excecute(current_scene.name,"refresh")
                self.sleep_time(1)
                current_scene = self.scene_wait_to_dectect_scene()
                if "yuanzheng_refresh" not in current_scene.name:
                    self.scene_action_excecute(current_scene.name,"return")
                    return
                self.scene_action_excecute(current_scene.name,"refresh")
                if self.current_id != 0:
                    self.scene_action_excecute("yuanzheng_screen_position_baoxiang1_0","xianqian")
                    self.scene_action_excecute("zhandou_chuchang_no_hero","hero_6")
                    self.scene_action_excecute("zhandou_chuchang_yingxiong_buman","hero_7")
                    self.scene_action_excecute("zhandou_chuchang_yingxiong_buman","hero_8")
                    self.scene_action_excecute("zhandou_chuchang_yingxiong_buman","hero_9")
                    self.scene_action_excecute("zhandou_chuchang_yingxiong_buman","hero_10")
                    self.scene_action_excecute("zhandou_chuchang_yingxiong", "jingru_fuben")
                    self.sleep_time(2)
                    click_list = [(700,650)]
                    self.unknown_screen_mouse_click(click_list)
                
            
            current_scene = self.scene_wait_to_dectect_scene()
            self.return_to_main_screena()
            #self.scene_action_excecute(current_scene.name,"return")
            try:
                if "zhan16" in action.name and current_scene.name == "yuanzheng_screen_position_baoxiang11_0":
                    return
            except:
                pass
            
        
        if self.is_timeout():
            
            self.action_timeout_timer = 30
            
            current_scene = self.scene_wait_to_dectect_scene()
            
            if current_scene != None:              
                
                if "yuanzheng_chuchang_main_win_no_hero" == current_scene.name:    
                    
                    self.action_timeout_timer = 50
                    
                    self.scene_action_excecute("yuanzheng_chuchang_main_win_no_hero","return")
                    
                    self.current_scene_action_excecute("refresh")
                    
                    self.current_scene_action_excecute("refresh")
                    
                    self.current_scene_action_excecute("return")
                else:
                    self.action_timeout_timer = -1
            
            
    def yuanzheng_zhandou_fuben(self):
        if self.is_timeout():
            return
        current_scene = self.scene_wait_to_dectect_scene()
        
        #while "zhandou_chuchang_yingxiong" in current_scene.name and self.not_timeout():
            #self.scene_action_excecute(current_scene.name,"repick_hero")
            #current_scene = self.scene_wait_to_dectect_scene()
            
        if "yuanzheng_chuchang_main_win_no_hero" in current_scene.name or "zhandou_chuchang_no_hero" in current_scene.name:
            if self.current_id == 0:
                self.scene_action_excecute(current_scene.name,"hero_1")
            else:
                self.scene_action_excecute(current_scene.name,"rent")
                self.scene_action_excecute(current_scene.name,"hero_1")

        current_scene = self.scene_wait_to_dectect_scene()
        if "yuanzheng_chuchang_1_rented_hero" in current_scene.name or "yuanzheng_chuchang_main_win_1st_hero_0" in current_scene.name or "zhandou_chuchang_yingxiong_buman" in current_scene.name:
            self.scene_action_excecute(current_scene.name,"jingru_fuben")
            current_scene = self.scene_wait_to_dectect_scene()
        
        self.scene_action_excecute(current_scene.name,"haode")
        current_scene = self.scene_wait_to_dectect_scene()
        
        if "yuanzheng_chuchang_rent_hero" in current_scene.name:
            self.scene_action_excecute(current_scene.name,"rent")
            current_scene = self.scene_wait_to_dectect_scene()
        
        while "zhandou_ing" not in current_scene.name and self.not_timeout():
            self.sleep_time(1.0)
            current_scene = self.scene_wait_to_dectect_scene()
            self.error_connect_again()
        
        self.current_scene_action_excecute("auto")
        #self.scene_action_excecute("yuanzheng_screen_zhandou_ing_0","auto")
        self.zhandou_jeshu_fuben()
        
    def arrange_duiwu(self, num = 5):
        if self.is_timeout():
            return
        #return # debug
        current_scene = self.scene_wait_to_dectect_scene()
        if current_scene.name == "zhandou_chuchang_yingxiong_buman" or current_scene.name == "zhandou_chuchang_no_hero":       
            while current_scene.name != "zhandou_chuchang_no_hero" and self.not_timeout():
                self.scene_action_excecute(current_scene.name,"repick_hero")
                current_scene = self.scene_wait_to_dectect_scene()
                
            for i in range(num):
                self.scene_action_excecute(current_scene.name,"hero_"+str(1+i))
                current_scene = self.scene_wait_to_dectect_scene()

    def dianjin_check(self):
        if self.is_timeout():
            return False
        self.set_action_duration(event_max_time['dianjing'])
        
        self.mainscreen_action_excecute("dianjin")
        
        self.sleep_time(1)
        current_scene = self.scene_wait_to_dectect_scene()
        if current_scene.name == "dianjing_main_win":
            self.scene_action_excecute(current_scene.name,"dianjin")
            current_scene = self.scene_wait_to_dectect_scene()
            if current_scene.name == "dianjing_finish":
                self.scene_action_excecute(current_scene.name,"return")
                return True
            
        self.scene_action_excecute(current_scene.name,"return")
        return False
        
    def qiandao_reward_check(self):
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['qiandao'])
        self.mainscreen_action_excecute("qiandao")
        result = self.scene_find_qiandao_target()
        if result == None:
            mouseDragDown()
            result = self.scene_find_qiandao_target()
        
        if result != None:
            mouseLeftClickPoint(result)
            self.sleep_time(2)
            get_reward_done = False
            while get_reward_done == False  and self.not_timeout():
                current_scene = self.scene_dectector()
                try:
                    if "qiandao_main_win" in current_scene.name:
                        get_reward_done = True
                        continue                       
                except:
                    pass
                self.sleep_time(0.5)
                mouseLeftClickPoint((615,600))
                self.sleep_time(0.05)
                mouseLeftClickPoint((615,650))
                self.sleep_time(0.05)
                mouseLeftClickPoint((615,700))
                self.sleep_time(0.05)
                mouseLeftClickPoint((700,790))
                self.sleep_time(0.5)
        
        current_scene = self.scene_wait_to_dectect_scene()
        self.scene_action_excecute(current_scene.name,"return")   
    
    def scene_find_qiandao_target(self):
        if self.is_timeout():
            return None

        self.win.get_new_screen()                   
        point_img = Image.open("img//element//qiandao//diandao_target_color.png").convert("L")
        return self.win.find_obj_in_area_in_new_screen(point_img)
    
    def scene_find_current_fuben(self):
        if self.is_timeout():
            return None

        self.win.get_new_screen()                   
        point_img = Image.open("img//element//tuandui//temp_0_1.png").convert("L")
        return self.win.find_obj_in_area_in_new_screen(point_img)

         
    def huodong_reward_check(self):
        if self.is_timeout():
            return
        current_scene = self.scene_wait_to_dectect_scene()
        if "mainscreen_0" not in current_scene.name:
            return
        self.set_action_duration(event_max_time['huodong'])
        
        self.mainscreen_action_excecute("huodong")
        
        self.sleep_time(1)
        current_scene = self.scene_wait_to_dectect_scene()
        while (current_scene.name == "huodong_finish" or current_scene.name == "huodong_reward_1" or current_scene.name == "huodong_reward_2" or current_scene.name == "huodong_reward_3" or current_scene.name == "levelup")  and self.not_timeout():
            if current_scene.name == "huodong_finish" or current_scene.name == "huodong_reward_1" or current_scene.name == "huodong_reward_2" or current_scene.name == "huodong_reward_3":
                self.scene_action_excecute(current_scene.name,"get_reward")
            elif current_scene.name == "levelup" :
                self.scene_action_excecute(current_scene.name,"return")   
            current_scene = self.scene_dectector()
            while current_scene == None  and self.not_timeout():
                self.check_levelup()
                current_scene = self.scene_dectector()
            self.sleep_time(1)
            #click_list = [(800, 539),(1099, 223),(1099, 273),(1099, 323)]
            #self.unknown_screen_mouse_click(click_list)
            #self.sleep_time(1)
        
        self.scene_action_excecute("huodong_main_win","return")
        
    def check_levelup(self):
        if self.is_timeout():
            return

        self.sleep_time(1.5)
        mouseLeftClickPoint((800,539))
        mouseLeftClickPoint((1099,223))
        mouseLeftClickPoint((1099,273))
        mouseLeftClickPoint((1099,323))
        self.sleep_time(1)
        
    def hero_update_skill(self, num = 3):
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['shill_update'])
        self.mainscreen_action_excecute("hero")
        self.scene_action_excecute("hero_main_win_0","hero_6")
        self.scene_action_excecute("hero_tujian_win_0","jineng")
        for i in range(num):
            current_scene = self.scene_wait_to_dectect_scene()
            while "can_update_skill" not in current_scene.name and self.not_timeout():
                self.scene_action_excecute(current_scene.name,"next")
                current_scene = self.scene_wait_to_dectect_scene()
                
            self.scene_action_excecute(current_scene.name,"levelup")
            #self.sleep_time(1)
            
        current_scene = self.scene_wait_to_dectect_scene()
        self.scene_action_excecute(current_scene.name,"return")
        self.scene_action_excecute("hero_main_win_0","return")
                
    def shuipian_hecheng(self, num = 100):
        if self.is_timeout():
            return
        self.set_action_duration(num * 2)
        self.mainscreen_action_excecute("shuipian")
        for i in range(num):
            print "remain: ", i
            mouseLeftClickPoint((700, 250))
            self.sleep_time(0.3)
            mouseLeftClickPoint((435, 745))
            self.sleep_time(0.3)
            mouseLeftClickPoint((576, 689))
            self.sleep_time(0.3)
            mouseLeftClickPoint((952, 143))
            self.sleep_time(0.3)
            self.error_connect_again()
                
        
        self.sleep_time(3)
        mouseLeftClickPoint((125, 77))
                
    def xingxiang_check(self):
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['xingxiang'])
        
        self.mainscreen_action_excecute("xingxiang")
        
        self.sleep_time(1)
        current_scene = self.scene_wait_to_dectect_scene()
        while current_scene.name == "xingxiang_new_mail"  and self.not_timeout():
            self.scene_action_excecute("xingxiang_new_mail","read")
            self.scene_action_excecute("xingxiang_detail","read")
            current_scene = self.scene_wait_to_dectect_scene()
        
        self.scene_action_excecute("xingxiang_main_win","return")
                
    def baoxiang_check(self):
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['baoxiang'])
        
        current_scene = self.scene_wait_to_dectect_scene()
        if "mainscreen_0" not in current_scene.name:
            return
        
        self.mainscreen_action_excecute("baoxiang")
        jingbi_action_flag = False
        zhuanshi_action_flag = False
                    
        current_scene = self.scene_wait_to_dectect_scene()
        if "baoxiang_jingbi_mianfei" in current_scene.name:
            self.scene_action_excecute("baoxiang_jingbi_mianfei","jingbi_down_bt")
            jingbi_action_flag = True
            
        current_scene = self.scene_wait_to_dectect_scene()
        if  "baoxiang_main_win" in current_scene.name:
            self.scene_action_excecute("baoxiang_main_win","zhuanshi_down_bt")
            zhuanshi_action_flag = True
            
        if jingbi_action_flag == True:
            current_scene = self.scene_wait_to_dectect_scene()
            self.scene_action_excecute(current_scene.name,"jingbi_up_bt")
            self.check_got_yingxiong()
            current_scene = self.scene_wait_to_dectect_scene()  
            if current_scene.name == "baoxiang_yingxiong_0":
                self.scene_action_excecute("baoxiang_yingxiong_0","queding")
            self.scene_action_excecute("baoxiang_queding_0","queding")
        
        current_scene = self.scene_wait_to_dectect_scene()
        if zhuanshi_action_flag == True and "baoxiang_zhuanshi_mianfei" in current_scene.name:
            current_scene = self.scene_wait_to_dectect_scene()
            self.scene_action_excecute(current_scene.name,"zhuanshi_up_bt")
            self.check_got_yingxiong()
            current_scene = self.scene_wait_to_dectect_scene()  
            if current_scene.name == "baoxiang_yingxiong_0":
                self.scene_action_excecute("baoxiang_yingxiong_0","queding")
            self.scene_action_excecute("baoxiang_queding_0","queding")
        
        current_scene = self.scene_wait_to_dectect_scene()
        self.scene_action_excecute(current_scene.name,"return")
           
    def check_got_yingxiong(self):
        if self.is_timeout():
            return
        
        current_scene = self.scene_dectector()
        while current_scene == None  and self.not_timeout():
            if self.is_timeout():
                return False
            mouseLeftClickPoint((1099,223))
            current_scene = self.scene_dectector()
            self.sleep_time(1)
            
    def unknown_screen_mouse_click(self,click_list = [(1099,223)]):
        if self.is_timeout():
            return
        
        current_scene = self.scene_dectector()
        while current_scene == None  and self.not_timeout():
            if self.is_timeout():
                return False
            for click_point in click_list:
                mouseLeftClickPoint(click_point)
                self.sleep_time(1)
                current_scene = self.scene_dectector()
                if (current_scene == None  and self.not_timeout()) == False:
                    return
                
        
    def cangbao_kaicai_and_search_once(self):  
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['cangbao'])
        self.mainscreen_action_excecute("cangbao")
        
        self.scene_wait_defined_scenes(['cangbao_main_win_1','cangbao_has_kaicai_0'])
        self.current_scene_action_excecute('center')
        self.unknown_screen_mouse_click([(1251, 271)])
        self.sleep_time(5)
        self.current_scene_action_excecute('center')
        self.unknown_screen_mouse_click([(1251, 271)])
        
        hero_counter = 1
        current_scene = self.scene_wait_to_dectect_scene()
        while "cangbao_not_kaicai" not in current_scene.name and self.not_timeout():
            while "cangbao_not_kaicai" not in current_scene.name and "cangbao_has_kaicai" not in current_scene.name and self.not_timeout():
                if "cangbao_jinkuang_kaicai_finish" in current_scene.name:
                    self.scene_action_excecute(current_scene.name,"get")
                    self.sleep_time(3)
                else:
                    self.scene_action_excecute(current_scene.name,"next")
                current_scene = self.scene_wait_to_dectect_scene()
            if "cangbao_not_kaicai" in current_scene.name:
                break
            #self.current_scene_action_excecute("kaicai")
            self.scene_action_excecute("cangbao_has_kaicai_0", "kaicai")
            #self.scene_action_excecute("cangbao_select_type_1", "jinkuang")
            self.scene_action_excecute("cangbao_select_type_2", "iron")
            #self.scene_action_excecute("cangbao_jinkuang_type_0", "large")
            self.scene_action_excecute("cangbao_size_type_0", "large")
            current_scene = self.scene_wait_to_dectect_scene()
            
            while "cangbao_kaicai_yingxiong_ready" not in current_scene.name and self.not_timeout():
                
                self.scene_action_excecute(current_scene.name,"hero_"+str(hero_counter))
                hero_counter += 1
                current_scene = self.scene_wait_to_dectect_scene()
                
                if "cangbao_zhaohui_yingxiong" in current_scene.name :
                    self.scene_action_excecute(current_scene.name,"return")
                    current_scene = self.scene_wait_to_dectect_scene()
                
            
            self.scene_action_excecute(current_scene.name,"queding")
            current_scene = self.scene_wait_to_dectect_scene()
            
            
        self.scene_action_excecute(current_scene.name,"search")
        self.sleep_time(5)
        current_scene = self.scene_wait_to_dectect_scene()
        self.scene_action_excecute(current_scene.name,"return")
        return
        
        if "cangbao_main_win" in current_scene.name:
            
            self.scene_action_excecute(current_scene.name,"next")
            self.scene_action_excecute(current_scene.name,"next")
            self.scene_action_excecute(current_scene.name,"next")
            self.scene_action_excecute(current_scene.name,"search")
            self.sleep_time(5)
            current_scene = self.scene_wait_to_dectect_scene()
            
        self.scene_action_excecute(current_scene.name,"return")
        
    def gonghui_event(self):
        if self.is_timeout():
            return

        self.set_action_duration(event_max_time['gonghui'])
        self.mainscreen_action_excecute("gonghui")
        
        #self.scene_action_excecute("gonghui_main_win_0","mobai_1")
        #current_scene = self.scene_wait_to_dectect_scene()
        #if "mobai_or_liaotian" in current_scene.name:
            #self.scene_action_excecute("mobai_or_liaotian","return")
            #current_scene = self.scene_wait_to_dectect_scene()
        #if "gonghui_main_win" in current_scene.name:
            #self.scene_action_excecute("gonghui_main_win_0","mobai_2")
            #current_scene = self.scene_wait_to_dectect_scene()
        #if "mobai_win" in current_scene.name:
            #self.scene_action_excecute("mobai_win_0","gold")
            #self.scene_action_excecute("mobai_reward_0","confirm")

        if True:
            self.scene_action_excecute("gonghui_main_win_0","yongbing")
            if 0 == self.scene_wait_defined_scenes(['yongbing_full_1','yongbing_no_2_hero']):
                self.scene_action_excecute("yongbing_full_1","hero_2_back")
                self.sleep_time(1)
                current_scene = self.scene_wait_to_dectect_scene()
                if "yongbing_refund" in current_scene.name:
                    self.scene_action_excecute("yongbing_refund","close")
                else:
                    self.return_to_main_screena()
                    return
            
            self.scene_action_excecute("yongbing_no_2_hero","hero_2_send")
            for i in range(11):
                self.scene_action_excecute("yongbing_send_hero_win","hero_"+str(15-i))
                current_scene = self.scene_wait_to_dectect_scene()
                if "yongbing_confirm" in current_scene.name:
                    break
                elif "cangbao_zhaohui_yingxiong" in current_scene.name:
                    self.scene_action_excecute(current_scene.name,"return")
                    current_scene = self.scene_wait_to_dectect_scene()
            self.scene_action_excecute("yongbing_confirm","confirm")
        self.return_to_main_screena()

    def get_current_zhanyi_info(self):
        if self.is_timeout():
            return
        
        is_in_zhanyi = False
        while is_in_zhanyi == False and self.not_timeout():
            current_scene = self.scene_wait_to_dectect_scene()
            curr_scene_event = current_scene.name.split("_")[0]
            if curr_scene_event == "zhanyi":
                is_in_zhanyi = True
            else:
                print "ERROR not in zhanyi event"
                self.current_scene_action_excecute("return")
                self.sleep_time(1)
        
        if current_scene.name.split("_")[1]=="jingying" :
            curr_typ = "jy"
        elif current_scene.name.split("_")[1]=="putong" :
            curr_typ = "pt"
        elif current_scene.name.split("_")[1]=="tuandui" :
            curr_typ = "td"
        
        curr_cap = int(current_scene.name.split("_")[2]) + 1
        
        return {'zhanyi_typ': curr_typ, 'zhanyi_cap': curr_cap}
    
    def zhanyi_go_to_captital(self,target_type = "jy", target_capital = 1):
        if self.is_timeout():
            return
        current = self.get_current_zhanyi_info()
        
        while current['zhanyi_typ'] != target_type and self.not_timeout():
            print current
            if target_type == "pt":
                self.current_scene_action_excecute("to_putong")
            elif target_type == "jy":
                self.current_scene_action_excecute("to_jingying")
            elif target_type == "td":
                self.current_scene_action_excecute("to_tuandui")
            current = self.get_current_zhanyi_info()
    
        while current['zhanyi_cap'] != target_capital and self.not_timeout():
            if current['zhanyi_cap'] > target_capital:
                self.current_scene_action_excecute("previous")
            else:
                self.current_scene_action_excecute("next")
            current = self.get_current_zhanyi_info()
    
    def return_to_main_screena(self):
        if self.is_timeout() :
            return
        current_scene = self.scene_wait_to_dectect_scene()
        while "mainscreen" not in current_scene.name and self.not_timeout():
            self.scene_action_excecute(current_scene.name,"return")
            current_scene = self.scene_wait_to_dectect_scene()
            
    def saodang_jingying_fuben(self, max_cnt = 1): 
        if self.is_timeout() or self.action_point == False:
            return
        self.set_action_duration(event_max_time['saodang'])
            
        self.mainscreen_action_excecute("zhanyi")
        done_saodang_time = 0
        
        for fuben in fuben_saodang_jingying:            
            self.set_action_duration(event_max_time['saodang'])
            soll_typ = fuben.split("_")[0]
            soll_cap = int(fuben.split("_")[1])
            soll_num = fuben.split("_")[2]
            self.zhanyi_go_to_captital(soll_typ,soll_cap)
            self.current_scene_action_excecute("fuben_"+soll_num)
            
            fuben_done = False
            while fuben_done==False and self.not_timeout():
                self.current_scene_action_excecute("saodang")
                #self.check_levelup()
                current_scene = self.scene_wait_to_dectect_scene()
                if "zhandou_found_something" in current_scene.name:
                    self.scene_action_excecute("zhandou_found_something", "return")
                    self.scene_action_excecute("zhandou_saodang", "return")
                    done_saodang_time += 1
                elif "zhandou_saodang" in current_scene.name:
                    self.scene_action_excecute("zhandou_saodang", "return")
                    done_saodang_time += 1
                elif "event_maitili" in current_scene.name:
                    self.return_to_main_screena()
                    self.action_point = False
                    return "notili"# mein you ti li
                else:
                    self.current_scene_action_excecute("return")
                    fuben_done=True
                    
                if done_saodang_time >=max_cnt:
                    self.return_to_main_screena()
                    return "finish saodang"
                    
                if self.is_timeout():
                    self.action_timeout_timer = 15
                    self.check_levelup()
                    mouseLeftClickPoint((1082, 277))
                    self.sleep_time(3)
                    mouseLeftClickPoint((1082, 177))
                    self.sleep_time(3)
                    
                    current_scene = self.scene_wait_to_dectect_scene()
                    if current_scene != None:              
                        self.set_action_duration(event_max_time['saodang'])
                        #self.action_timeout_timer = (max_cnt - done_saodang_time) *  event_max_time['saodang']
                
                
        self.current_scene_action_excecute("return")
        return "done all saodang list fuben"
            
      
    def manage_tuandui_fuben(self, obj_fuben = fuben_tuandui): 
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['tuandui'])
            
        self.mainscreen_action_excecute("zhanyi")
        
        if self.last_tuandui_fuben != None and self.last_tuandui_fuben in obj_fuben: 
            soll_typ = self.last_tuandui_fuben.split("_")[0]
            soll_cap = int(self.last_tuandui_fuben.split("_")[1])
            soll_num = self.last_tuandui_fuben.split("_")[2]
            self.zhanyi_go_to_captital(soll_typ,soll_cap)

            for i in range(3):
                self.current_scene_action_excecute("fuben_"+soll_num)
                
                current_scene = self.scene_wait_to_dectect_scene()
                if "zhandou_fuben_info_no_tuandui" in current_scene.name:
                    self.scene_action_excecute("zhandou_fuben_info_no_tuandui","return")  
                    break
                elif "zhandou_jj_sg_sl_fuben_info" in current_scene.name:
                    self.scene_action_excecute("zhandou_jj_sg_sl_fuben_info","jingru_fuben_1")
                    self.sleep_time(3)
                    current_scene = self.scene_wait_to_dectect_scene()
                    if "zhandou_jj_sg_sl_fuben_info" in current_scene.name:
                        self.scene_action_excecute(current_scene.name,"return")     
                        self.current_scene_action_excecute("return")
                        return "finish"  
                    else:
                        self.zhandou_jingying_fuben()
                else:
                    self.sleep_time(1)
        
        for fuben in obj_fuben:     
            self.last_tuandui_fuben = fuben       
            soll_typ = fuben.split("_")[0]
            soll_cap = int(fuben.split("_")[1])
            soll_num = fuben.split("_")[2]
            self.zhanyi_go_to_captital(soll_typ,soll_cap)

            for i in range(3):
                self.current_scene_action_excecute("fuben_"+soll_num)
                
                current_scene = self.scene_wait_to_dectect_scene()
                if "zhandou_fuben_info_no_tuandui" in current_scene.name:
                    self.scene_action_excecute("zhandou_fuben_info_no_tuandui","return")  
                    break
                elif "zhandou_jj_sg_sl_fuben_info" in current_scene.name:
                    self.scene_action_excecute("zhandou_jj_sg_sl_fuben_info","jingru_fuben_1")
                    self.sleep_time(3)
                    current_scene = self.scene_wait_to_dectect_scene()
                    if "zhandou_jj_sg_sl_fuben_info" in current_scene.name:
                        self.scene_action_excecute(current_scene.name,"return")     
                        self.current_scene_action_excecute("return")
                        return "finish"  
                    else:
                        self.zhandou_jingying_fuben()
                else:
                    self.sleep_time(1)
                    
        self.current_scene_action_excecute("return")
        return "done tuandui fuben"      
        
    def manage_jingying_fuben(self, max_cnt = 1): 
        if self.is_timeout() or self.action_point == False:
            return
        self.set_action_duration(max_cnt*event_max_time['jingying'])
            
        self.mainscreen_action_excecute("zhanyi")
        current_scene = self.scene_wait_to_dectect_scene()
        self.scene_action_excecute(current_scene.name,"to_jingying")
        current_scene = self.scene_wait_to_dectect_scene()
        while current_scene.name != "zhanyi_jingying_0"  and self.not_timeout():
            self.scene_action_excecute(current_scene.name,"previous")
            current_scene = self.scene_wait_to_dectect_scene()
        self.zhandou_jingying_fuben_loop(max_cnt)
        
    def manage_putong_fuben(self, max_cnt = 1): 
        if self.is_timeout() or self.action_point == False:
            return
        self.set_action_duration(max_cnt*event_max_time['putong'])
            
        self.mainscreen_action_excecute("zhanyi")
        self.sleep_time(1)
        current_scene = self.scene_wait_to_dectect_scene()
        while current_scene.name != "zhanyi_putong_0"  and self.not_timeout():
            self.scene_action_excecute(current_scene.name,"previous")
            current_scene = self.scene_wait_to_dectect_scene()
        for i in range(max_cnt):
            self.scene_action_excecute("zhanyi_putong_0","fuben_1")
            zhandou_result = self.zhandou_general_fuben()
            if zhandou_result == "shengli":
                pass
            elif zhandou_result == "notili":
                break
            else:
                break
            
        self.scene_action_excecute("zhanyi_putong_0","return")  
    
    def zhandou_jingying_fuben_loop(self, max_cnt = 1):
        if self.is_timeout() or self.action_point == False:
            return
        #random_fuben_begin = random.randint(0, 16)
        random_fuben_begin = 0
        skip_fuben_num = 0
        
        current_cnt = 0
        for fubenlist in fuben_capital:
            current_scene = self.scene_wait_to_dectect_scene()
            if "zhanyi_jingying" not in current_scene.name:
                break
            else:
                zhanyi_capital = current_scene.name
                print "current capital is: " , zhanyi_capital
            for fuben in fubenlist:
                skip_fuben_num += 1
                if skip_fuben_num < random_fuben_begin:
                    continue
                for x in range(3):
                    if "fuben" not in fuben or fuben == "":
                        continue
                    self.scene_action_excecute(zhanyi_capital,fuben)
                    zhandou_result = self.zhandou_general_fuben()
                    if zhandou_result == "shengli":
                        current_cnt += 1
                        if current_cnt >= max_cnt:
                            self.scene_action_excecute(zhanyi_capital,"return")
                            return # zhan dou ci shu man zu
                    elif zhandou_result == "notili" and zhandou_result == "shibai":
                        self.scene_action_excecute(zhanyi_capital,"return")  
                        return
                    elif zhandou_result == "notime":
                        break
                    else:
                        self.scene_action_excecute(zhanyi_capital,"return")  
                        return
                    
                    current_scene = self.scene_wait_to_dectect_scene()
                    if current_scene.name != zhanyi_capital:
                        self.scene_action_excecute(current_scene.name,"previous")  
                        current_scene = self.scene_wait_to_dectect_scene()
                        if current_scene.name != zhanyi_capital:
                            self.scene_action_excecute(current_scene.name,"return") 
                            return
                            
            if fubenlist != fuben_capital[-1]:
                print "next capital"
                self.scene_action_excecute(zhanyi_capital,"next")
            else:
                print "last captial"
        self.scene_action_excecute(zhanyi_capital,"return")  
        
    def zhandou_general_fuben(self):    
        if self.is_timeout():
            return False
        current_scene = self.scene_wait_to_dectect_scene()
        self.scene_action_excecute(current_scene.name,"jingru_fuben")
        
        current_scene = self.scene_wait_to_dectect_scene()
        if "invalid_fuben" in current_scene.name:
            self.scene_action_excecute(current_scene.name,"return")     
            return "notime"  
        elif "event_maitili" in current_scene.name:
            self.scene_action_excecute(current_scene.name,"return")
            current_scene = self.scene_wait_to_dectect_scene()
            self.scene_action_excecute(current_scene.name,"return")  
            self.action_point = False
            return "notili"# mein you ti li
        else:
            if self.zhandou_jingying_fuben():
                return "shengli"
            else:
                return "shibai"
            #Need to reprogram !!!!!!!!
        
    def zhandou_jingying_fuben(self): 
        if self.is_timeout():
            return False
        #self.scene_action_excecute("zhandou_jj_sg_sl_fuben_info","jingru_fuben")

        self.arrange_duiwu()
        current_scene = self.scene_wait_to_dectect_scene()    
        self.scene_action_excecute(current_scene.name,"jingru_fuben")
        self.zhandou_ing_smart_auto()
        return self.zhandou_jeshu_fuben()
        
    def zhandou_ing_smart_auto(self):
        if self.is_timeout():
            return
        
        current_scene = self.scene_wait_to_dectect_scene()
        while "zhandou_ing" not in current_scene.name and self.not_timeout():
            if self.is_timeout():
                return
            self.sleep_time(2)
            current_scene = self.scene_wait_to_dectect_scene()
        
        auto_action = current_scene.get_action_by_name("auto")
        previous_img = pointImageInGameWin(auto_action.action_point)
            
        self.scene_action_excecute(current_scene.name,"auto")
        
        if previous_img is not None:
            current_img = pointImageInGameWin(auto_action.action_point)
            if compareTwoImages(previous_img , current_img):
                current_scene = self.scene_wait_to_dectect_scene()
                while current_scene.name == "zhandou_ing" and self.not_timeout():
                    if self.is_timeout():
                        return
                    
                    point_list_auto_action = []
                    point_list_auto_action.append(current_scene.get_action_by_name("next").action_point)
                    point_list_auto_action.append(current_scene.get_action_by_name("hero_1").action_point)
                    point_list_auto_action.append(current_scene.get_action_by_name("hero_2").action_point)
                    point_list_auto_action.append(current_scene.get_action_by_name("hero_3").action_point)
                    point_list_auto_action.append(current_scene.get_action_by_name("hero_4").action_point)
                    point_list_auto_action.append(current_scene.get_action_by_name("hero_5").action_point)
                    mouseLeftClickMultiPoints(point_list_auto_action)
                    
                    #self.scene_action_excecute("zhandou_ing","next")
                    self.sleep_time(2)
                    current_scene = self.scene_dectector()
                    if current_scene == None:
                        self.sleep_time(2)
                        current_scene = self.scene_dectector()
                        if current_scene == None:
                            break
                    
    def putongshangren_buy(self): 
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['shangren'])
        
        self.mainscreen_action_excecute("shangren")
        self.sleep_time(1)
        current_scene = self.scene_wait_to_dectect_scene()
        if current_scene.name != "shangren_putong_mainwin":            
            self.scene_action_excecute(current_scene.name,"sell")
        buy_item_list = ("item_1","item_2","item_3","item_4","item_5","item_6","item_7","item_8")
        for item in buy_item_list:
            self.scene_action_excecute("shangren_putong_mainwin",item)
            current_scene = self.scene_wait_to_dectect_scene()
            if "shangren_bumai" in current_scene.name:
                self.scene_action_excecute(current_scene.name,"return")
                continue
            if current_scene.name != "shangren_buy_win":
                break
            self.scene_action_excecute("shangren_buy_win","buy")
        self.scene_action_excecute("shangren_putong_mainwin","return")
             
    def tiaozhan_jingjichang(self): 
        if self.is_timeout():
            return
        self.set_action_duration(event_max_time['jingjichang'])
        
        current_scene = self.scene_wait_to_dectect_scene()
        if "mainscreen_0" not in current_scene.name:
            return
        
        self.mainscreen_action_excecute("jingjichang")
        self.scene_action_excecute("event_jingjichang","tiaozhan")
        current_scene = self.scene_wait_to_dectect_scene()
        if current_scene.name == "event_jingjichang":
            self.scene_action_excecute("event_jingjichang","return")
            return
            
        self.arrange_duiwu()
        self.scene_action_excecute("zhandou_chuchang_yingxiong","jingru_fuben")
        self.zhandou_jeshu_fuben()
        self.scene_action_excecute("event_jingjichang","return")
    def wangzuozhita(self): 
        if self.is_timeout() or china_time().hour in [4]:
            return
        self.set_action_duration(event_max_time['wangzuozhita'])
        
        current_scene = self.scene_wait_to_dectect_scene()
        if "mainscreen_0" not in current_scene.name:
            return
        
        self.mainscreen_action_excecute("wangzuozhita")
        self.sleep_time(3)
        self.scene_action_excecute("event_wangzuozhita","tiaozhan")
        current_scene = self.scene_wait_to_dectect_scene()
        if current_scene.name == "event_wangzuozhita":
            self.scene_action_excecute("event_wangzuozhita","return")
            return
            
        self.arrange_duiwu()
        self.scene_action_excecute("zhandou_chuchang_yingxiong","jingru_fuben")
        self.zhandou_jeshu_fuben()
        self.scene_action_excecute("event_wangzuozhita","return")
    def fuben_event_shiguang(self):
        if self.is_timeout():
            return
        day = dotaTime_weekday()

        for fuben_name in shiguang_shilian_list[day]:
            if "shiguang" in fuben_name:
                self.fuben_shiguangzhixue(fuben_name,nandu[self.current_id][fuben_name])
    def fuben_event_shilian(self):
        if self.is_timeout():
            return
        day = dotaTime_weekday()

        for fuben_name in shiguang_shilian_list[day]:
            if "shilian" in fuben_name:
                self.fuben_yingxiongshilian(fuben_name,nandu[self.current_id][fuben_name])    
        
    def fuben_yingxiongshilian(self,fuben,nandu):
        if self.is_timeout() or self.action_point == False:
            return
        self.set_action_duration(event_max_time['shilian'])
        
        if nandu == "":
            return
        self.mainscreen_action_excecute("shilian")
        
        for i in range(5):
            self.set_action_duration(event_max_time['shilian'])
            self.scene_action_excecute("event_shilian",fuben)
            current_scene = self.scene_wait_to_dectect_scene()
            if current_scene.name == "event_shilian":
                self.scene_action_excecute("event_shilian","return")
                return
            
            current_scene = self.scene_wait_to_dectect_scene()
            if current_scene.name == "zhandou_xuanzhe_nandu":
                mouseDragLeftNandu()
                self.sleep_time(0.2)
                mouseDragLeftNandu()
                self.sleep_time(0.5)
                
            self.scene_action_excecute("zhandou_xuanzhe_nandu",nandu)
            current_scene = self.scene_wait_to_dectect_scene()
            if "zhandou_xuanzhe_nandu" in current_scene.name:
                self.scene_action_excecute(current_scene.name,"return")
                self.scene_action_excecute("event_shilian","return")
                return
    
            if "event_maitili" in current_scene.name:
                self.scene_action_excecute(current_scene.name,"return")
                self.scene_action_excecute("zhandou_xuanzhe_nandu","return")
                self.scene_action_excecute("event_shilian","return")
                self.action_point = False
                return
            #self.scene_action_excecute("zhandou_jj_sg_sl_fuben_info","jingru_fuben")
            
            while self.not_timeout():
                self.current_scene_action_excecute("saodang")
                #self.check_levelup()
                current_scene = self.scene_wait_to_dectect_scene()
                if "zhandou_found_something" in current_scene.name:
                    self.scene_action_excecute("zhandou_found_something", "return")
                    self.scene_action_excecute("zhandou_saodang", "return")
                elif "zhandou_saodang" in current_scene.name:
                    self.scene_action_excecute("zhandou_saodang", "return")
                elif "event_maitili" in current_scene.name:
                    self.return_to_main_screena()
                    self.action_point = False
                    return "notili"# mein you ti li
                else:
                    self.return_to_main_screena()
                    return "finish"# mein you ti li
                
            self.arrange_duiwu()
            self.scene_action_excecute("zhandou_chuchang_yingxiong","jingru_fuben")
            self.zhandou_ing_smart_auto()
            #self.scene_action_excecute("zhandou_ing","auto")
            self.zhandou_jeshu_fuben()
            self.sleep_time(1)
            
        self.scene_action_excecute("event_shilian","return")
         
    def fuben_shiguangzhixue(self,fuben,nandu): 
        if self.is_timeout() or self.action_point == False:
            return
        self.set_action_duration(event_max_time['shiguang'])
        
        if nandu == "":
            return
        self.mainscreen_action_excecute("shiguang")
        
        for i in range(2):
            self.set_action_duration(event_max_time['shiguang'])
            self.scene_action_excecute("event_shiguang",fuben)
            current_scene = self.scene_wait_to_dectect_scene()
            if current_scene.name == "event_shiguang":
                self.scene_action_excecute("event_shiguang","return")
                return
            
            current_scene = self.scene_wait_to_dectect_scene()
            if current_scene.name == "zhandou_xuanzhe_nandu":
                mouseDragLeftNandu()
                self.sleep_time(0.2)
                mouseDragLeftNandu()
                self.sleep_time(0.5)
                
            self.scene_action_excecute("zhandou_xuanzhe_nandu",nandu)
            current_scene = self.scene_wait_to_dectect_scene()
            if  "zhandou_xuanzhe_nandu" in current_scene.name:
                self.scene_action_excecute(current_scene.name,"return")
                self.scene_action_excecute("event_shiguang","return")
                return
            if "event_maitili" in current_scene.name:
                self.scene_action_excecute(current_scene.name,"return")
                self.scene_action_excecute("zhandou_xuanzhe_nandu","return")
                self.scene_action_excecute("event_shiguang","return")
                self.action_point = False
                return
            
            #self.scene_action_excecute("zhandou_jj_sg_sl_fuben_info","jingru_fuben")
            
            while self.not_timeout():
                self.current_scene_action_excecute("saodang")
                #self.check_levelup()
                current_scene = self.scene_wait_to_dectect_scene()
                if "zhandou_found_something" in current_scene.name:
                    self.scene_action_excecute("zhandou_found_something", "return")
                    self.scene_action_excecute("zhandou_saodang", "return")
                elif "zhandou_saodang" in current_scene.name:
                    self.scene_action_excecute("zhandou_saodang", "return")
                elif "event_maitili" in current_scene.name:
                    self.return_to_main_screena()
                    self.action_point = False
                    return "notili"# mein you ti li
                else:
                    self.return_to_main_screena()
                    return "finish"# mein you ti li
                    
            
            self.arrange_duiwu()
            self.scene_action_excecute("zhandou_chuchang_yingxiong","jingru_fuben")
            self.zhandou_ing_smart_auto()
            #self.scene_action_excecute("zhandou_ing","auto")        
            self.zhandou_jeshu_fuben()
            self.sleep_time(1)
            
        self.scene_action_excecute("event_shiguang","return")

    def fuben_event_mengjing(self):
        if self.is_timeout() or self.action_point == False:
            return
        self.set_action_duration(event_max_time['mengjing'])
        
        #self.mainscreen_action_excecute("mengjing")
        
        current_scene = self.scene_wait_to_dectect_scene()
        while "mainscreen" not in current_scene.name:
            self.current_scene_action_excecute("return")
            print "waiting to return to mainscreen"
            current_scene = self.scene_wait_to_dectect_scene()
            self.sleep_time(2)
            if self.is_timeout():
                return
            
        if current_scene.get_action_by_name("mengjing") == None:
            moveToRightEnd()
                
        self.scene_action_excecute("mainscreen_2","mengjing")

        self.scene_wait_scenes_with_string(["mengjing_main_win_0"])

        current_scene = self.scene_wait_to_dectect_scene()
        if "mengjing_main_win" not in current_scene.name:
            return
        
        self.scene_action_excecute("mengjing_main_win_0","jingru_fuben")
        self.unknown_screen_mouse_click([(1250, 223)])
        current_scene = self.scene_wait_to_dectect_scene()
        if "mengjing_fuben_info" not in current_scene.name:
            self.return_to_main_screena()
            return
        
        self.scene_action_excecute("mengjing_fuben_info_0","jingru_fuben")
        
        self.arrange_duiwu()
        self.scene_action_excecute("zhandou_chuchang_yingxiong","jingru_fuben")
        self.unknown_screen_mouse_click()
        self.zhandou_ing_smart_auto()
        #self.scene_action_excecute("zhandou_ing_mengjing_0","auto")
        self.zhandou_jeshu_fuben()
        self.return_to_main_screena()
        
    def zhandou_jeshu_fuben(self):
        if self.is_timeout():
            return False
        ret_val = False
        current_scene = screen_str()
        while ("zhandou_shibai" not in current_scene.name) and ("zhandou_shengli" not in current_scene.name)  and self.not_timeout() :        
            if self.is_timeout():
                return False
            current_scene = self.scene_dectector()
            while current_scene == None  and self.not_timeout():
                if self.is_timeout():
                    return False
                self.check_levelup()
                current_scene = self.scene_dectector()
                self.error_connect_again()
            
            if "zhandou_found_something" in current_scene.name:
                self.scene_action_excecute("zhandou_found_something", "return")
            self.sleep_time(1)
            self.error_connect_again()
        if "zhandou_shibai" in current_scene.name:
            ret_val =  False
        elif "zhandou_shengli" in current_scene.name:
            ret_val =  True
        self.scene_action_excecute(current_scene.name,"jieshu_fuben")
        return ret_val
    def scene_action_excecute(self, screen_name, action_name): 
        if self.is_timeout():
            return
        current_scene = screen_str()
        waiting_counter = 0
        while current_scene.name != screen_name and self.not_timeout():
            if self.is_timeout():
                return
            if waiting_counter > 5:
                print "cnt = ", waiting_counter, " waiting for screen: ", screen_name, " act: ", action_name
            waiting_counter += 1
            current_scene = self.scene_wait_to_dectect_scene()
            self.sleep_time(2)
            self.error_connect_again()
            
        cur_action = current_scene.get_action_by_name(action_name)
        try:
            init_action_img = pointImageInGameWin(cur_action.action_point)
            cur_action_img = init_action_img
        except:
            return
        while compareTwoImages(init_action_img , cur_action_img) and self.not_timeout():
            if self.is_timeout():
                return
            mouseLeftClickPoint(cur_action.action_point)
            self.sleep_time(2)
            self.error_connect_again()
            if cur_action.next_screen == "self":
                break
            cur_action_img = pointImageInGameWin(cur_action.action_point)
            print "action remain time:" + str(self.action_timeout_timer)
    def current_scene_action_excecute(self, action_name):
        if self.is_timeout():
            return
        current_scene = self.scene_wait_to_dectect_scene()
        if current_scene.get_action_by_name(action_name) != None:
            self.scene_action_excecute(current_scene.name, action_name)
            return True
        else:
            return False
        
    def mainscreen_action_excecute(self, action_name):
        if self.is_timeout():
            return
        
        current_scene = self.scene_wait_to_dectect_scene()
        while "mainscreen" not in current_scene.name:
            self.current_scene_action_excecute("return")
            print "waiting to return to mainscreen"
            current_scene = self.scene_wait_to_dectect_scene()
            self.sleep_time(2)
            if self.is_timeout():
                return
            
        if current_scene.get_action_by_name(action_name) == None:
            moveToRightEnd()
            current_scene = self.scene_wait_to_dectect_scene()
            if current_scene.get_action_by_name(action_name) == None:
                moveToLeftEnd()
                current_scene = self.scene_wait_to_dectect_scene()
                if current_scene.get_action_by_name(action_name) == None:
                    return False
                
        current_scene = self.scene_wait_to_dectect_scene()
        self.scene_action_excecute(current_scene.name,action_name)
            
def main():
    time.sleep(1)
    manager = act_manager()
    #manager.saodang_jingying_fuben(3)
    #manager.manage_jingying_fuben(1)
    #manager.manage_tuandui_fuben()
    #manager.cangbao_kaicai_and_search_once()
    #manager.shuipian_hecheng(500)
    #manager.yuanzheng_event_do_all()
    #manager.wangzuozhita()
    #manager.dota_logout()
    while 0:
        print manager.get_current_zhanyi_info()
    if 1:
        manager.scene_auto_action_manager()
        print get_cords()
        time.sleep(1)
    else:
        while 1:
            manager.scene_dectector()
            #print "CurrentFuben: ", manager.scene_find_current_fuben()
            print "CurrentMousePos: ", get_cords()
            time.sleep(1)



if __name__ == '__main__':
    main()