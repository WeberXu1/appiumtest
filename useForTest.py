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
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set())
        common.read_logs(self.wd, 'logcat', ignore=True)
       # self.wd.implicitly_wait(60)

    def test_putupdatetoscreen(self):
        download_button = common.click_checkfota(self.wd, 0, 0)
        print "%r" %download_button
        download_button.click()
        time.sleep(3)

        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message").get_attribute("text"),
                         u"No internet connection")
        self.assertEqual(
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra").get_attribute("text")[0:23],
            u"Couldn't start download")
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"),
                         u"TRY AGAIN")











    def tearDown(self):

        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


