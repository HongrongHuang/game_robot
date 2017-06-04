import xml.etree.ElementTree as ET
import xml.dom.minidom as DM
'''tree = ET.parse('test_xml_file.xml')
root = tree.getroot()

print root.tag, root.attrib

for child in root:
    print child.tag, child.attrib
    
for neighbor in root.iter('neighbor'):
    print neighbor.attrib
    
for rank in root.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
    rank.set('updated', 'yes')
'''
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = DM.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")
class screen_image_str():
    def __init__(self):
        self.id = 0
        self.pos = (0,0)
        self.path = ""
        
class screen_action_str():
    def __init__(self):
        self.id = 0
        self.name = ""
        self.action_point = (0,0)
        self.next_screen = ""
        
class screen_str:
    def __init__(self):
        
        self.name = "screen_name"
        self.id = 1
        self.image_list = []
        self.action_list = []
        self.current_image_id = 0
        self.current_action_id = 0
    def set_screen_name(self, in_name):
        self.name = in_name
        
    def set_screen_id(self, in_id):
        self.id = in_id
        
    def add_ref_image(self, img_pos, img_path):
        temp_img = screen_image_str()
        temp_img.id = self.current_image_id
        temp_img.pos = img_pos
        temp_img.path = img_path
        self.add_ref_image_str(temp_img)
        
    def add_screen_action(self, name, act_pos, next_screen):
        temp_act = screen_action_str()
        temp_act.name = name
        temp_act.action_point = act_pos
        temp_act.next_screen = next_screen
        self.add_screen_action_str(temp_act)
        
    def add_ref_image_str(self, img_str):
        self.image_list.append(img_str)
        self.current_image_id = self.current_image_id + 1
        
    def add_screen_action_str(self, act_str):
        self.action_list.append(act_str)
        self.current_action_id = self.current_action_id + 1
        
    def get_screen_name(self):
        return self.name
    
    def get_screen_id(self):
        return self.id
        
    def get_all_ref_images(self):
        return self.image_list
    
    def get_all_screen_actions(self):
        return self.action_list
    
    def get_action_position(self, action_name):
        for action in self.action_list:
            if action.name == action_name:
                return action.action_point
        return None
    def get_action_by_name(self, action_name):
        for action in self.action_list:
            if action.name == action_name:
                return action
        return None
    def get_action_next_screen(self, action_name):
        for action in self.action_list:
            if action.name == action_name:
                return action.next_screen
        return None
    
class action_str:
    def __init__(self, id=0, pos=(0, 0), img=""):
        
        self.id = 1
        self.art = "img_pos_act"
        self.position = (0, 0)
        self.image = ""
        self.action_time = 1000
        self.response_time = 1000
        self.set_action(id, pos, img)
        
    def set_action(self, id, pos, img):
        self.id = id
        self.art = "img_pos_act"
        self.position = pos
        self.image = img
        self.action_time = 1000
        self.response_time = 1000
        
    def set_id(self, input_info):
        self.id = input_info
    def set_art(self, input_info):
        self.art = input_info
    def set_position(self, input_info):
        self.position = input_info
    def set_image_path(self, input_info):
        self.image = input_info
    def set_action_duration(self, input_info):
        self.action_time = input_info
    def set_response_duration(self, input_info):
        self.response_time = input_info
                
    def get_id(self):
        return self.id
    def get_art(self):
        return self.art
    def get_position(self):
        return self.position
    def get_image_path(self):
        return self.image
    def get_action_duration(self):
        return self.action_time
    def get_response_duration(self):
        return self.response_time

class screen_loader:
    def __init__(self,file_name):
        self.screen_list = []
        self.read_action_in_new_xml(file_name)
                        
    def read_screen_info_in_screen_list(self, screen_xml):
        temp_screen = screen_str()
        temp_screen.set_screen_name(screen_xml.get("name"))
        for screen_item in screen_xml:
            if screen_item.tag == "screen_id":
                temp_screen.set_screen_id(int(screen_item.text))
            if screen_item.tag == "image":
                temp_image = screen_image_str()
                for image in screen_item:
                    if image.tag == "image_id":
                        temp_image.id = int(image.text)
                    elif image.tag == "position":
                        for d in image:
                            if d.tag == "x":
                                temp_x = int(d.text)
                            elif d.tag == "y":
                                temp_y = int(d.text)
                        temp_image.pos = (temp_x,temp_y)
                    elif image.tag == "image_path":
                        temp_image.path = image.text.strip()
                temp_screen.add_ref_image_str(temp_image)
            if screen_item.tag == "action":
                temp_action = screen_action_str()
                for action in screen_item:
                    if action.tag == "action_id":
                        temp_action.id = int(action.text)
                    elif action.tag == "name":
                        temp_action.name = str(action.text)
                    elif action.tag == "action_point":
                        for d in action:
                            if d.tag == "x":
                                temp_x = int(d.text)
                            elif d.tag == "y":
                                temp_y = int(d.text)
                        temp_action.action_point = (temp_x,temp_y)
                    elif action.tag == "next_screen":
                        temp_action.next_screen = action.text.strip()
                temp_screen.add_screen_action_str(temp_action)
        self.screen_list.append(temp_screen)
    
    def read_action_in_new_xml(self,file_name):    
        tree = ET.parse(file_name)
        root = tree.getroot()        
        for screen_list in root:
            for screen_group in screen_list:
                if screen_group.tag == "screen_group":
                    for screen in screen_group:
                        self.read_screen_info_in_screen_list(screen)
                if screen_group.tag == "screen":
                    self.read_screen_info_in_screen_list(screen_group)
    
    def get_all_screen(self):
        return self.screen_list
    
