#coding=utf-8
import unittest
#import selenium.common.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import common
import os
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

    def test_aotaDownloadInstall(self):
        aota_update_app = []
        aota_new_app = []
        aota_app1 = {"name":"Apps","size":"10.0 MB","description":"""
        Apps is an application store of alcatel smartphone, which offers a variety of applications for free downloading. Discover and download apps or games for your phone or tablet through Apps. Enjoy millions of the latest Android apps and games. Anytime, anywhere, with your device. This new version can also help you clean up your phone, make it faster, and protect your cell phone from viruses. So, what are you waiting for? Update it now!
        ""","content":"""
        · Phone Booster A quick booster to free up RAM, clean background tasks, provide extra entrances in widgets, desktop shortcuts and notification toolbar. · Junk Files Cleaner Help analyze and safely remove junk files which take up your memory and storage space. · Antivirus - Virus Cleaner Protect your mobile from virus attack and keep your privacy safe. · Battery Saver Instantly find and fix battery power consumption problems and quickly scan your mobile, save the power consumption of apps and settings. · CPU Cooler Analyze CPU usage and stop overheating apps to cool down CPU temperature, with only 1-tap. · APP Uninstall Help you find rarely used apps, and uninstall unnecessary apps to save more space.
        """}
        aota_app2 = {"name":"Files","size":"5.9 MB","description":"0525","content":"0525"}
        aota_app3 = {"name":"Weather","size":"22.5 MB","description":"wqwewqqwe","content":"weqqewqwe"}
        aota_app4 = {"name":"Turbo Browser","size":"10.5 MB","description":"""
        Turbo Browser, the top ultra-fast and lightweight browser for Android mobile, provides incognito browsing and fast web opening for all the users. It enables fast downloading of video, image, doc, PDF & files; secure & fluent browsing with ad blocker and antivirus. Night mode is included to give you the comfortable browsing experience.
        ""","content":"""
        Features: ✔Private Search ✔Adblocker Provided ✔Fast Open and Download ✔Multiple Search Engines ✔Data Saving ✔News Feed ✔Night Mode ✔Switch Text Font Try the super fast browser for Android right now! Contact Us: For any issue or suggestion, please send us feedbacks via: Twitter: https://twitter.com/TurboBrowser_ Facebook: https://www.facebook.com/TheTurboBrowser/ G+: https://plus.google.com/u/1/communities/116473561383982061062
        """}
        aota_app5 = {"name":"掌阅iReader","size":"16.0 MB","description":"掌阅iReader","content":"掌阅iReader"}
        aota_update_app.append(aota_app1)
        aota_update_app.append(aota_app2)
        aota_update_app.append(aota_app3)
        aota_new_app.append(aota_app4)
        aota_new_app.append(aota_app5)


        common.change_network(self.wd, 0)
        self.wd.reset()     #修改aota自动下载为never
        self.wd.find_element_by_accessibility_id("More options").click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Automatically update")').click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Never")').click()
        print "Disable AOTA autodownload successfully"
        self.wd.keyevent(4)

        common.change_network(self.wd, 2)       #手动点击checkaota数据
        self.wd.find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')[1].click()
        for i in range(1, 10):
            common.swape_bygiven(self.wd, "aotacheck")
            try:
                self.wd.find_element_by_id("com.tcl.ota:id/update_available")
            except NoSuchElementException, e:
                time.sleep(5)
            else:
                print "Check for app update successfully"
                break
            if i > 8:
                print "ERROR:check for app list failed"
        applist = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/name")')
        applist_t = []      #创建applist界面的app列表

        for appelm1 in applist:
            appname = appelm1.get_attribute("text")
            applist_t.append({"name": appname, "size": "", "description": "", "content": "", "state": ""})
        app_button = self.wd.find_elements_by_class_name("android.widget.Button")
        i = 0
        for app_button_elm in app_button:
            buttonname = app_button_elm.get_attribute("text")
            if (buttonname == "UPDATE" or buttonname == "INSTALL" or buttonname == "PAUSE" or buttonname == "RESUME"):
                if len(applist_t) > i:
                    print "state num more than appname's num, check the applist"
                applist_t[i]["state"] = buttonname
                i = i + 1

        app_content = self.wd.find_elements_by_android_uiautomator(
            'new UiSelector().resourceId("com.tcl.ota:id/app_content")')
        i = 0
        for app_content_elm in app_content:
            contenttext = app_content_elm.get_attribute("text")
            applist_t[i]["content"] = contenttext
            i = i + 1

        app_size = self.wd.find_elements_by_android_uiautomator(
            'new UiSelector().resourceId("com.tcl.ota:id/status")')
        i = 0
        for app_size_elm in app_size:
            size_num = app_size_elm.get_attribute("text")
            applist_t[i]["size"] = size_num
            i = i + 1

        for appifo in applist_t:
            print appifo
















    def tearDown(self):
        self.wd.quit()


if __name__ == '__main__':
    unittest.main()