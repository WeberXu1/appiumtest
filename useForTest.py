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

        self.wd.open_notifications()
        time.sleep(2)
        common.swape_bygiven(self.wd, "dragdown")  # enter setting and change the system time.
        time.sleep(2)
        print "now drag down the noti"
        self.wd.find_element_by_accessibility_id("Settings").click()
        common.swape_findelm(self.wd, "allappdown", 'new UiSelector().text("Date & time")',
                             MobileBy.ANDROID_UIAUTOMATOR).click()

        hourtype = self.wd.find_elements_by_class_name("android.widget.Switch")
        if (hourtype[1].get_attribute("text") == "Off"):
            hourtype[1].click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Automatic date & time")').click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Off")').click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Set time")').click()
        now_hour = self.wd.find_element_by_id("android:id/hours")
        now_hour_in = int(now_hour.get_attribute("text"))
        # now_minute = self.wd.find_element_by_id("android:id/minutes")

        if (now_hour_in + 1 > 23):
            self.wd.keyevent(4)
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("Set date")').click()
            now_day = self.wd.find_element_by_id("android:id/date_picker_header_date").get_attribute("text").split(" ")[
                2]
            try:
                next_dat_in = int(now_day) + 1
                next_day = 'new UiSelector().text("' + str(next_dat_in) + '")'
                next_day_elm = self.wd.find_element_by_android_uiautomator(next_day)
            except NoSuchElementException, e:
                common.swape_bygiven(self.wd, "right2left")
                self.wd.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
            else:
                next_day_elm.click()
            finally:
                self.wd.find_element_by_id("android:id/button1").click()

        else:
            now_hour_in = now_hour_in + 1
            self.wd.find_element_by_accessibility_id(str(now_hour_in)).click()
            self.wd.find_element_by_id("android:id/button1").click()

    def tearDown(self):

        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


