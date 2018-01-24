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


        print "now you have 20 seconds to check a package"

        self.wd.open_notifications()

        # point "Download" in different ways
        time.sleep(2)
        self.wd.find_element_by_accessibility_id("Download").click()  # point download in notification bar
        self.wd.launch_app()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"), "PAUSE")
        download_button = common.click_checkfota(self.wd, 0, 2)  # point download button
        download_button.click()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"), "PAUSE")
        download_icon = common.click_checkfota(self.wd, 1, 2)  # point download image icon
        download_icon.click()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"), "PAUSE")

        download_button = common.click_checkfota(self.wd, 0, 0)  # point download button when no network
        download_button.click()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message").get_attribute("text"),
                         u"No internet connection")
        self.assertEqual(
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra").get_attribute("text")[0:23],
            u"Couldn't start download")
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"),
                         u"TRY AGAIN")

        common.click_checkfota(self.wd, 0, 4)  # point download when only data nerwork
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message").get_attribute("text"),
                         u"System update available")
        self.assertEqual(
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra").get_attribute("text"),
            u'01008\x08(51.1 MB)')
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"),
                         u"DOWNLOAD UPDATE")
        # common.fill_ram()     #now will not add the fill ram function
        # common.click_checkfota(self.wd, 0, 2)












    def tearDown(self):

        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


