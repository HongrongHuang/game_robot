import urllib,httplib,md5,time
class qq:
    def __init__(self,qq="",pwd=""):
        self.pwd=md5.new(pwd).hexdigest()
        self.headers=""
        self.qq=qq
        


    def getdata(self):
        self.conn= httplib.HTTPConnection("tqq.tencent.com:8000")#
        self.conn.request("POST","", self.headers)
        response = self.conn.getresponse()                                      
        print response.read().decode('utf-8').encode("cp936")
        self.conn.close


    def Login(self):#
        self.headers=("VER=1.0&CMD=Login&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq+"&PS="+\
                      self.pwd+\
                      "&M5=1&LC=9326B87B234E7235")
        self.getdata()      
        
        
    def Query_Stat(self):#
        self.headers=("VER=1.0&CMD=Query_Stat&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq+"&TN=50&UN=0")
                      
        self.getdata() 
        
    def List(self):#
        self.headers=("VER=1.0&CMD=List&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq+"&TN=160&UN=0")
        
        self.getdata()


    def GetInfo(self,friend=""):#
        self.headers=("VER=1.0&CMD=GetInfo&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq+"&LV=2&UN="+\
                      friend)
        
        self.getdata() 


    def AddToList(self,friend=""):#
        self.headers=("VER=1.0&CMD=AddToList&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq+"&UN="+\
                      friend)
        
        self.getdata()


    def GetMsg(self):#
        self.headers=("VER=1.0&CMD=GetMsgEx&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq)
        
        self.getdata()


    def SendMsg(self,friend="",msg=""):#
        self.headers=("VER=1.0&CMD=CLTMSG&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq+"&UN="+\
                      friend+"&MG="+\
                      msg.decode("cp936").encode('utf-8'))
        
        self.getdata()


    def Logout(self):#
        self.headers=("VER=1.0&CMD=Logout&SEQ="+\
                      str(int(time.time()*100)%(10**5))+"&UIN="+\
                      self.qq)
        
        self.getdata()


class myQQ():   
    def __init__(self): 
        self.QQ=qq('2967891620','1q2w3e')
    
    def login(self):
        self.QQ.Login()
        
    def send_msg(self, msg):
        self.QQ.SendMsg('329073497',msg)
    
    def logout(self):
        self.QQ.Logout()

def main():
    my_test_qq = myQQ()
    my_test_qq.login() 
    my_test_qq.send_msg("Hello!")
    my_test_qq.logout()
    
if __name__ == '__main__':
    main()