#coding=utf-8
import unittest
#import selenium.self.wd.exceptions
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
import xlrd
import xlwt
import xdrlib,sys

class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = common.UpdateWebDriver('http://127.0.0.1:4723/wd/hub')
        self.wd.read_logs('logcat', ignore=True)

    def test_putupdatetoscreen(self):
        time.sleep(10)
        self.wd.press_keycode(3)
        self.wd.press_keycode()###1.0


        #self.wd.set_network_connection(2)  # 2.0
        #print "net2"


        #print self.get_wifi_state()
        '''c11  = self.wd.network_connection
        print c11
        time.sleep(5)
        #self.wd.set_network_connection(4)  # 2.0
        print "net4"
        print self.wd.network_connection
        time.sleep(5)
        #self.wd.set_network_connection(6)  # 2.0
        print "net6"
        print self.wd.network_connection
        '''



    def tearDown(self):
        self.wd.quit()

    def get_wifi_state(self):
        """
        获取WiFi连接状态
        :return:
        """
        return 'enabled' in self.wd.shell('dumpsys wifi | %s ^Wi-Fi' % self.__find).read().strip()
if __name__ == '__main__':
    unittest.main()