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

    def test_putupdatetoscreen(self):
        time.sleep(10)
        #self.wd.keyevent()         ###1.0
        self.wd.press_keycode(3)
        self.wd.set_network_connection(0)#2.0
        print "net0"
        print self.wd.network_connection()
        time.sleep(5)
        self.wd.set_network_connection(2)  # 2.0
        print "net2"
        print self.wd.network_connection()
        time.sleep(5)
        self.wd.set_network_connection(4)  # 2.0
        print "net4"
        print self.wd.network_connection()
        time.sleep(5)
        self.wd.set_network_connection(6)  # 2.0
        print "net6"
        print self.wd.network_connection()
        self.wd.network_connection


    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()