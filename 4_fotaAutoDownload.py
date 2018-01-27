#coding=utf-8
import unittest
#import selenium.common.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
import time
import common
import subprocess
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction

class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set(1))
        common.read_logs(self.wd, 'logcat', ignore=True)
       # self.wd.implicitly_wait(60)

    def test_fotaautodownload(self):
        self.wd.reset()
        download_button = common.click_checkfota(self.wd, 0, 2)
        download_button.click()  #fota interface point "download" button
        self.check_fotastate(self.wd,"PAUSE")
        self.click_state_button(self.wd, "PAUSE",0)

        time.sleep(2)
        self.check_fotastate(self.wd, "RESUME")
        self.click_state_button(self.wd, "RESUME",0)

        time.sleep(2)
        self.check_fotastate(self.wd, "PAUSE")
        self.click_state_button(self.wd, "PAUSE", 1)

        time.sleep(2)
        self.check_fotastate(self.wd, "RESUME")
        self.click_state_button(self.wd, "RESUME", 1)

        time.sleep(2)
        self.check_fotastate(self.wd, "PAUSE")

        common.change_network(self.wd,4)
        self.check_fotastate(self.wd, "RESUME")
        download_state = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra")
        download_statetext = download_state.get_attribute("text")
        download_statetext1 = download_statetext.split(',')
        self.assertEqual(download_statetext1[0],"Waiting for Wi-Fi")

        common.change_network(self.wd, 6)
        time.sleep(10)
        self.check_fotastate(self.wd, "PAUSE")
        download_state = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra")
        downloadsize = download_state.get_attribute("text").split('/')
        download_percent = float(downloadsize[0]) * 100 / 51.1
        self.wd.open_notifications()
        # self.wd.find_element_by_android_uiautomator('new UiSelector().text("Downloading system update").fromParent(new UiSelector().resourceId("android:id/line3")).childSelector(new UiSelector().resourceId("android:id/text"))')
        noti_downloadp = self.wd.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/'
                                                       'android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/'
                                                       'android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/'
                                                       'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/'
                                                       'android.widget.TextView')
        noti_downloadpc = noti_downloadp.get_attribute("text").split("%")[0]
        if abs(float(noti_downloadpc) - download_percent) > 10:
            print "download percent sync failed "
        self.wd.keyevent(4)

        while(True):
            time.sleep(5)
            try:
                fota_state = self.wd.find_element_by_id("com.tcl.ota:id/firmware_update")
            except NoSuchElementException,e:
                print "download error,maybe updates Fc"
            else:
                fota_state_att = fota_state.get_attribute("text")
                if fota_state_att == "Installing":      #download successfully
                    break
                if fota_state_att == "RESUME":      #Network disconnected
                    if (self.wd.network_connection() != 2):
                        print "download error"
                    else:
                        common.change_network(self.wd, 6)
                        fota_state.click()
                else:
                    print "download failed"
                    break



        common.swape_bygiven(self.wd, "dragdown")  #enter setting and change the system time.
        self.wd.find_element_by_accessibility_id("Settings").click()
        common.swape_findelm(self.wd, "allappdown", 'new UiSelector().text("Date & time")',
                                 MobileBy.ANDROID_UIAUTOMATOR).click()

        hourtype = self.wd.find_elements_by_class_name("android.widget.Switch")
        if (hourtype[1].get_attribute("text") == "Off"):
            hourtype[1].click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Automatic date & time")').click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Off")').click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Set time")').click()
        now_hour = self.wd.find_element_by_id("android:id/hours")
        #now_minute = self.wd.find_element_by_id("android:id/minutes")

        if (int(now_hour)+1 > 23):
            self.wd.keyevent(4)
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("Set data")').click()
            now_day = self.wd.find_element_by_id("android:id/date_picker_header_date").get_attribute("text").split(" ")[1]
            try:
                next_day = 'new UiSelector().text("' + (now_day + 1) + '")'
                next_day_elm = self.wd.find_element_by_android_uiautomator(next_day)
            except NoSuchElementException,e:
                common.swape_bygiven(self.wd, "left2right")
                self.wd.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
            else:
                next_day_elm.click()
                self.wd.find_element_by_id("android:id/button1")

        else:
            self.wd.find_element_by_accessibility_id("15").click()
            self.wd.find_element_by_id("android:id/button1")





































    def tearDown(self):

        self.wd.quit()

    def check_fotastate(self,device, state):
        state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")
        self.assertEqual(state_button.get_attribute("text"), state)

        device.open_notifications()
        try:
            noti_button = device.find_element_by_id("android:id/action0")
        except NoSuchElementException, e:
            print "downloading page missing" + state
        else:
            self.assertEqual(noti_button.get_attribute("text"), "PAUSE")
        finally:
            device.keyevent(4)

    def click_state_button(self,device,state,type):
        if type == 0:
            state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")

        else:
            device.open_notifications()
            time.sleep(1)
            state_button = device.find_element_by_id("android:id/action0")

        if state_button.get_attribute("text") == state:  # point Pause button in fota interface
            state_button.click()
        else:
            print " point button failed" + state

        if type == 1:
            device.keyevent(4)

if __name__ == '__main__':
    unittest.main()