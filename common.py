#coding=utf-8

import unittest
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from datetime import datetime

By.ACCESSIBILITY_ID = MobileBy.ACCESSIBILITY_ID
By.ANDROID_UIAUTOMATOR = MobileBy.ANDROID_UIAUTOMATOR
fota_cu = "8090-V1FOTA0"
fota_fv = "8EA2ZZ20"
fota_imei = "358511032234522"
def capabilities_set(device_num):
    capabilities = {}
    if device_num == 1:
        capabilities['platformVersion'] = '6.0'
    if device_num == 2:
        capabilities['platformVersion'] = '7.0'
        capabilities['automationName'] = 'UIAutomator2'

    capabilities['unicodeKeyboard'] = 'True'
    capabilities['platformName'] = 'Android'
    capabilities['deviceName'] = 'Android Emulator'
    capabilities['noSign'] = 'True'
    capabilities['resetKeyboard'] = 'True'
    capabilities['appPackage'] = 'com.tcl.ota'
    capabilities['appActivity'] = 'com.tcl.ota.SystemUpdatesActivity'
    capabilities['app'] = 'C:\\Users\\77465\\eclipse-workspace\\appiumdemo\\apps\\Fota_Global_v7.0.10.3.0626.0_signed_platformkey_alldpi.apk'
    capabilities['noReset'] = 'True'

    return capabilities

def allapp_find_app(device,appname):
    device.keyevent(3)
    time.sleep(2)
    el1 = device.find_element_by_accessibility_id("ALL APPS")
    el1.click()
    time.sleep(2)
    return swape_findelm(device,"allappdown", appname)

def recent_find_app(device,appname):
    device.keyevent(1)
    time.sleep(1)
    return swape_findelm(device,"recentup", appname, )

def swape_bygiven(device,distance):
    x = device.get_window_size()['width']
    y = device.get_window_size()['height']
    if distance == "dragdown":
        device.swipe(x / 2 , y / 20,x / 2,y / 2,1000)
    if distance == "left2right":
        device.swipe(x / 20,y / 2,x * 19 / 20,y / 2,1000)
    if distance == "allappdown":
        device.swipe(x / 2, y * 3 / 4, x / 2, y / 4, 1000)
    if distance == "recentup":
        device.swipe(x / 2, y / 4, x / 2, y * 3 / 4, 1000)
    if distance == "right2left":
        device.swipe(x * 5 / 6, y / 2, x / 6, y / 2, 1000)

def swape_app2homescreen(device,appname):
    try:
        updateelm1 = allapp_find_app(device,appname)
    except CantFindAppException, e:
        print e
    else:
        x = device.get_window_size()['width'] / 2
        y = device.get_window_size()['height'] / 2

        TouchAction(device).long_press(updateelm1).move_to(x=x, y=y).release().perform()

def swape_findelm(device,distance,value="Updates",by=By.ACCESSIBILITY_ID):
    while True:
        str1 = device.page_source
        try:
            appelm = device.find_element(by,value)
        except NoSuchElementException:
            swape_bygiven(device, distance)
        else:
            return appelm

        str2 = device.page_source
        if (str1 == str2):
            raise CantFindAppException()

def open_appinhomescreen(device,appname):
    device.keyevent(3)
    try:
        device.find_element_by_accessibility_id(appname).click()
    except NoSuchElementException,e:
        print e
        return False
    else:
        return True

def read_logs(driver, log_type, ignore=False):
    raw_logs = driver.get_log(log_type)
    if ignore: return []

    logs = []
    for raw_log in raw_logs:
        timestamp_sec = raw_log['timestamp'] / 1000
        time_str = datetime.fromtimestamp(timestamp_sec).strftime('%Y-%m-%d %H:%M:%S')
        log = '%s %s' % (time_str, raw_log['message'])
        logs.append(log)

    return logs

def write_logs(logs, to_file):
    with open(to_file, 'wb') as f:
        lines = [log.encode('utf-8') + '\n' for log in logs]
        f.writelines(lines)
    return logs

