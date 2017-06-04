import xlrd
import xlwt
import itertools
from xlutils.copy import copy

class dota_event:
    def __init__(self):
        self.jingjichang = 0
        self.shiguang_1  = 0
        self.shiguang_2  = 0
        self.shilian_1   = 0
        self.shilian_2   = 0
        self.shilian_3   = 0
        self.yuanzheng   = 0
        self.putong      = 0
        self.jingying    = 0
        self.tuandui     = 0
        self.dianjing    = 0
        self.shangren    = 0
        self.baoxiang    = 0
        self.xingxiang   = 0
        self.huodong     = 0
        
def get_sheet_by_name(book, name):
    """Get a sheet by name from xlwt.Workbook, a strangely missing method.
    Returns None if no sheet with the given name is present.
    """
    # Note, we have to use exceptions for flow control because the
    # xlwt API is broken and gives us no other choice.
    try:
        for idx in itertools.count():
            sheet = book.get_sheet(idx)
            if sheet.name == name:
                return sheet
    except IndexError:
        return None
    
def get_sheet_idx_by_name(book, name):
    """Get a sheet by name from xlwt.Workbook, a strangely missing method.
    Returns None if no sheet with the given name is present.
    """
    # Note, we have to use exceptions for flow control because the
    # xlwt API is broken and gives us no other choice.
    try:
        for idx in itertools.count():
            sheet = book.get_sheet(idx)
            if sheet.name == name:
                return idx
    except IndexError:
        return None
    
class user_event:
    def __init__(self):
        self.username = ""
        self.availible_event = {}
        self.default_event = {}
        
    def daily_update(self, weekday_nr):
        for key, value in self.default_event.iteritems() :
            self.availible_event[key] = value
        
        
class user_group_event:
    def __init__(self):
        self.user_event_list = []
        pass
    def read_excel(self,file_name):
        book = xlrd.open_workbook(file_name)
        availible_event_sheet = book.sheet_by_name('availible')
        default_event_sheet = book.sheet_by_name('default')
        rows = availible_event_sheet.nrows
        cols = availible_event_sheet.ncols
        event_nr = rows - 1
        user_nr = cols - 1
        for user in range(user_nr):
            temp = user_event()
            temp.username = availible_event_sheet.cell(0, user+1).value
            for event in range(event_nr):
                temp.availible_event[availible_event_sheet.cell(event+1, 0).value] = int(availible_event_sheet.cell(event+1, user+1).value)
                temp.default_event[default_event_sheet.cell(event+1, 0).value]     = int(default_event_sheet.cell(event+1, user+1).value)
            self.user_event_list.append(temp)
            
    def read_availible_event_from_excel(self,file_name):
        book = xlrd.open_workbook(file_name)
        availible_event_sheet = book.sheet_by_name('availible')
        rows = availible_event_sheet.nrows
        cols = availible_event_sheet.ncols
        event_nr = rows - 1
        user_nr = cols - 1
        for user in range(user_nr):
            temp = user_event()
            temp.username = availible_event_sheet.cell(0, user+1).value
            for event in range(event_nr):
                temp.availible_event[availible_event_sheet.cell(event+1, 0).value] = int(availible_event_sheet.cell(event+1, user+1).value)
            self.user_event_list.append(temp)
            
    def write_availible_event_to_excel(self,file_name):
        
        read_book = xlrd.open_workbook(file_name)
        availible_event_sheet = read_book.sheet_by_name('availible')
        
        book = copy(xlrd.open_workbook(file_name))
        sheet_nr = get_sheet_idx_by_name(book, 'availible')
        event_nr = len(self.user_event_list[0].availible_event)
        user_nr = len(self.user_event_list)
        for user in range(user_nr):
            for event in range(event_nr):
                event_name = availible_event_sheet.cell(event+1, 0).value
                book.get_sheet(sheet_nr).write(event+1, user+1, self.user_event_list[user].availible_event[event_name])
        book.save('book2.xls')
        
    def availible_event_daily_update(self, weekday_nr):
        
        for user in self.user_event_list:
            user.daily_update(weekday_nr)
            
        
book = xlrd.open_workbook('daily_event.xls')

print book.nsheets
print book.sheet_names()

sh = book.sheet_by_index(0)
print sh.name, sh.nrows, sh.ncols

def main():
    test = user_group_event()
    test.read_excel('daily_event.xls')
    #test.read_availible_event_from_excel('daily_event.xlsx')
    test.availible_event_daily_update(1)
    test.write_availible_event_to_excel('daily_event.xls')

if __name__ == '__main__':
    main()