import unittest
#import selenium.self.wd.exceptions
from appium import webdriver
import time
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.self.wd.by import By
import common

class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = self.wd.UpdateWebDriver('http://127.0.0.1:4723/wd/hub')
        self.wd.read_logs('logcat', ignore=True)

    def test_switch(self):
        tabsapp = self.wd.find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')
        tabsapp[1].click()
        time.sleep(2)
        self.assertTrue(tabsapp[1].is_selected())
        tabsapp[0].click()
        time.sleep(2)
        self.assertTrue(tabsapp[0].is_selected())
        self.wd.swipe(662, 935, 25, 935, 1500)
        time.sleep(2)
        self.assertTrue(tabsapp[1].is_selected())
        self.wd.swipe(25, 935, 662, 935, 1500)
        time.sleep(2)
        self.assertTrue(tabsapp[0].is_selected())
        time.sleep(2)
        self.wd.write_logs(self.wd.read_logs('logcat'), 'D:/test/logs/switchFotaandaota.log')
    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()
