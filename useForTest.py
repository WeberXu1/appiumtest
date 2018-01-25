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
        time.sleep(20)
        self.wd.open_notifications()
        time.sleep(2)
        #self.wd.find_element_by_android_uiautomator(
        #    'new UiSelector().text("Downloading system update").getparent().getFromParent(new UiSelector().resourceId("android:id/line3")).getChild(new UiSelector().resourceId("android:id/text"))')
        p = self.wd.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/'
            'android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/'
            'android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/'
            'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/'
            'android.widget.TextView')
        print "%r" %p
        print p.get_attribute("text")
        print p.get_attribute("text").split("%")[0]









    def tearDown(self):

        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