def enable_fota_advance(device,type):
    if type == "FOTA":
        cu = "8090-V1FOTA0"
        fv = "8EA2ZZ20"
        imei = "358511032234522"

    if type == "AOTA":
        cu = "AOTATEST6"
        fv = "8EA2ZZ20"
        imei = "358511032234522"

    device.launch_app()
    device.find_element_by_accessibility_id("More options").click()
    device.find_element_by_android_uiautomator('new UiSelector().text("Help")').click()
    cfu_elm = device.find_element_by_android_uiautomator('new UiSelector().text("Checking for updates")')
    for i in range(1,10):
        try:
            pwdinput = device.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")')
        except NoSuchElementException, e:
            cfu_elm.click()
            time.sleep(1)
        else:
            pwdinput.send_keys("20180201")
            break
    try:
        device.find_element_by_id("android:id/button1").click()
    except NoSuchElementException, e:
        print "advance mode already enabled"
    else:
        pass
    device.keyevent(4)
    try:
        device.find_element_by_android_uiautomator('new UiSelector().text("Password incorrect")')
    except NoSuchElementException,e:
        print "open fota advance mode success"
        device.find_element_by_accessibility_id("More options").click()
        device.find_element_by_android_uiautomator('new UiSelector().text("FOTA test")').click()
        device.find_element_by_id("android:id/switchWidget").click()
        device.find_element_by_android_uiautomator('new UiSelector().text("Emulated CU Reference")').click()
        device.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")').send_keys(cu)
        device.find_element_by_id("android:id/button1").click()
        device.find_element_by_android_uiautomator('new UiSelector().text("Emulated current version")').click()
        device.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")').send_keys(fv)
        device.find_element_by_id("android:id/button1").click()
        device.find_element_by_android_uiautomator('new UiSelector().text("Emulated IMEI")').click()
        device.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")').send_keys(imei)
        device.find_element_by_id("android:id/button1").click()
        device.find_element_by_android_uiautomator('new UiSelector().text("Start Test")').click()
        print device.current_activity
        time.sleep(3)
        return True


    else:
        print "failed to open fota advance mode"
        return False



def delete_fotapac(device):
    device.keyevent(3)
    device.launch_app()
    device.find_element_by_accessibility_id("More options").click()
    device.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
    try:
        print "try to find package in setting"
        delete_icon = device.find_element_by_id("com.tcl.ota:id/pref_button")
    except NoSuchElementException,e:
        print " no package"
        pass
    else:
        delete_icon.click()
        time.sleep(2)
        device.find_element_by_android_uiautomator('new UiSelector().text("Delete")').click()

def click_checkfota(device,buttontype,network):   #关闭Wi-Fi-删除以下载差分包-打开Wi-Fi-检查状态按钮
    change_network(device, 0)
    delete_fotapac(device)
    device.keyevent(4)
    change_network(device, 2)
    for i in range(1, 5):  # point download button
        j = i
        while(True):
            try:
                download_button  = device.find_element_by_id("com.tcl.ota:id/firmware_update")
                button_text = download_button.get_attribute("text")
            except NoSuchElementException, e:
                time.sleep(5)
            else:
                if button_text == u"CHECK FOR UPDATES NOW":    #状态是未check差分包时点击搜索按钮
                    download_button.click()  # point search button
                    break
                elif button_text == u"PAUSE":           #状态已经在下载时说明设置是自动下载直接pass
                    j = j + 1
                    return device.find_element_by_id("com.tcl.ota:id/firmware_update")
                    break
                else:
                    if network != 2:                    #状态是已check到差分包未下载时，选择网络模式后点击下载
                        change_network(device, network)
                    j = j + 1
                    time.sleep(5)
                    if(buttontype == 0):        #point download button
                        return device.find_element_by_id("com.tcl.ota:id/firmware_update")
                    if(buttontype == 1):        #point download image icon
                        return device.find_element_by_id("com.tcl.ota:id/firmware_state_bottomright")
                    if(buttontype == 2):        #point download in notification bar
                        device.open_notifications()
                        try:
                            device.find_elements_by_android_uiautomator(
                                'new UiSelector().text("System update available")')
                        except NoSuchElementException, e:
                            print "there are no notification "
                            return False
                        else:
                            return device.find_element_by_accessibility_id("Download")
                    break



        if j > i:
            break
        if i >= 4:
            raise CantSearchedFotaPackage

def fill_ram(device):  #fill ram
    device.install_app("C:\\Users\\77465\\eclipse-workspace\\appiumdemo\\apps\\fill.apk")
    if not device.is_app_installed("com.tcl.fill"):
        print "can not install fill.apk"

    allapp_find_app(device,"fill")
    #do fill

    recent_find_app(device, "Updates")

