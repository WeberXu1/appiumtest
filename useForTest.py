#coding=utf-8
import unittest
#import selenium.common.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import common
import os
from datetime import datetime
import subprocess
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction

class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set(2))
        common.read_logs(self.wd, 'logcat', ignore=True)
        print "begin logtime" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
       # self.wd.implicitly_wait(60)

    def test_putupdatetoscreen(self):
        self.wd.find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')[1].click()
        for i in range(1, 10):
            common.swape_bygiven(self.wd, "aotacheck")
            try:
                self.wd.find_element_by_id("com.tcl.ota:id/update_available")
            except NoSuchElementException, e:
                time.sleep(5)
            else:
                print "Check for app update successfully"
                break
            if i > 8:
                print "ERROR:check for app list failed"
        applist = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/name")')
        print applist[0].get_attribute("text")
        print applist[0].get_attribute("instance")
    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


