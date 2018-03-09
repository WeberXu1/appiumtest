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
        self.wd = common.UpdateWebDriver('http://127.0.0.1:4723/wd/hub')
        self.wd.read_logs('logcat', ignore=True)
        print "begin logtime" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.aota_update_app = []
        aota_new_app = []
        aota_app1 = {"name": u"Apps", "size": u"10.0 MB", "description": u"""
                Apps is an application store of alcatel smartphone, which offers a variety of applications for free downloading. Discover and download apps or games for your phone or tablet through Apps. Enjoy millions of the latest Android apps and games. Anytime, anywhere, with your device. This new version can also help you clean up your phone, make it faster, and protect your cell phone from viruses. So, what are you waiting for? Update it now!
                """, "content": u"""
                · Phone Booster A quick booster to free up RAM, clean background tasks, provide extra entrances in widgets, desktop shortcuts and notification toolbar. · Junk Files Cleaner Help analyze and safely remove junk files which take up your memory and storage space. · Antivirus - Virus Cleaner Protect your mobile from virus attack and keep your privacy safe. · Battery Saver Instantly find and fix battery power consumption problems and quickly scan your mobile, save the power consumption of apps and settings. · CPU Cooler Analyze CPU usage and stop overheating apps to cool down CPU temperature, with only 1-tap. · APP Uninstall Help you find rarely used apps, and uninstall unnecessary apps to save more space.
                ""","state":u"UPDATE"}
        aota_app2 = {"name": u"Files", "size": u"5.9 MB", "description": u"0525", "content": u"0525","state":u"UPDATE"}
        aota_app3 = {"name": u"Weather", "size": u"22.5 MB", "description": u"wqwewqqwe", "content": u"weqqewqwe","state":u"UPDATE"}
        aota_app4 = {"name": u"Turbo Browser", "size": u"10.5 MB", "description": u"Turbo Browser, the top ultra-fast and lightweight browser for Android mobile, provides incognito browsing and fast web opening for all the users. It enables fast downloading of video, image, doc, PDF & files; secure & fluent browsing with ad blocker and antivirus. Night mode is included to give you the comfortable browsing experience.", "content": u"Features:\n\u2714Private Search\n\u2714Adblocker Provided\n\u2714Fast Open and Download\n\u2714Multiple Search Engines\n\u2714Data Saving\n\u2714News Feed\n\u2714Night Mode\n\u2714Switch Text Font\n\nTry the super fast browser for Android right now!\n\nContact Us:\nFor any issue or suggestion, please send us feedbacks via: \nTwitter: https://twitter.com/TurboBrowser_\nFacebook: https://www.facebook.com/TheTurboBrowser/\nG+: https://plus.google.com/u/1/communities/116473561383982061062","state":u"INSTALL"}
        aota_app5 = {"name": u"掌阅iReader", "size": u"16.0 MB", "description": u"掌阅iReader", "content": u"掌阅iReader","state":u"INSTALL"}
        #aota_update_app.append(aota_app1)
        self.aota_update_app.append(aota_app2)
        self.aota_update_app.append(aota_app3)
        self.aota_update_app.append(aota_app4)
        #aota_new_app.append(aota_app5)
       # self.wd.implicitly_wait(60)

    def test_putupdatetoscreen(self):
        self.aota_applist_load(0)
        applist = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/name")')
        applist_t = []

        for appelm1 in applist:  # 获取AOTA app列表中的项
            appname = appelm1.get_attribute("text")
            applist_t.append({"name": appname, "size": "", "description": "", "content": "", "state": ""})
        app_button = self.wd.find_elements_by_class_name("android.widget.Button")
        i = 0
        for app_button_elm in app_button:
            buttonname = app_button_elm.get_attribute("text")
            if (buttonname == "UPDATE" or buttonname == "INSTALL" or buttonname == "PAUSE" or buttonname == "RESUME"):
                if len(applist_t) < i:
                    print "state num more than appname's num, check the applist"
                if len(applist_t) == 0:
                    print applist
                applist_t[i]["state"] = buttonname
                i = i + 1

        app_content = self.wd.find_elements_by_android_uiautomator(
            'new UiSelector().resourceId("com.tcl.ota:id/app_content")')
        print app_content
        i = 0
        for app_content_elm in app_content:  # 将applist中获取的content 项加入到 app列表数组中
            contenttext = app_content_elm.get_attribute("text")
            applist_t[i]["content"] = contenttext
            i = i + 1

        app_size = self.wd.find_elements_by_android_uiautomator(
            'new UiSelector().resourceId("com.tcl.ota:id/status")')
        i = 0
        for app_size_elm in app_size:  # 将applist中获取的size 项加入到 app列表数组中
            size_num = app_size_elm.get_attribute("text")
            applist_t[i]["size"] = size_num
            i = i + 1

        for appifo in applist_t:
            print appifo

        app_detail_list = []  # 创建详情界面applist
        for appelm1 in applist:  # 获取所有applist应用详情页面的信息
            appelm1.click()
            self.wd.swape_bygiven("allappdown")
            time.sleep(2)
            appdet_state = self.wd.find_element_by_class_name("android.widget.Button").get_attribute("text")
            appdet_name = self.wd.find_element_by_id("com.tcl.ota:id/name").get_attribute("text")
            if (appdet_state == "INSTALL" or appdet_state == "UPDATE"):
                appdet_content_s = self.wd.find_element_by_id("com.tcl.ota:id/app_content").get_attribute("text")
                appdet_size = self.wd.find_element_by_id("com.tcl.ota:id/app_size").get_attribute("text")
                if (appdet_content_s.find("[New]", 0, 5) != -1):
                    appdet_content_s = appdet_content_s[6:]
            else:
                appdet_content_s = ""
                appdet_size = ""
            time.sleep(2)
            appdet_detail = self.wd.find_elements_by_android_uiautomator(
                'new UiSelector().resourceId("com.tcl.ota:id/expandable_text")')
            while True:
                if len(appdet_detail) == 0:
                    time.sleep(5)
                    appdet_detail = self.wd.find_elements_by_android_uiautomator(
                        'new UiSelector().resourceId("com.tcl.ota:id/expandable_text")')
                else:
                    break
            appdet_description = appdet_detail[0].get_attribute("text")
            appdet_content = appdet_detail[1].get_attribute("text")
            if (appdet_content_s != ""):
                if appdet_content.replace("\n", "").replace(" ", "") != appdet_content_s.replace(" ", ""):
                    print "xontent : %r" % appdet_content.replace("\n", "").replace(" ", "")
                    print "xontent short: %r " % appdet_content_s.replace(" ", "")
                    print "ERROR:app content in detail is different from short one"

            app_detail = {"name": appdet_name, "size": appdet_size, "description": appdet_description,
                          "content": appdet_content, "state": appdet_state}
            app_detail_list.append(app_detail)
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_detail_app_bar_close").click()

        print "NOW APPDETAIL"
        i = 0
        for appifo1 in app_detail_list:
            print appifo1
        for appifo2 in app_detail_list:  # 对比详情页面和applist页面中的信息是否一致
            self.assertEqual(appifo2["name"], applist_t[i]["name"])
            if appifo2["state"] != "OPEN":
                self.assertEqual(appifo2["state"], applist_t[i]["state"])
                if (applist_t[i]["content"].find("[New]", 0, 5) != -1):
                    applist_t[i]["content"] = applist_t[i]["content"][6:]
                self.assertEqual(appifo2["content"].replace(" ", "").replace("\n", ""),
                                 applist_t[i]["content"].replace(" ", ""))
                self.assertEqual(appifo2["size"], applist_t[i]["size"])

                print "@@@"
                print appifo2
                print self.aota_update_app[i]
                # self.assertEqual(appifo2 in self.aota_update_app , True)
                self.assertEqual(appifo2["state"], self.aota_update_app[i]["state"])
                print appifo2["content"]
                print appifo2["content"].replace(" ", "").replace("\n", "").replace("\u2741", "")
                print "%r" % (appifo2["content"].replace(" ", "").replace("\n", "").replace("\u2741", ""))
                print "%r" % (self.aota_update_app[i]["content"].replace(" ", ""))
                self.assertEqual(appifo2["content"].replace(" ", "").replace("\n", "").replace("\u2741", ""),
                                 self.aota_update_app[i]["content"].replace(" ", "").replace("\n", ""))
                self.assertEqual(appifo2["size"], self.aota_update_app[i]["size"])

            i = i + 1
















    def tearDown(self):
        self.wd.quit()


if __name__ == '__main__':
    unittest.main()