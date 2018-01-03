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
        self.wd.set_network_connection(0)
        #need to clear the app's data.
        common.enable_fota_advance(self.wd, "FOTA")
        self.wd.find_element_by_accessibility_id("More options").click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
        elm1 = self.wd.find_element_by_class_name("android.widget.Switch")
        if elm1[0].text().equal("On"):
            elm1.click()
        self.wd.keyevent(4)
        time.sleep(2)
        self.wd.set_network_connection(2)
        for i in range(1,6):
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_bottomright").click()
            time.sleep(5)
            try:
                elm2 = self.wd.find_element_by_id("com.tcl.ota:id/firmware_update")
            except NoSuchElementException,e:
                pass
            else:
                svn_value = self.wd.find_element_by_id(com.tcl.ota:id/firmware_system_version).text()
                self.assertEqual(svn_value,"6.0-01001")
                package_size = self.wd.find_element_by_id("com.tcl.ota:id / firmware_state_message_extra").text()
                self.assertEqual(package_size,"20171219_135255?(76.5 MB)")
                state_message = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message")
                self.assertEqual(state_message,"System update available")
                self.wd.find_element_by_id("com.tcl.ota:id/firmware_info").click()
                detail_title = self.wd.find_element_by_id("com.tcl.ota:id/firmware_detail_title_shadow")
                self.assertEqual(detail_title,"New in this version")
                detail_content = self.wd.find_element_by_id("com.tcl.ota:id/firmware_detail_content")
                self.assertEqual(detail_content,"UPDATE TO A8")
                self.wd.keyevent(4)
            if i > 4:
                raise common.CantSearchedFotaPackage








    def tearDown(self):

        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


