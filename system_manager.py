#I have used os comands for a while
#this program will try to close a firefox window every ten secounds
###
import os
import time
#creating a forever loop

def terminate_bluestacks():
    if False:
        # old Version
        os.system("TASKKILL /F /IM HD-Adb.exe")
        os.system("TASKKILL /F /IM HD-Agent.exe")
        os.system("TASKKILL /F /IM HD-BlockDevice.exe")
        os.system("TASKKILL /F /IM HD-Frontend.exe")
        os.system("TASKKILL /F /IM HD-LogRotatorService.exe")
        os.system("TASKKILL /F /IM HD-Network.exe")
        os.system("TASKKILL /F /IM HD-RunApp.exe")
        os.system("TASKKILL /F /IM HD-Service.exe")
        os.system("TASKKILL /F /IM HD-SharedFolder.exe")
        os.system("TASKKILL /F /IM HD-UpdaterService.exe")
    elif True:
        os.system("TASKKILL /F /IM BluestacksGP.exe")
        os.system("TASKKILL /F /IM BstkSVC.exe")
        os.system("TASKKILL /F /IM HD-Agent.exe")
        os.system("TASKKILL /F /IM HD-Frontend.exe")
        os.system("TASKKILL /F /IM HD-LogRotatorService.exe")
        os.system("TASKKILL /F /IM HD-Plus-Service.exe")
    else:
        os.system("TASKKILL /F /IM HD-Frontend.exe")
    time.sleep(5)
    
def run_bluestacks():
    #cmdline =  r'"C:\Program Files (x86)\BlueStacks\HD-StartLauncher.exe"'
    cmdline =  r'"C:\Program Files (x86)\BluestacksCN\BluestacksGP.exe"'
    os.system(cmdline)
    #raw_input()
    time.sleep(15)

def relaunch_bluestacks(gab_time = 120):
    try:
        terminate_bluestacks()
    except:
        pass
    time.sleep(gab_time)
    run_bluestacks()
    
    
def main():
    #relaunch_bluestacks()
    terminate_bluestacks()
    run_bluestacks()
    pass
    
if __name__ == '__main__':
    main()