def change_network(device,network_type):
    if network_type == 1:
        device.set_network_connection(network_type)
    else:
        device.set_network_connection(network_type)
        device.open_notifications()
        time.sleep(2)
        swape_bygiven(device, "dragdown")
        try:
            device.find_element_by_accessibility_id("Mobile No phone. No data. No service.")
        except NoSuchElementException,e:
            pass
        else:
            raise HavntInsertSim()

        try:
            device.find_element_by_accessibility_id("Mobile No signal. No data. No SIM cards.")
        except NoSuchElementException,e:
            pass
        else:
            raise HavntInsertSim()
        print "now try to check the 4g icon"

        try:
            data_icon = device.find_element_by_accessibility_id("Mobile Phone four bars.. 4G. CHN-UNICOM.")

        except NoSuchElementException, e:
            if network_type == 4:
                try:
                    data_icon1 = device.find_element_by_accessibility_id("Mobile Phone four bars.. No data. CHN-UNICOM.")
                except NoSuchElementException, e:
                    print "Please insert UNICOM 4G SIM Card"
                else:
                    click_dataicon(device, data_icon1, "Off")


        else:
            if network_type == 4:
                pass
            else:
                click_dataicon(device, data_icon, "On")
        finally:
            time.sleep(1)
            device.keyevent(4)
            time.sleep(1)
            device.keyevent(4)

def click_dataicon(device,data_icon,state):
    data_icon.click()
    data_switch = device.find_element_by_id("android:id/toggle")
    if (data_switch.get_attribute("text") == unicode(state, "utf-8")):

        data_switch.click()
    else:
        print data_switch.get_attribute("text")
        print state
        print unicode(state, "utf-8")
    time.sleep(1)
    device.keyevent(4)


def change_time_forfota(device):
    device.open_notifications()
    time.sleep(2)
    swape_bygiven(device, "dragdown")  # enter setting and change the system time.
    time.sleep(2)
    print "now drag down the noti"
    device.find_element_by_accessibility_id("Settings").click()
    swape_findelm(device, "allappdown", 'new UiSelector().text("Date & time")',
                         MobileBy.ANDROID_UIAUTOMATOR).click()

    hourtype = device.find_elements_by_class_name("android.widget.Switch")
    if (hourtype[1].get_attribute("text") == "Off"):
        hourtype[1].click()
    device.find_element_by_android_uiautomator('new UiSelector().text("Automatic date & time")').click()
    device.find_element_by_android_uiautomator('new UiSelector().text("Off")').click()
    device.find_element_by_android_uiautomator('new UiSelector().text("Set time")').click()
    now_hour = device.find_element_by_id("android:id/hours")
    now_hour_in = int(now_hour.get_attribute("text"))
    # now_minute = self.wd.find_element_by_id("android:id/minutes")

    if (now_hour_in + 1 > 23):
        device.keyevent(4)
        device.find_element_by_android_uiautomator('new UiSelector().text("Set date")').click()
        now_day = device.find_element_by_id("android:id/date_picker_header_date").get_attribute("text").split(" ")[
            2]
        try:
            next_dat_in = int(now_day) + 1
            next_day = 'new UiSelector().text("' + str(next_dat_in) + '")'
            next_day_elm = device.find_element_by_android_uiautomator(next_day)
        except NoSuchElementException, e:
            device.swape_bygiven(device, "right2left")
            device.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
        else:
            next_day_elm.click()
        finally:
            device.find_element_by_id("android:id/button1").click()

    else:
        now_hour_in = now_hour_in + 1
        device.find_element_by_accessibility_id(str(now_hour_in)).click()
        device.find_element_by_id("android:id/button1").click()

def get_bettery(device):
    device.open_notifications()
    time.sleep(2)
    swape_bygiven(device, "dragdown")
    time.sleep(2)
    bettery_icon = device.find_element_by_id("com.android.systemui:id/battery")
    bettery_value = int(bettery_icon.get_attribute("name").split(" ")[1])
    device.keyevent(4)
    device.keyevent(4)
    return bettery_value

class CantFindAppException(Exception):
    def __init__(self, err='Can not open update or update is not in app list'):
        Exception.__init__(self, err)

class CantSearchedFotaPackage(Exception):
    def __init__(self, err='Can not searched FOTA package,please check the network and GOTU setting'):
        Exception.__init__(self, err)

class HavntInsertSim(Exception):
    def __init__(self, err="Haven't insert sim card"):
        Exception.__init__(self, err)

