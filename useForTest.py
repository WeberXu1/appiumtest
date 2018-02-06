#coding=utf-8
import unittest
#import selenium.common.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import common
import os
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
        cmd = "adb logcat > C:\\Users\\77465\\Desktop\\1122.txt"
        cmd1 = "adb reboot"
        os.popen(cmd1)
        while True:
            time.sleep(10)
            try:
                self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', common.capabilities_set(1))
            except WebDriverException,e:
                pass
            else:
                print "reconnnect to appium secc"
                break

        self.wd.open_notifications()


    def tearDown(self):
        self.wd.quit()

    def click_state_button(self, device, state, type):  # 在type页面点击state按钮
        if type == 0:  # 在update主界面点击state键
            state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")
            print "state 0"
        else:  # 在notification bar上点击state键
            device.open_notifications()
            print "state 1"
            '''
            updates_int = "PAUSE" 
            updates_noti = "Pause"
            updates_int = "RESUME"
            updates_noti = "RESUME"

            '''
            if (state == "PAUSE"):
                state = state.capitalize()
            time.sleep(2)
            print ""
            state_button = device.find_element_by_accessibility_id(state)

        if state_button.get_attribute("text") == state:  # point Pause button in fota interface/notificationbar
            state_button.click()
        else:
            print " point button failed" + state

    def check_fotastate(self,device, state):
        device.launch_app()
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


