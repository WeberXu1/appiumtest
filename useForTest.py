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

    def test_putupdatetoscreen(self):
        self.wd.reset()
        # need to clear the app's data.ok
        # common.enable_fota_advance(self.wd, "FOTA")
        self.wd.find_element_by_accessibility_id("More options").click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
        elm1 = self.wd.find_elements_by_class_name("android.widget.Switch")
        str1 = elm1[0].get_attribute("text")
        print "%r" % str1
        if str1 == u'Off':
            elm1[0].click()
        download_button = common.click_checkfota(self.wd, 0, 2)
        if download_button.get_attribute("text") == u"CHECK FOR UPDATES NOW":
            download_button.click()  # fota interface point "download" button
        self.check_fotastate(self.wd, u"PAUSE")
        self.click_state_button(self.wd, "PAUSE", 0)

        time.sleep(2)
        self.check_fotastate(self.wd, u"RESUME")
        self.click_state_button(self.wd, "RESUME", 0)

    def tearDown(self):
        self.wd.quit()

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

    def check_fotastate(self,device, state):
        state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")
        self.assertEqual(state_button.get_attribute("text"), state)

        device.open_notifications()
        time.sleep(2)
        try:
            noti_button = device.find_element_by_id("android:id/action0")
        except NoSuchElementException, e:
            print "downloading page missing" + state
        else:
            if(state == u"PAUSE"):
                state = state.capitalize()
            self.assertEqual(noti_button.get_attribute("text"), state)
        finally:
            device.keyevent(4)
if __name__ == '__main__':
    unittest.main()


