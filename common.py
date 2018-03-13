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

class UpdateWebDriver(webdriver.Remote):
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 capabilities_type=1, browser_profile=None, proxy=None, keep_alive=False):
        webdriver.Remote.__init__(self,command_executor ,self.capabilities_set(capabilities_type) ,browser_profile ,proxy ,keep_alive)

        By.ANDROID_UIAUTOMATOR = MobileBy.ANDROID_UIAUTOMATOR
        fota_cu = "8090-V1FOTA0"
        fota_fv = "8EA2ZZ20"
        fota_imei = "358511032234522"

    def capabilities_set(self,device_num):
        self.capabilities = {}
        if device_num == 1:
            self.capabilities['platformVersion'] = '6.0'
        if device_num == 2:
            self.capabilities['platformVersion'] = '7.0'
            self.capabilities['automationName'] = 'UIAutomator2'

        self.capabilities['unicodeKeyboard'] = 'True'
        self.capabilities['platformName'] = 'Android'
        self.capabilities['deviceName'] = 'Android Emulator'
        self.capabilities['noSign'] = 'True'
        self.capabilities['resetKeyboard'] = 'True'
        self.capabilities['appPackage'] = 'com.tcl.ota'
        self.capabilities['appActivity'] = 'com.tcl.ota.SystemUpdatesActivity'
        self.capabilities['app'] = 'C:\\Users\\77465\\eclipse-workspace\\appiumdemo\\apps\\Fota_GL_v7.0.10.3.0655.0_signed_platformkey_alldpi.apk'
        self.capabilities['noReset'] = 'True'

        return self.capabilities

    def allapp_find_app(self,appname):
        self.press_keycode(3)
        time.sleep(2)
        el1 = self.find_element_by_accessibility_id("ALL APPS")
        el1.click()
        time.sleep(2)
        return self.swape_findelm("allappdown", appname)

    def recent_find_app(self,appname):
        self.press_keycode(1)
        time.sleep(1)
        return self.swape_findelm("recentup", appname)

    def swape_bygiven(self,distance):
        x = self.get_window_size()['width']
        y = self.get_window_size()['height']
        if distance == "dragdown":
            self.swipe(x / 2 , y / 20,x / 2,y / 2,1000)
        if distance == "left2right":
            self.swipe(x / 20,y / 2,x * 19 / 20,y / 2,1000)
        if distance == "allappdown":
            self.swipe(x / 2, y * 3 / 4, x / 2, y / 4, 1000)
        if distance == "recentup":
            self.swipe(x / 2, y / 4, x / 2, y * 3 / 4, 1000)
        if distance == "right2left":
            self.swipe(x * 5 / 6, y / 2, x / 6, y / 2, 1000)
        if distance == "aotacheck":
            self.swipe(x / 2, y / 4, x / 2, y * 3 / 4, 1000)

    def swape_app2homescreen(self,appname):
        try:
            updateelm1 = self.allapp_find_app(appname)
        except CantFindAppException, e:
            print e
        else:
            x = self.get_window_size()['width'] / 2
            y = self.get_window_size()['height'] / 2

            TouchAction(self).long_press(updateelm1).move_to(x=x, y=y).release().perform()

    def swape_findelm(self,distance,value="Updates",by=By.ACCESSIBILITY_ID):
        while True:
            str1 = self.page_source
            try:
                appelm = self.find_element(by,value)
            except NoSuchElementException:
                self.swape_bygiven(distance)
            else:
                return appelm

            str2 = self.page_source
            if (str1 == str2):
                raise CantFindAppException()

    def open_appinhomescreen(self,appname):
        self.press_keycode(3)
        try:
            self.find_element_by_accessibility_id(appname).click()
        except NoSuchElementException,e:
            print e
            return False
        else:
            return True

    def read_logs(self, log_type, ignore=False):
        raw_logs = self.get_log(log_type)
        if ignore: return []

        logs = []
        for raw_log in raw_logs:
            timestamp_sec = raw_log['timestamp'] / 1000
            time_str = datetime.fromtimestamp(timestamp_sec).strftime('%Y-%m-%d %H:%M:%S')
            log = '%s %s' % (time_str, raw_log['message'])
            logs.append(log)

        return logs

    def write_logs(self, logs , to_file):
        with open(to_file, 'wb') as f:
            lines = [log.encode('utf-8') + '\n' for log in logs]
            f.writelines(lines)
        return logs

    def enable_fota_advance(self,type):
        if type == "FOTA":
            self.cu = "8090-V1FOTA0"
            self.fv = "8EA2ZZ20"
            self.imei = "358511032234522"

        if type == "AOTA":
            self.cu = "AOTATEST6"
            self.fv = "8EA2ZZ20"
            self.imei = "358511032234522"

        self.launch_app()
        self.find_element_by_accessibility_id("More options").click()
        self.find_element_by_android_uiautomator('new UiSelector().text("Help")').click()
        cfu_elm = self.find_element_by_android_uiautomator('new UiSelector().text("Checking for updates")')
        for i in range(1,10):
            try:
                pwdinput = self.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")')
            except NoSuchElementException, e:
                cfu_elm.click()
                time.sleep(1)
            else:
                pwdinput.send_keys("20180201")
                break
        try:
            self.find_element_by_id("android:id/button1").click()
        except NoSuchElementException, e:
            print "advance mode already enabled"
        else:
            pass
        self.press_keycode(4)
        try:
            self.find_element_by_android_uiautomator('new UiSelector().text("Password incorrect")')
        except NoSuchElementException,e:
            print "open fota advance mode success"
            self.find_element_by_accessibility_id("More options").click()
            self.find_element_by_android_uiautomator('new UiSelector().text("FOTA test")').click()
            self.find_element_by_id("android:id/switchWidget").click()
            self.find_element_by_android_uiautomator('new UiSelector().text("Emulated CU Reference")').click()
            self.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")').send_keys(self.cu)
            self.find_element_by_id("android:id/button1").click()
            self.find_element_by_android_uiautomator('new UiSelector().text("Emulated current version")').click()
            self.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")').send_keys(self.fv)
            self.find_element_by_id("android:id/button1").click()
            self.find_element_by_android_uiautomator('new UiSelector().text("Emulated IMEI")').click()
            self.find_element_by_android_uiautomator('new UiSelector().className("android.widget.EditText")').send_keys(self.imei)
            self.find_element_by_id("android:id/button1").click()
            self.find_element_by_android_uiautomator('new UiSelector().text("Start Test")').click()
            print self.current_activity
            time.sleep(3)
            return True


        else:
            print "failed to open fota advance mode"
            return False



    def delete_fotapac(self):
        self.press_keycode(3)
        self.launch_app()
        self.find_element_by_accessibility_id("More options").click()
        self.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
        try:
            print "try to find package in setting"
            delete_icon = self.find_element_by_id("com.tcl.ota:id/pref_button")
        except NoSuchElementException,e:
            print " no package"
            pass
        else:
            delete_icon.click()
            time.sleep(2)
            self.find_element_by_android_uiautomator('new UiSelector().text("Delete")').click()

    def click_checkfota(self,buttontype,network):   #关闭Wi-Fi-删除以下载差分包-打开Wi-Fi-检查状态按钮
        self.change_network(0)
        self.delete_fotapac()
        self.press_keycode(4)
        self.change_network(2)
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

    def fill_ram(self):  #fill ram
        self.install_app("C:\\Users\\77465\\eclipse-workspace\\appiumdemo\\apps\\fill.apk")
        if not self.is_app_installed("com.tcl.fill"):
            print "can not install fill.apk"

        self.allapp_find_app("fill")
        #do fill

        self.recent_find_app("Updates")

    def change_network(self,network_type):
        if self.capabilities['platformVersion'] == '6.0':
            if network_type == 1 or network_type == 2 or network_type == 6:
                self.set_network_connection(network_type)
            else:
                self.set_network_connection(network_type)
                self.open_notifications()
                time.sleep(2)
                self.swape_bygiven("dragdown")
                try:
                    self.find_element_by_accessibility_id("Mobile No phone. No data. No service.")
                except NoSuchElementException,e:
                    pass
                else:
                    raise HavntInsertSim()

                try:
                    self.find_element_by_accessibility_id("Mobile No signal. No data. No SIM cards.")
                except NoSuchElementException,e:
                    pass
                else:
                    raise HavntInsertSim()
                print "now try to check the 4g icon"

                try:
                    data_icon = self.find_element_by_accessibility_id("Mobile Phone four bars.. 4G. CHN-UNICOM.")

                except NoSuchElementException, e:
                    if network_type == 4:
                        try:
                            data_icon1 = self.find_element_by_accessibility_id("Mobile Phone four bars.. No data. CHN-UNICOM.")
                        except NoSuchElementException, e:
                            print "Please insert UNICOM 4G SIM Card"
                        else:
                            self.click_dataicon(data_icon1, "Off")


                else:
                    if network_type == 4:
                        pass
                    else:
                        self.click_dataicon(data_icon, "On")
                finally:
                    self.tap_mutiback(2)
        elif self.capabilities['platformVersion'] == '7.0':
            self.open_notifications()
            time.sleep(2)
            self.swape_bygiven("dragdown")
            time.sleep(2)
            if network_type == 2 or network_type == 6:
                try:
                    wifi_button = self.find_element_by_accessibility_id("Wi-Fi Off,Open Wi-Fi settings.")
                except NoSuchElementException,e:
                    self.press_keycode(4)
                else:
                    wifi_button.click()
                    self.tap_mutiback(3)
                finally:
                    time.sleep(3)
                    #here need click the open button
            elif network_type == 4 :
                try:
                    self.find_element_by_accessibility_id("Wi-Fi Off,Open Wi-Fi settings.")
                except NoSuchElementException, e:
                    self.find_element_by_android_uiautomator('new UiSelector().descriptionStartsWith("Wi-Fi")').click()
                    self.find_element_by_id("android:id/toggle").click()
                else:
                    pass
                time.sleep(2)
                try:
                    self.find_element_by_accessibility_id("No SIM card,Open Cellular data settings.")
                except NoSuchElementException,e:
                    data_button = self.find_element_by_android_uiautomator('new UiSelector().descriptionStartsWith("Mobile Mobile Data On")')
                    data_button.click()
                    data_state = self.find_element_by_id("com.android.systemui:id/sim_toggle")
                    if data_state.get_attribute("text") == "OFF":
                        data_state.click()
                        self.press_keycode(4)
                    else:
                        self.press_keycode(4)
                    self.tap_mutiback(2)

                else:
                    raise HavntInsertSim
            elif network_type == 0 :
                try:
                    self.find_element_by_accessibility_id("No SIM card,Open Cellular data settings.")
                except NoSuchElementException,e:
                    data_button = self.find_element_by_accessibility_id("Mobile Mobile Data On. Phone four bars.. China Unicom.,Open Cellular data settings.")
                    data_button.click()
                    time.sleep(1)
                    data_state = self.find_element_by_id("com.android.systemui:id/sim_toggle")
                    if data_state.get_attribute("text") == "On":
                        data_state.click()
                        self.press_keycode(4)
                    else:
                        self.press_keycode(4)
                    self.tap_mutiback(2)
                else:
                    self.tap_mutiback(2)
            else:
                print "ERROR:WRONG NETWORK TYPE"
            network_chag_ifo =  "change network to " + str(network_type) + " successfully!"
            print network_chag_ifo
        else:
            print "ERROR: Now we don't support this android version network change "

    def click_dataicon(self,data_icon,state):
        data_icon.click()
        data_switch = self.find_element_by_id("android:id/toggle")
        if (data_switch.get_attribute("text") == unicode(state, "utf-8")):

            data_switch.click()
        else:
            print data_switch.get_attribute("text")
            print state
            print unicode(state, "utf-8")
        time.sleep(1)
        self.press_keycode(4)


    def change_time_forfota(self):
        self.open_notifications()
        time.sleep(2)
        self.swape_bygiven("dragdown")  # enter setting and change the system time.
        time.sleep(2)
        print "now drag down the noti"
        self.find_element_by_accessibility_id("Settings").click()
        self.swape_findelm("allappdown", 'new UiSelector().text("Date & time")',
                             MobileBy.ANDROID_UIAUTOMATOR).click()

        hourtype = self.find_elements_by_class_name("android.widget.Switch")
        if (hourtype[1].get_attribute("text") == "Off"):
            hourtype[1].click()
        self.find_element_by_android_uiautomator('new UiSelector().text("Automatic date & time")').click()
        self.find_element_by_android_uiautomator('new UiSelector().text("Off")').click()
        self.find_element_by_android_uiautomator('new UiSelector().text("Set time")').click()
        now_hour = self.find_element_by_id("android:id/hours")
        now_hour_in = int(now_hour.get_attribute("text"))
        # now_minute = self.wd.find_element_by_id("android:id/minutes")

        if (now_hour_in + 1 > 23):
            self.press_keycode(4)
            self.find_element_by_android_uiautomator('new UiSelector().text("Set date")').click()
            now_day = self.find_element_by_id("android:id/date_picker_header_date").get_attribute("text").split(" ")[
                2]
            try:
                next_dat_in = int(now_day) + 1
                next_day = 'new UiSelector().text("' + str(next_dat_in) + '")'
                next_day_elm = self.find_element_by_android_uiautomator(next_day)
            except NoSuchElementException, e:
                self.swape_bygiven( "right2left")
                self.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
            else:
                next_day_elm.click()
            finally:
                self.find_element_by_id("android:id/button1").click()

        else:
            now_hour_in = now_hour_in + 1
            self.find_element_by_accessibility_id(str(now_hour_in)).click()
            self.find_element_by_id("android:id/button1").click()

    def get_bettery(self):
        self.open_notifications()
        time.sleep(2)
        self.swape_bygiven("dragdown")
        time.sleep(2)
        bettery_icon = self.find_element_by_id("com.android.systemui:id/battery")
        bettery_value = int(bettery_icon.get_attribute("name").split(" ")[1])
        self.tap_mutiback(2)
        return bettery_value

    def tap_mutiback(self,times,internal=1):
        for i in range(0,times):
            time.sleep(internal)
            self.press_keycode(4)

    def try_findeletimes(self, value, by=By.ACCESSIBILITY_ID, times=5, internal=3):
        for i in range(0,times):
            time.sleep(internal)
            applist = self.find_elements(by,value)
            if len(applist) != 0:
                print "ele name find successfully"
                return applist
            if i == (times - 1):
                return []


class CantFindAppException(Exception):
    def __init__(self, err='Can not open update or update is not in app list'):
        Exception.__init__(self, err)

class CantSearchedFotaPackage(Exception):
    def __init__(self, err='Can not searched FOTA package,please check the network and GOTU setting'):
        Exception.__init__(self, err)

class HavntInsertSim(Exception):
    def __init__(self, err="Haven't insert sim card"):
        Exception.__init__(self, err)

