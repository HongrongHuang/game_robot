

            
#game_width = 1532 - 113
#game_height = 896 - 45
# game window parameter calibration
# first number is the real position, second number is the find position from find_bitmap
# use the bottom left corner
#game_offset_xl = 113 - 24
#game_offset_yb = 896 - 906
#use the bottom right corner
#game_offset_xr = 1532 - 1499
#game_offset_yb = 896  - 906

game_window = [1532 - 113,  897 - 45]
game_bl_corner_offset = [113 - 48, 896 - 914]
game_br_corner_offset = [1532 - 1512, 896  - 914]

fast_search_point_bl = [48 + 224/2, 915 + 30/2]
fast_search_point_br = [1513 + 110/2, 915 + 30/2]

default_game_rect = [113, 45, 1533, 897]

def game_win_w():
    return game_window[0]
    
    
def game_win_h():
    return game_window[1]

def game_bl_corn_off_x():
    return game_bl_corner_offset[0]

def game_bl_corn_off_y():
    return game_bl_corner_offset[1]

def game_br_corn_off_x():
    return game_br_corner_offset[0]

def game_br_corn_off_y():
    return game_br_corner_offset[1]