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

    def test_fotaautodownload(self):
        self.wd.reset()
        download_button = common.click_checkfota(self.wd, 0, 2)
        download_button.click()  #fota interface point "download" button
        self.check_fotastate(self.wd,"PAUSE")
        self.click_state_button(self.wd, "PAUSE",0)

        time.sleep(2)
        self.check_fotastate(self.wd, "RESUME")
        self.click_state_button(self.wd, "RESUME",0)

        time.sleep(2)
        self.check_fotastate(self.wd, "PAUSE")
        self.click_state_button(self.wd, "PAUSE", 1)

        time.sleep(2)
        self.check_fotastate(self.wd, "RESUME")
        self.click_state_button(self.wd, "RESUME", 1)

        time.sleep(2)
        self.check_fotastate(self.wd, "PAUSE")

        common.change_network(self.wd,4)
        self.check_fotastate(self.wd, "RESUME")
        download_state = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra")
        download_statetext = download_state.get_attribute("text")
        download_statetext1 = download_statetext.split(',')
        self.assertEqual(download_statetext1[0],"Waiting for Wi-Fi")

        common.change_network(self.wd, 6)
        time.sleep(10)
        self.check_fotastate(self.wd, "PAUSE")
        download_state = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra")
        downloadsize = download_state.get_attribute("text").split('/')
        download_percent = float(downloadsize[0]) * 100 / 51.1
        self.wd.open_notifications()
        # self.wd.find_element_by_android_uiautomator('new UiSelector().text("Downloading system update").fromParent(new UiSelector().resourceId("android:id/line3")).childSelector(new UiSelector().resourceId("android:id/text"))')
        noti_downloadp = self.wd.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/'
                                                       'android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/'
                                                       'android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/'
                                                       'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/'
                                                       'android.widget.TextView')
        noti_downloadpc = noti_downloadp.get_attribute("text").split("%")[0]
        if abs(float(noti_downloadpc) - download_percent) > 10:
            print "download percent sync failed "
        self.wd.keyevent(4)

        while(True):
            i = 1
            try:
                fota_state = self.wd.find_element_by_id("selfcom.tcl.ota:id / firmware_install")
            except NoSuchElementException,e:
                try:
                    download_depend = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message")
                except NoSuchElementException,e:
                    common.change_network(6)
                    try:
                        retry_button = self.wd.find_element_by_id("com.tcl.ota:id/firmware_update")
                    except NoSuchElementException,e:
                        print "Download failed and somthing wrong happend"
                        break

                    else:
                        if retry_button.get_attribute("text") == "TRY AGAIN":
                            retry_button.click()
                            i = i + 1
                        else:
                            print "Download failed and not network problem"
                            break


                else:
                    if download_depend.get_attribute("text") == "Downloading system update":
                        time.sleep(10)

            else:
                bettery_value1 = common.get_bettery(self.wd)
                if bettery_value1 < 30:
                    self.assertEqual(fota_state.get_attribute("clickable"),False)
                    bettery_info = self.wd.find_element_by_id("com.tcl.ota:id/firmware_battery_info")
                    self.assertEqual(bettery_info.get_attribute("text"),"	Battery needs > 30% charge to start installation")
                    break
                else:
                    break





        self.wd.keyevent(3)
        self.wd.open_notifications()
        try:
            later_button = self.wd.find_element_by_accessibility_id("LATER")
        except NoSuchElementException,e:
            print "Installing notification pop up failed"
        else:
            later_button.click()
            time.sleep(1)
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("1 hour")').click()
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("OK")').click()

        self.wd.open_notifications()
        try:
            self.wd.find_element_by_accessibility_id("LATER")
        except NoSuchElementException,e:
            pass
        else:
            bettery_icon = self.wd.find_element_by_id("com.android.systemui:id/battery")
            bettery_value = int(bettery_icon.get_attribute("name").split(" ")[1])
            if bettery_value != 100:
                print "Installing notification did not disappeared after point later"

        common.change_time_forfota(self.wd)

        time.sleep(2)
        try:
            install_button = self.wd.find_element_by_accessibility_id("Install")
        except NoSuchElementException,e:
            print "Installing notification pop up failed"
        else:
            install_button.click()
            time.sleep(1)

        install_tital = self.wd.find_element_by_id("com.tcl.ota:id/alertTitle").get_attribute("text")
        self.assertEqual(install_tital,"Install system update?")
        install_message = self.wd.find_element_by_id("android:id/message")
        self.assertEqual(install_message,"	This improves your device's security, performance and software. It will keep your personal data safe.")

        later_button = self.wd.find_element_by_id("android:id/button2")
        self.assertEqual(later_button.get_attribute("text"),"Later")
        later_button.click()
        try:
            install_button = self.wd.find_element_by_id("selfcom.tcl.ota:id / firmware_install")
        except NoSuchElementException,e:
            print "click later button in installing interface failed"
        else:
            install_button.click()

        install_button = self.wd.find_element_by_id("android:id/button1")
        self.assertEqual(install_button.get_attribute("text"),"Install")
        install_button.click()

    def tearDown(self):

        self.wd.quit()

    def check_fotastate(self,device, state):
        state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")
        self.assertEqual(state_button.get_attribute("text"), state)

        device.open_notifications()
        try:
            noti_button = device.find_element_by_id("android:id/action0")
        except NoSuchElementException, e:
            print "downloading page missing" + state
        else:
            self.assertEqual(noti_button.get_attribute("text"), "PAUSE")
        finally:
            device.keyevent(4)

    def click_state_button(self,device,state,type):
        if type == 0:
            state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")

        else:
            device.open_notifications()
            time.sleep(1)
            state_button = device.find_element_by_id("android:id/action0")

        if state_button.get_attribute("text") == state:  # point Pause button in fota interface
            state_button.click()
        else:
            print " point button failed" + state

        if type == 1:
            device.keyevent(4)

if __name__ == '__main__':
    unittest.main()