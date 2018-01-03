import unittest
#import selenium.common.exceptions
from appium import webdriver
import time
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.common.by import By
import common

class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set())

    def test_switch(self):
        self.tabsapp = self.wd.find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')
        self.tabsapp[1].click()
        time.sleep(2)
        self.result = self.wd.find_elements_by_class_name('android.view.ViewGroup')
        self.assertIsNotNone(self.result, "fail to switch to app list")
        self.assertTrue(self.tabsapp[1].is_selected())
        self.tabsapp[0].click()
        time.sleep(2)
        self.wd.swipe(662, 935, 25, 935, 1500)
        time.sleep(2)
        self.wd.swipe(25, 935, 662, 935, 1500)
        time.sleep(10)

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()
