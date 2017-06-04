
import par
import time
import win32api, win32con

from par import default_game_rect as win_rect

x_offset = win_rect[0]
y_offset = win_rect[1]
class mouseClass():
    def __init__(self, offset_x=0, offset_y=0, range_x=400, range_y=400):
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        self.game_window_range_x = range_x
        self.game_window_range_y = range_y
        
        self.game_window_center_x = self.game_window_range_x / 2
        self.game_window_center_y = self.game_window_range_y / 2
        
    def leftPress(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        
    def leftRelease(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

    def leftClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        print "Left Click"
    def rightClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        print "Right Click"
    def moveMouseTo(self,cord):
        win32api.SetCursorPos((self.offset_x+cord[0],self.offset_y+cord[1]))
    def getMousePos(self):
        x,y = win32api.GetCursorPos()
        x = x - self.offset_x
        y = y - self.offset_y
        #print x,y
        return (x,y)

    def mouseLeftClickPoint(self, target_click_pos):
        
        x,y = self.getMousePos()

        self.moveMouseTo(target_click_pos)
        time.sleep(0.02)
        self.leftClick()
        
        self.moveMouseTo((x,y))
            
    def mouseLeftClickMultiPoints(self, point_list):
        
        x,y = win32api.GetCursorPos()
        
        for point in point_list:
            self.moveMouseTo(point)
            time.sleep(0.02)
            self.leftClick()
    
        self.moveMouseTo((x,y))


    def mouseDragEvent(self, press_point, release_point):
        time.sleep(0.1)
        self.moveMouseTo(press_point)
        time.sleep(0.3)
        self.leftPress()
        time.sleep(0.3)
        self.moveMouseTo(release_point)
        time.sleep(0.3)
        self.leftRelease()
        time.sleep(0.1)
        
    
    def moveToLeft(self):
        pass
    def moveToRight(self):
        pass

def keypress(str_input):
    for char in str_input:
        win32api.keybd_event(ord(char),0) 

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print "Click"
        
def mouseOffset(offset = (0,0)):
    x,y = win32api.GetCursorPos()
    win32api.SetCursorPos((x+offset[0],y+offset[1]))
    
def mousePos(cord):    
    win32api.SetCursorPos((x_offset+cord[0],y_offset+cord[1]))
    
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_offset
    y = y - y_offset
    #print x,y
    return (x,y)
    

def set_cords(x,y):
    win32api.SetCursorPos(x,y)
    print x,y

def mouseLeftClickPoint(target_click_pos):
    
    mod = 1
    if mod == 0:
        mousePos(target_click_pos)
        time.sleep(0.1)
        leftClick()
    elif mod == 1:
        x,y = win32api.GetCursorPos()

        mousePos(target_click_pos)
        time.sleep(0.02)
        leftClick()
        
        win32api.SetCursorPos((x,y))

def mouseLeftClickMultiPoints(point_list):
    
    x,y = win32api.GetCursorPos()
    
    for point in point_list:
        mousePos(point)
        time.sleep(0.02)
        leftClick()

    win32api.SetCursorPos((x,y))
        
def mouseCenter():    
    win32api.SetCursorPos((x_offset+par.game_win_w()/2,y_offset+par.game_win_h()/2))
    
def mouseDragLeftNandu():
    time.sleep(0.1)
    win32api.SetCursorPos((x_offset+par.game_win_w()/2-300,y_offset+par.game_win_h()/2))
    time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.3)
    for i in range(13):
        win32api.SetCursorPos((x_offset+par.game_win_w()/2-300 + i*100,y_offset+par.game_win_h()/2))
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.1)
    print "Mouse Drag Down"
    
def mouseDragDown():
    time.sleep(0.1)
    win32api.SetCursorPos((x_offset+par.game_win_w()/2,y_offset+par.game_win_h()/2+300))
    time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.3)
    for i in range(50):
        win32api.SetCursorPos((x_offset+par.game_win_w()/2,y_offset+par.game_win_h()/2+300 - i*10))
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.1)
    print "Mouse Drag Down"
    
def moveToLeftEnd():
    for x in range (5):
        time.sleep(0.1)
        win32api.SetCursorPos((x_offset+par.game_win_w()/2,y_offset+840))
        time.sleep(0.3)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(0.3)
        win32api.SetCursorPos((x_offset+par.game_win_w()/2+600,y_offset+840))
        time.sleep(0.3)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(0.1)
    print "Move To the Left End"
    

def moveToRightEnd():
    for x in range (5):
        time.sleep(0.1)
        win32api.SetCursorPos((x_offset+par.game_win_w()/2,y_offset+840))
        time.sleep(0.3)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(0.3)
        win32api.SetCursorPos((x_offset+par.game_win_w()/2-600,y_offset+840))
        time.sleep(0.3)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(0.1)
    print "Move To the Right End"
    


def main():
    #mouseDragDown()
    #mouseDragLeftNandu()
    pass
    print get_cords()
    leftClick()
    #get_cords()
    #mousePos((400,400))
    #leftClick()
    #time.sleep(2)
    #win32api.keybd_event(win32con.VK_NUMPAD2,0)
    
def test():
    test_mouse = mouseClass()
    cord = test_mouse.getMousePos()
    print test_mouse.moveMouseTo((cord[0] + 100, cord[1] + 0))
    test_mouse.mouseLeftClickPoint((400,400))
    
    
if __name__ == '__main__':
    #main()
    test()