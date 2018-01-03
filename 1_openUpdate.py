import unittest
#import selenium.common.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
import time
import common
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.common.by import By


class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set())
        common.read_logs(self.wd, 'logcat', ignore=True)
       # self.wd.implicitly_wait(60)

    def test_accessupdate(self):
        #Open updates in Allapplist
        try:
            updateelm = common.allapp_find_app(self.wd,"Updates")
        except common.CantFindAppException,e:
            print e
        else:
            updateelm.click()

        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s1_logs = common.write_logs(common.read_logs(self.wd, 'logcat'), 'D:/test/logs/openupdates_1.log')
        #Open Updates in Homescreen
        self.wd.keyevent(3)
        try:
            updateelm2 = self.wd.find_element_by_accessibility_id("Updates")
        except NoSuchElementException:
            common.swape_app2homescreen(self.wd, "Updates")
            try:
                self.wd.find_element_by_accessibility_id("ALL APPS")
            except NoSuchElementException:
                self.wd.keyevent(3)
                deleapp = self.wd.find_elements_by_class_name("android.widget.TextView")
                TouchAction(self.wd).long_press(el=deleapp[0], duration=2000).perform()
                deleicon = self.wd.find_elements_by_android_uiautomator('new UiSelector().text("Remove")')
                TouchAction(self.wd).move_to(deleicon[0]).release().perform()
                common.swape_app2homescreen(self.wd, "Updates")
                openupdate = common.open_appinhomescreen(self.wd, "Updates")
            else:
                openupdate = common.open_appinhomescreen(self.wd, "Updates")

        else:
            openupdate = common.open_appinhomescreen(self.wd, "Updates")

        if not (openupdate):
            print "process mistake,can not open app in homescreen"
        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s2_logs = common.write_logs(common.read_logs(self.wd, 'logcat'), 'D:/test/logs/openupdates_2.log')

        #Open updates in recent page
        self.wd.keyevent(3)
        time.sleep(1)
        self.wd.keyevent(82)
        common.recent_find_app(self.wd, "Updates").click()
        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s3_logs = common.write_logs(common.read_logs(self.wd, 'logcat'), 'D:/test/logs/openupdates_3.log')

        #Open updates in setting.
        self.wd.keyevent(3)
        self.wd.open_notifications()
        time.sleep(2)
        common.swape_bygiven(self.wd, "dragdown")
        self.wd.find_element_by_accessibility_id("Settings").click()
        try:
            common.swape_findelm(self.wd, "allappdown", 'new UiSelector().text("About phone")',MobileBy.ANDROID_UIAUTOMATOR).click()
        except:
            pass
        else:
            print"open about phone success"
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Updates")').click()
        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s4_logs = common.write_logs(common.read_logs(self.wd, 'logcat'), 'D:/test/logs/openupdates_4.log')
        common.write_logs(s1_logs + s2_logs + s3_logs + s4_logs ,'D:/test/logs/openupdates_total.log' )
    cc
