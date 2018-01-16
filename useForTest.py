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
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set(2))
        common.read_logs(self.wd, 'logcat', ignore=True)
       # self.wd.implicitly_wait(60)

    def test_putupdatetoscreen(self):
        #network 0
        #print "now set the network as 0"
        #self.wd.set_network_connection(0)
       # time.sleep(1)
        #print self.wd.network_connection
        #network 1
       # print "now set the network as 1"
        #self.wd.set_network_connection(1)
        #time.sleep(1)
        #print self.wd.network_connection
        # network 2
        print "now set the network as 2"
        #self.wd.set_network_connection(2)
        time.sleep(1)
        print self.wd.network_connection
        # network 4
        print "now set the network as 4"
        #self.wd.set_network_connection(4)
        time.sleep(1)
        print self.wd.network_connection
        # network 6
        print "now set the network as 6"
        #self.wd.set_network_connection(6)
        time.sleep(1)
        #print self.wd.network_connection
        #self.wd.set_network_connection(1)












    def tearDown(self):

        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


