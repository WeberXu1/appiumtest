import unittest
#import selenium.common.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
import time
import common
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.mobileby import MobileBy

class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set())
        common.read_logs(self.wd, 'logcat', ignore=True)
       # self.wd.implicitly_wait(60)

    def test_fotanoautodownload(self):
        s1_logs = common.write_logs(common.read_logs(self.wd, 'logcat'), 'D:/test/logs/openupdates_1.log')
        common.write_logs(s1_logs, 'D:/test/logs/openupdates_total.log')

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()