class action_loader:
    def __init__(self,file_name):
        tree = ET.parse(file_name)
        self.root = tree.getroot()
        self.current_act_pointer = 0
        self.action_list = []
        
        for event in self.root:
            for action in event:
                temp_action = action_str()
                for act_info in action:
                    if act_info.tag == "identity":
                        temp_action.set_id(int(act_info.text))
                    elif act_info.tag == "art":
                        temp_action.set_art(act_info.text.strip())
                    elif act_info.tag == "position":
                        for d in act_info:
                            if d.tag == "x":
                                temp_x = int(d.text)
                            elif d.tag == "y":
                                temp_y = int(d.text)
                        temp_action.set_position((temp_x,temp_y))
                    elif act_info.tag == "image":
                        temp_action.set_image_path(act_info.text.strip())
                    elif act_info.tag == "time":
                        for d in act_info:
                            if d.tag == "action_time":
                                temp_action.set_action_duration( int(d.text))
                            elif d.tag == "response_time":
                                temp_action.set_response_duration( int(d.text))
                self.action_list.append(temp_action)
                
    def get_action(self,num = None):
        
        if num == None:  
            num = self.current_act_pointer
            self.current_act_pointer = self.current_act_pointer + 1
        try:
            return self.action_list[num]
        except:
            return
    def get_all_action(self):
        return self.action_list
    

#load = action_loader('output2.xml')      
#load.get_action()

class screen_recorder:
    def __init__(self):
        self.root = ET.Element("root")
        self.screen_list = ET.SubElement(self.root, "screen_list")
        self.counter = 1;

    def add_screen(self, screen_name):
        self.screen = ET.SubElement(self.screen_list, "screen")
        self.screen.set("name",screen_name)
        self.screen_img_counter = 1
        
        identity = ET.SubElement(self.screen, "screen_id")
        #identity.set("name", "blah")
        identity.text = str(self.counter)
        self.counter = self.counter + 1        
    
    def add_ref_img_in_screen(self, pos_info, img_path_info):
        image  = ET.SubElement(self.screen, "image")
        identity = ET.SubElement(image, "image_id")
        #identity.set("name", "blah")
        identity.text = str(self.screen_img_counter)
        self.screen_img_counter = self.screen_img_counter + 1
        
        position = ET.SubElement(image, "position")
        pos_x = ET.SubElement(position, "x")
        pos_x.text = str(pos_info[0])
        pos_y = ET.SubElement(position, "y")
        pos_y.text = str(pos_info[1])
        
        image = ET.SubElement(image, "image_path")
        image.text = img_path_info

    def save_screen(self, xml_file_name):
        #tree = ET.ElementTree(self.root)
        #tree.write(xml_file_name)
        
        text_file = open(xml_file_name, "w")
        text_file.write("%s" % prettify(self.root))
        text_file.close()
        print xml_file_name, "is saved!"
        #print prettify(self.root)
    
    
class action_recorder:
    def __init__(self):
        self.root = ET.Element("root")
        self.event = ET.SubElement(self.root, "event")
        self.counter = 1;

    def add_act(self, action = action_str()):
        self.add_action(action.position, action.image, action.art, [action.action_time,action.response_time])

    def add_action(self, pos_info, img_path, action_art = "img_pos_act", time_info = (1000, 1000)):
        action = ET.SubElement(self.event, "action")
        identity = ET.SubElement(action, "identity")
        #identity.set("name", "blah")
        identity.text = str(self.counter)
        self.counter = self.counter + 1
        
        art = ET.SubElement(action, "art")
        art.text = action_art
        
        position = ET.SubElement(action, "position")
        pos_x = ET.SubElement(position, "x")
        pos_x.text = str(pos_info[0])
        pos_y = ET.SubElement(position, "y")
        pos_y.text = str(pos_info[1])
        
        image = ET.SubElement(action, "image")
        image.text = img_path
        
        
        time = ET.SubElement(action, "time")
        action_time = ET.SubElement(time, "action_time")
        action_time.text = str(time_info[0])
        response_time = ET.SubElement(time, "response_time")
        response_time.text = str(time_info[1])

    def save_action(self, xml_file_name):
        #tree = ET.ElementTree(self.root)
        #tree.write(xml_file_name)
        
        text_file = open(xml_file_name, "w")
        text_file.write("%s" % prettify(self.root))
        text_file.close()
        print xml_file_name, "is saved!"
        #print prettify(self.root)
def main():
    
    if 1:
        record = screen_recorder()
        temp = screen_str()
        temp.set_screen_id(1)
        temp.set_screen_name("screen1")
        temp.add_ref_image((100,200), "image1.png")
        temp.add_ref_image((100,300), "image2.png")
        
        record.add_screen("screen1")
        record.add_ref_img_in_screen((100,200), "image1.png")
        record.add_ref_img_in_screen((100,300), "image2.png")
        record.add_screen("screen2")
        record.add_ref_img_in_screen((100,300), "image3.png")
        
        record.save_screen("output.xml")
        
        loader = screen_loader("img//element//allscene.xml")

        print loader.screen_list[9].image_list[0].pos
        print loader.screen_list[9].image_list[0].path
        print loader.screen_list[9].action_list[0].name
        print loader.screen_list[9].action_list[0].action_point

        
        
        #main = action_recorder()
        #main.add_act(action_str("",(1000,2000),"image1.png"))
        #main.add_action((300,400),"image2.png")
        #main.save_action("output.xml")
        
    
    if 0:
        tree = ET.parse("img//event//output.xml")
        root = tree.getroot()
        text_file = open("img//event//output2.xml", "w")
        text_file.write("%s" % prettify(root))
        text_file.close()
    
if __name__ == '__main__':
    main()