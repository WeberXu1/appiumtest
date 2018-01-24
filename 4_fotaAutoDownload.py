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
        downloadsize = download_statetext1[1].split(" ")
        download_percent = float(downloadsize[2]) / 51.1

        self.wd.open_notifications()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Downloading system update").fromParent(new UiSelector().resourceId("android:id/line3")).childSelector(new UiSelector().resourceId("android:id/text"))')




















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