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
def capabilities_set():
    capabilities = {}
    capabilities['platformName'] = 'Android'
    capabilities['deviceName'] = 'Android Emulator'
    capabilities['platformVersion'] = '6.0'
    capabilities['unicodeKeyboard'] = 'True'
    capabilities['resetKeyboard'] = 'True'
    capabilities['appPackage'] = 'com.tcl.ota'
    #capabilities['appActivity'] = 'com.tcl.ota.SystemUpdatesActivity'
    #capabilities['app'] = 'C:\\Users\\77465\\eclipse-workspace\\appiumdemo\\apps\\Fota_Global_v7.0.10.3.0626.0_signed_platformkey_alldpi.apk'
    capabilities['noReset'] = 'True'
    capabilities['noSign'] = 'True'
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
    device.launch_app()
    device.find_element_by_accessibility_id("More options").click()
    device.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
    try:
        delete_icon = device.find_element_by_id("com.tcl.ota:id/pref_button")
    except NoSuchElementException,e:
        return False
    else:
        delete_icon.click()
        time.sleep(2)
        device.find_element_by_android_uiautomator('new UiSelector().text("Delete")').click()
        return True

def click_checkfota(device,buttontype,network):
    device.set_network_connection(0)
    if not delete_fotapac(device):
        return False
    device.keyevent(4)
    device.set_network_connection(2)
    for i in range(1, 5):  # point download button
        try:
            download_dutton = device.find_element_by_id("com.tcl.ota:id / firmware_update")
        except NoSuchElementException, e:
            pass
        else:
            device.set_network_connection(network)
            if(buttontype == 0):        #point download button
                return download_dutton
            if(buttontype == 1):        #point download image icon
                return device.find_element_by_id("com.tcl.ota:id/firmware_state_bottomright")
            if(buttontype == 2):        #point download in notification bar
                self.wd.open_notifications()
                try:
                    device.find_elements_by_android_uiautomator(
                        'new UiSelector().text("System update available")')
                except NoSuchElementException, e:
                    print "there are no notification "
                else:
                    return device.find_elements_by_android_uiautomator(
                        'new UiSelector().package("com.tcl.ota").text("Download")').click()
            break
        device.find_element_by_id("com.tcl.ota:id/firmware_state_bottomright").click()
        time.sleep(10)
        if i >= 4:
            raise CantSearchedFotaPackage

def fill_ram(device):
    device.install_app("C:\\Users\\77465\\eclipse-workspace\\appiumdemo\\apps\\fill.apk")
    if not device.is_app_installed("com.tcl.fill"):
        print "can not install fill.apk"

    allapp_find_app(device,"fill")
    #do fill

    recent_find_app(device, "Updates")






class CantFindAppException(Exception):
    def __init__(self, err='Can not open update or update is not in app list'):
        Exception.__init__(self, err)

class CantSearchedFotaPackage(Exception):
    def __init__(self, err='Can not searched FOTA package,please check the network and GOTU setting'):
        Exception.__init__(self, err)


