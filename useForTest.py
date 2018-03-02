#coding=utf-8
import unittest
#import selenium.self.wd.exceptions
from appium import webdriver
from selenium.common.exceptions import  NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import common
import os
from datetime import datetime
import subprocess
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction

class AppTest(unittest.TestCase):

    def setUp(self):
        self.wd = common.UpdateWebDriver('http://127.0.0.1:4723/wd/hub',2)
        self.wd.read_logs('logcat', ignore=True)
        print "begin logtime" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.aota_update_app = []
        aota_new_app = []
        aota_app1 = {"name": u"Apps", "size": u"10.0 MB", "description": u"""Apps is an application store of alcatel smartphone, which offers a variety of applications for free downloading. Discover and download apps or games for your phone or tablet through Apps. Enjoy millions of the latest Android apps and games. Anytime, anywhere, with your device. This new version can also help you clean up your phone, make it faster, and protect your cell phone from viruses. So, what are you waiting for? Update it now!
                """, "content": u"""· Phone Booster A quick booster to free up RAM, clean background tasks, provide extra entrances in widgets, desktop shortcuts and notification toolbar. · Junk Files Cleaner Help analyze and safely remove junk files which take up your memory and storage space. · Antivirus - Virus Cleaner Protect your mobile from virus attack and keep your privacy safe. · Battery Saver Instantly find and fix battery power consumption problems and quickly scan your mobile, save the power consumption of apps and settings. · CPU Cooler Analyze CPU usage and stop overheating apps to cool down CPU temperature, with only 1-tap. · APP Uninstall Help you find rarely used apps, and uninstall unnecessary apps to save more space.
                ""","state":u"UPDATE"}
        aota_app2 = {"name": u"Files", "size": u"5.9 MB", "description": u"0525", "content": u"0525","state":u"UPDATE"}
        aota_app3 = {"name": u"Weather", "size": u"22.5 MB", "description": u"wqwewqqwe", "content": u"weqqewqwe","state":u"UPDATE"}
        aota_app4 = {"name": u"Turbo Browser", "size": u"10.5 MB", "description": u"Turbo Browser, the top ultra-fast and lightweight browser for Android mobile, provides incognito browsing and fast web opening for all the users. It enables fast downloading of video, image, doc, PDF & files; secure & fluent browsing with ad blocker and antivirus. Night mode is included to give you the comfortable browsing experience.", "content": u"Features:\n\u2714Private Search\n\u2714Adblocker Provided\n\u2714Fast Open and Download\n\u2714Multiple Search Engines\n\u2714Data Saving\n\u2714News Feed\n\u2714Night Mode\n\u2714Switch Text Font\n\nTry the super fast browser for Android right now!\n\nContact Us:\nFor any issue or suggestion, please send us feedbacks via: \nTwitter: https://twitter.com/TurboBrowser_\nFacebook: https://www.facebook.com/TheTurboBrowser/\nG+: https://plus.google.com/u/1/communities/116473561383982061062","state":u"INSTALL"}
        aota_app5 = {"name": u"掌阅iReader", "size": u"16.0 MB", "description": u"掌阅iReader", "content": u"掌阅iReader","state":u"INSTALL"}
        self.aota_update_app.append(aota_app1)
        self.aota_update_app.append(aota_app2)
        self.aota_update_app.append(aota_app3)
        self.aota_update_app.append(aota_app4)
        #aota_new_app.append(aota_app5)
       # self.wd.implicitly_wait(60)

    def test_putupdatetoscreen(self):
        self.aota_applist_load(0)
        applist = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/name")')
        applist_t = []

        for appelm1 in applist:        #获取AOTA app列表中的项
            appname = appelm1.get_attribute("text")
            applist_t.append({"name": appname , "size": "", "description": "", "content": "","state":""})
        app_button = self.wd.find_elements_by_class_name("android.widget.Button")
        i = 0
        for app_button_elm in app_button:
            buttonname = app_button_elm.get_attribute("text")
            if(buttonname == "UPDATE" or buttonname == "INSTALL" or buttonname == "PAUSE" or buttonname == "RESUME"):
                if len(applist_t) < i:
                    print "state num more than appname's num, check the applist"
                applist_t[i]["state"] = buttonname
                i = i + 1


        app_content = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/app_content")')
        i = 0
        for app_content_elm in app_content:     #将applist中获取的content 项加入到 app列表数组中
            contenttext = app_content_elm.get_attribute("text")
            applist_t[i]["content"] = contenttext
            i = i + 1

        app_size = self.wd.find_elements_by_android_uiautomator(
            'new UiSelector().resourceId("com.tcl.ota:id/status")')
        i = 0
        for app_size_elm in app_size:   #将applist中获取的size 项加入到 app列表数组中
            size_num = app_size_elm.get_attribute("text")
            applist_t[i]["size"] = size_num
            i = i + 1

        for appifo in applist_t:
            print appifo

        app_detail_list = []        #创建详情界面applist
        for appelm1 in applist:     #获取所有applist应用详情页面的信息
            appelm1.click()
            self.wd.swape_bygiven("allappdown")
            time.sleep(2)
            appdet_state = self.wd.find_element_by_class_name("android.widget.Button").get_attribute("text")
            appdet_name = self.wd.find_element_by_id("com.tcl.ota:id/name").get_attribute("text")
            if (appdet_state == "INSTALL" or appdet_state == "UPDATE"):
                appdet_content_s = self.wd.find_element_by_id("com.tcl.ota:id/app_content").get_attribute("text")
                appdet_size = self.wd.find_element_by_id("com.tcl.ota:id/app_size").get_attribute("text")
                if(appdet_content_s.find("[New]",0,5) != -1):
                    appdet_content_s = appdet_content_s[6:]
            else:
                appdet_content_s = ""
                appdet_size = ""
            time.sleep(1)
            appdet_detail = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/expandable_text")')
            appdet_description = appdet_detail[0].get_attribute("text")
            appdet_content = appdet_detail[1].get_attribute("text")
            if (appdet_content_s != ""):
                if appdet_content.replace("\n","").replace(" ","") != appdet_content_s.replace(" ",""):
                    print "xontent : %r" % appdet_content.replace("\n","").replace(" ","")
                    print "xontent short: %r " % appdet_content_s.replace(" ","")
                    print "ERROR:app content in detail is different from short one"


            app_detail = {"name": appdet_name, "size": appdet_size, "description": appdet_description, "content": appdet_content, "state": appdet_state}
            app_detail_list.append(app_detail)
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_detail_app_bar_close").click()

        print "NOW APPDETAIL"
        i = 0
        for appifo1 in app_detail_list:
            print appifo1
        for appifo2 in app_detail_list: #对比详情页面和applist页面中的信息是否一致
            self.assertEqual(appifo2["name"],applist_t[i]["name"])
            if appifo2["state"] != "OPEN":
                self.assertEqual(appifo2["state"],applist_t[i]["state"])
                if (applist_t[i]["content"].find("[New]", 0, 5) != -1):
                    applist_t[i]["content"] = applist_t[i]["content"][6:]
                self.assertEqual(appifo2["content"].replace(" ","").replace("\n",""),applist_t[i]["content"].replace(" ",""))
                self.assertEqual(appifo2["size"],applist_t[i]["size"])

                print "@@@"
                print appifo2
                print self.aota_update_app[i]
                self.assertEqual(appifo2 in self.aota_update_app , True)

            i = i + 1

        self.aota_applist_load(0)
        self.open_noti_button()
        self.click_button_noti("INSTALL")
        self.check_aota_state(applist_t, app_button, "INSTALL")

        self.aota_applist_load(0)
        self.open_noti_button()
        self.click_button_noti("UPDATE")
        self.check_aota_state(applist_t, app_button, "UPDATE")
















































    def tearDown(self):
        self.wd.quit()

    def aota_applist_load(self, auto_type,network_type=2 ):
        self.wd.reset()# 重置手机并重新check applist
        if auto_type == 2 or auto_type == 0:#0:NEVER 1:Using Wi-Fi only 2:Using Wi-Fi & DATA
            if auto_type == 2:
                self.wd.change_network(0)
            else:
                self.wd.change_network(4)
            time.sleep(2)
            self.wd.find_element_by_accessibility_id("More options").click()
            time.sleep(1)
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("Automatically update")').click()
            auto_type_issue = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("android:id/text1")')
            auto_type_issue[auto_type].click()
            self.wd.press_keycode(4)
        elif auto_type != 1:
            print "ERROR:WRONG parm"

        time.sleep(2)
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("SYSTEM APPS")').click()
        for i in range(1, 10):
            self.wd.swape_bygiven( "aotacheck")
            try:
                self.wd.find_element_by_id("com.tcl.ota:id/update_available")
            except NoSuchElementException, e:
                time.sleep(5)
            else:
                print "Check for app update successfully"
                break
            if i > 8:
                print "ERROR:check for app list failed"

        if auto_type != 1:
            self.wd.change_network(network_type)


    def open_noti_button(self):
        self.wd.open_notifications()
        display_icon = self.wd.find_elements_by_android_uiautomator(
            'new UiSelector().resourceId("android:id/expand_button")')
        if len(display_icon) != 0:  # 打开notification bar 并显示所有的隐藏按钮
            for display_icon_t in display_icon:
                display_icon_t.click()

    def find_install_icon(self,button):
        try:
            button_all = button + " ALL"#点击新安装的应用的按钮INSTALL
            install_button_noti = self.wd.find_element_by_accessibility_id(button_all)
        except NoSuchElementException,e:
            return self.wd.find_element_by_accessibility_id(button)
        else:
            return install_button_noti

    def click_button_noti(self,button):
        self.find_install_icon(button).click()
        print "Click the " + button + "button successfully"

    def check_aota_state(self,applist1,appnonlystate,mode):
        for installing_app in reversed(applist1):
            if installing_app["state"] == mode:
                str = "Updating" + installing_app["name"]
                try:
                    new_install_noti = self.wd.find_element_by_android_uiautomator('new UiSelector().text("' + str + '")')
                except NoSuchElementException,e:
                    print "ERROR:No downloading notification after click " + mode + " all button"
                else:
                    print "Downloading notification normally"
                    new_install_noti.click()
                now_applist_state = self.wd.find_elements_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/update_button")')
                installing_app_state = now_applist_state[applist1.index(installing_app)]
                self.assertEqual(installing_app_state.get_attribute("text"),u"PAUSE")
                installing_app_content = self.wd.find_element_by_android_uiautomator('new UiSelector().resourceId("com.tcl.ota:id/progressvalue")')
                self.assertEqual(installing_app_content.get_attribute("text"),"Downloading")
                print "Check the downloading state successfully in AOTA interface "

                self.aota_applist_load(0)


                now_applist_state = self.wd.find_elements_by_android_uiautomator(
                    'new UiSelector().resourceId("com.tcl.ota:id/update_button")')
                installing_app_state = now_applist_state[applist1.index(installing_app)]
                #self.assertEqual(installing_app_state.get_attribute("text"), u"RESUME")
                installing_app_state.click()

                now_applist_state = self.wd.find_elements_by_android_uiautomator(
                    'new UiSelector().resourceId("com.tcl.ota:id/update_button")')
                installing_app_state = now_applist_state[applist1.index(installing_app)]
                self.assertEqual(installing_app_state.get_attribute("text"), u"Paused")
                installing_app_state.click()


                now_applist_state = self.wd.find_elements_by_android_uiautomator(
                    'new UiSelector().resourceId("com.tcl.ota:id/update_button")')
                installing_app_state = now_applist_state[applist1.index(installing_app)]
                self.assertEqual(installing_app_state.get_attribute("text"), u"Resume")
                installing_app_state.click()
                print "PAUSE " + mode + "in AOTA interface successfully"

                now_applist_state = self.wd.find_elements_by_android_uiautomator(
                    'new UiSelector().resourceId("com.tcl.ota:id/update_button")')
                installing_app_state = now_applist_state[applist1.index(installing_app)]
                self.assertEqual(installing_app_state.get_attribute("text"), u"Pause")
                print "RESUME " + mode + "in AOTA interface successfully"


                print "Wait for downloading finished"

                while True:
                    self.wd.press_keycode(3)
                    self.wd.launch_app()
                    self.wd.find_elements_by_class_name('android.support.v7.app.ActionBar$Tab')[1].click()
                    now_applist_state = self.wd.find_elements_by_android_uiautomator(
                        'new UiSelector().resourceId("com.tcl.ota:id/update_button")')
                    if mode == "INSTALL":
                        if len(now_applist_state) != (len(appnonlystate) - 1):
                            str2 = 'new UiSelector().text("' +  installing_app["name"] + '")'
                            self.wd.swape_findelm("allappdown",str2,MobileBy.ANDROID_UIAUTOMATOR).click()
                            detail_button = self.wd.find_element_by_id("com.tcl.ota:id/update_button")
                            self.assertEqual(detail_button.get_attribute("text"),"OPEN")
                            self.wd.press_keycode(4)
                            print "New app " + mode + " successfully"
                            break
                    elif mode == "UPDATE":
                        if len(now_applist_state) != (len(appnonlystate) - 1):
                            str2 = 'new UiSelector().text("' + installing_app["name"] + '")'
                            self.wd.swape_findelm( "allappdown", str2, MobileBy.ANDROID_UIAUTOMATOR).click()
                            detail_button = self.wd.find_element_by_id("com.tcl.ota:id/update_button")
                            self.assertEqual(detail_button.get_attribute("text"), "OPEN")
                            self.wd.press_keycode(4)
                            print "UPDATE app " + mode + " successfully"
                            break
                        installing_app_state = now_applist_state[now_applist_state[applist1.index(installing_app)]]
                        if installing_app_state.get_attribute("text") == "INSTALL":
                            print "UPDATE APP download successfully"
                            installing_app_state.click()
                    time.sleep(5)
                break
if __name__ == '__main__':
    unittest.main()


