import ImageGrab
from PIL import Image
import os
import time
import par

def screenGrab():
    im = ImageGrab.grab()
    #im.save('img//test.png', 'PNG')
    return im

def error_screen_grab_and_save():
    screenGrab().save(time.strftime("error_log//%Y%m%d_%H_%M_%S.png"))

def pointImageInGameWin(point):    
    left   = point[0] - 5 + par.default_game_rect[0]
    top    = point[1] - 5 + par.default_game_rect[1]
    right  = point[0] + 5 + par.default_game_rect[0]
    bottom = point[1] + 5 + par.default_game_rect[1]
    rect = (left,top,right, bottom )
    return screenGrab().crop(rect)    
    
def findObjectPos(obj, bg):    
    get_same_img = 0
    for j in range(0, bg.size[1]-obj.size[1]+1):
        for i in range(0, bg.size[0]-obj.size[0]+1):
            
            img_are_diff = 0
            for l in range(0, obj.size[1]):
                for k in range(0, obj.size[0]):
                    origin_pixel = bg.getpixel((i+k,j+l))
                    object_pixel = obj.getpixel((k,l))
                    if origin_pixel<>object_pixel:
                        img_are_diff = 1
                        break
                if img_are_diff == 1:
                    break
            if img_are_diff == 0:
                get_same_img = 1
                return (i,j)
                #print "got it"
                break
            
        if get_same_img == 1:
            break
    return None

def compareTwoImages(img1,img2):
    if findObjectPos(img1, img2) is not None:
        return True
    else:
        return False
 
def fastFindObjectPos(obj, bg, pos, tol=(0,0)): 
    size = obj.size
    left =  pos[0] - size[0] - tol[0]
    top =   pos[1] - size[1] - tol[1]
    right = pos[0] + size[0] + tol[0]
    bottom =pos[1] + size[1] + tol[1]
    rect = (left,top,right,bottom)
    obj_rel_pos = findObjectPos(obj, bg.crop(rect))
    try:
        return (obj_rel_pos[0]+left,obj_rel_pos[1]+top)
    except:
        return None
        
class gameWindow:
    def __init__(self):
        self.win_bl = Image.open('img//window//window_bl.png').convert("L")
        self.win_br = Image.open('img//window//window_br.png').convert("L")
        self.update_window_pos()
        self.screen = self.game_screen()
        
        
    def update_window_pos(self):
        background = ImageGrab.grab().convert("L") 
        #background = Image.open("calibrate_img.png").convert("L")#.crop(rect)
            
        pos_bl = fastFindObjectPos(self.win_bl, background, par.fast_search_point_bl)
        pos_br = fastFindObjectPos(self.win_br, background, par.fast_search_point_br)
            
        if ((pos_bl is None) or (pos_br is None)):
            print "search for whole screen"
            pos_bl = findObjectPos(self.win_bl, background)
            pos_br = findObjectPos(self.win_br, background)

        if not((pos_bl is None) or (pos_bl is None)):

            self.game_xl = pos_bl[0] + par.game_bl_corn_off_x()
            self.game_xr = pos_br[0] + par.game_br_corn_off_x()
            self.game_yb = pos_bl[1] + par.game_bl_corn_off_y()
            self.game_yt = self.game_yb - par.game_win_h()
            
        else:
            print "Cannot find simulator window"
            #print self.game_xl, self.game_xr,  self.game_yt, self.game_yb
    def game_screen(self):
        try:
            #print self.game_xl, self.game_yt, self.game_xr,  self.game_yb
            rect = (self.game_xl, self.game_yt, self.game_xr, self.game_yb)
            background = ImageGrab.grab().convert("L").crop(rect)
            
            #background = Image.open("error_log//20140903_03_50_10.png").convert("L").crop(rect)
            #background = ImageGrab.grab().crop(rect).save('screen.png')
            return background
        except:
            print "Cannot find game window!"
            return None
    
    def get_new_screen(self):
        self.screen = self.game_screen()
    
    def find_obj_in_area_in_new_screen(self, image_object, area = (0,0, par.game_win_w(), par.game_win_h())): 
        self.get_new_screen()
        return self.find_obj_in_area_in_old_screen(image_object, area)
        
    def find_obj_in_area_in_old_screen(self, image_object, area = (0,0, par.game_win_w(), par.game_win_h())): 
        return findObjectPos(image_object, self.screen.crop(area))
        #if 0:
            #print "found object"
            #return True
        #else:
            #print self.game_xl, self.game_yt, self.game_xr,  self.game_yb
            #print area[0], area[1],area[2],area[3]
            #print "cannot find object"
            #return False
            
    def find_obj_in_point_new_screen(self, image_object, point, tolerance = (5,5)):
        self.get_new_screen()
        return self.find_obj_in_point_old_screen(image_object, point, tolerance)
        
    def find_obj_in_point_old_screen(self, image_object, point, tolerance = (5,5)):
        left   = point[0] - tolerance[0]
        top    = point[1] - tolerance[1]
        right  = point[0] + tolerance[0]
        bottom = point[1] + tolerance[1]
        return self.find_obj_in_area_in_old_screen(image_object, (left,top,right,bottom))
    
    def find_obj_in_vertical(self, image_object, point, tolerance = (5,5)):
        self.get_new_screen()
        left   = 0
        top    = point[1] - tolerance[1]
        right  = par.game_win_w()
        bottom = point[1] + tolerance[1]
        return self.find_obj_in_area_in_old_screen(image_object, (left,top,right,bottom))

    def find_obj_in_horizontal(self, image_object, point, tolerance = (5,5)):
        self.get_new_screen()
        left   = point[0] - tolerance[0]
        top    = 0
        right  = point[0] + tolerance[0]
        bottom = par.game_win_h()
        return self.find_obj_in_area_in_old_screen(image_object, (left,top,right,bottom))


def main():
    print time.strftime("%Y%m%d_%H_%M_%S.png")
    error_screen_grab_and_save()
    #getGameWindowPos()
    #win = gameWindow()
        
    #win.game_screen()
    
    
    #bg = ImageGrab.grab().convert("L")
    #bg = Image.open('img//window//window_bl.png').convert("L")
    #bg.save("11.png")
    #obj = Image.open('img//window//window_br.png').convert("L")
    #obj.save("22.png")
    
    #bg = Image.open("10.png")
    #obj = Image.open("20.png")
    #obj.show()
    
    #hist = list(bg.getdata())
    #print '[%s]' % ', '.join(map(str, hist))
    #hist = list(obj.getdata())
    #print '[%s]' % ', '.join(map(str, hist))
         
    
    
if __name__ == '__main__':
    main()