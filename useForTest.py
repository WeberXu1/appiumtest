#coding=utf-8
import unittest
#import selenium.common.exceptions
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
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub',common.capabilities_set(2))
        common.read_logs(self.wd, 'logcat', ignore=True)
        print "begin logtime" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
       # self.wd.implicitly_wait(60)

    def test_putupdatetoscreen(self):
        self.wd.reset()
        self.wd.launch_app()
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
        applist_t = []

        for appelm1 in applist:
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

        app_detail_list = []
        for appelm1 in applist:
            appelm1.click()
            common.swape_bygiven(self.wd,"allappdown")
            time.sleep(1)
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
        for appifo1 in app_detail_list:
            print appifo1





    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()


