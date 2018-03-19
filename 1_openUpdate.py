import unittest
#import selenium.self.wd.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
import time
import common
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.self.wd.by import By


class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = common.UpdateWebDriver('http://127.0.0.1:4723/wd/hub')
        self.wd.read_logs('logcat', ignore=True)
       # self.wd.implicitly_wait(60)

    def test_accessupdate(self):
        #Open updates in Allapplist
        try:
            updateelm = self.wd.allapp_find_app("Updates")
        except common.CantFindAppException as e:
            print(e)
        else:
            updateelm.click()

        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s1_logs = self.wd.write_logs(self.wd.read_logs('logcat'), 'D:/test/logs/openupdates_1.log')
        #Open Updates in Homescreen
        self.wd.press_keycode(3)
        try:
            updateelm2 = self.wd.find_element_by_accessibility_id("Updates")
        except NoSuchElementException:
            self.wd.swape_app2homescreen("Updates")
            try:
                self.wd.find_element_by_accessibility_id("ALL APPS")
            except NoSuchElementException:
                self.wd.press_keycode(3)
                deleapp = self.wd.find_elements_by_class_name("android.widget.TextView")
                TouchAction(self.wd).long_press(el=deleapp[0], duration=2000).perform()
                deleicon = self.wd.find_elements_by_android_uiautomator('new UiSelector().text("Remove")')
                TouchAction(self.wd).move_to(deleicon[0]).release().perform()
                self.wd.swape_app2homescreen("Updates")
                openupdate = self.wd.open_appinhomescreen("Updates")
            else:
                openupdate = self.wd.open_appinhomescreen( "Updates")

        else:
            openupdate = self.wd.open_appinhomescreen("Updates")

        if not (openupdate):
            print("process mistake,can not open app in homescreen")
        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s2_logs = self.wd.write_logs(self.wd.read_logs('logcat'), 'D:/test/logs/openupdates_2.log')

        #Open updates in recent page
        self.wd.press_keycode(3)
        time.sleep(1)
        self.wd.press_keycode(82)
        self.wd.recent_find_app("Updates").click()
        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s3_logs = self.wd.write_logs(self.wd.read_logs('logcat'), 'D:/test/logs/openupdates_3.log')

        #Open updates in setting.
        self.wd.press_keycode(3)
        self.wd.open_notifications()
        time.sleep(2)
        self.wd.swape_bygiven("dragdown")
        time.sleep(2)
        self.wd.find_element_by_accessibility_id("Settings").click()
        try:
            self.wd.swape_findelm("allappdown", 'new UiSelector().text("About phone")',MobileBy.ANDROID_UIAUTOMATOR).click()
        except:
            pass
        else:
            print("open about phone success")
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Updates")').click()
        time.sleep(2)
        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        s4_logs = self.wd.write_logs(self.wd.read_logs('logcat'), 'D:/test/logs/openupdates_4.log')
        self.wd.write_logs(s1_logs + s2_logs + s3_logs + s4_logs ,'D:/test/logs/openupdates_total.log' )

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()
