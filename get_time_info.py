from datetime import datetime,timedelta,tzinfo
class GMT8(tzinfo):
    delta=timedelta(hours=8)
    def utcoffset(self,dt):
        return self.delta
    def tzname(self,dt):
        return "GMT+8"
    def dst(self,dt):
        return self.delta

class GMT1(tzinfo):
    delta=timedelta(hours=1)
    def utcoffset(self,dt):
        return self.delta
    def tzname(self,dt):
        return "GMT+8"
    def dst(self,dt):
        return self.delta
    
class GMT2(tzinfo):
    delta=timedelta(hours=2)
    def utcoffset(self,dt):
        return self.delta
    def tzname(self,dt):
        return "GMT+8"
    def dst(self,dt):
        return self.delta

class GMT(tzinfo):
    delta=timedelta(0)
    def utcoffset(self,dt):
        return self.delta
    def tzname(self,dt):
        return "GMT+0"
    def dst(self,dt):
        return self.delta 

def china_time():
    #from_tzinfo=GMT2()#
    from_tzinfo=GMT2()#
    local_tzinfo=GMT8()#
    gmt_time = datetime.now()
    gmt_time = gmt_time.replace(tzinfo=from_tzinfo)
    china_time = gmt_time.astimezone(local_tzinfo)
    return china_time
        
def dotaTime_weekday():
    weekday =  china_time().weekday()
    if china_time().hour < 5:
        weekday -= 1
    return weekday

def dotaTime_is_gotTili():
    current_hour = china_time().hour
    if current_hour in [9,10,12,13,18,19,21,22,23]:
        return True
    return False

def main():
    print china_time().hour
    print dotaTime_weekday()
    print dotaTime_is_gotTili()
    
    
if __name__ == '__main__':
    main()
