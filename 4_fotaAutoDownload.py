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
        # common.enable_fota_advance(self.wd, "FOTA")
        self.wd.find_element_by_accessibility_id("More options").click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
        elm1 = self.wd.find_elements_by_class_name("android.widget.Switch")
        str1 = elm1[0].get_attribute("text")
        if str1 == u'Off':      # 确保打开FOTA autodownload
            elm1[0].click()
            print "enable FOTA Auto-Download succsessfully"


        download_button = common.click_checkfota(self.wd, 0, 2) #删除已存在的差分包并开始check后自动下载
        if download_button.get_attribute("text") == u"CHECK FOR UPDATES NOW":
            download_button.click() # if downloading does not begin ,fota interface point "download" button
            print "Downloading did not begined,click the download button maully"

        self.check_fotastate(self.wd, u"PAUSE")
        print "Auto download begined"

        self.click_state_button(self.wd, "PAUSE", 0) #在fota interface 点击PAUSE
        time.sleep(2)
        self.check_fotastate(self.wd, u"RESUME")
        print "PAUSE the downloading in update interface seccessfully"

        self.click_state_button(self.wd, "RESUME", 0) #在fota interface 点击RESUME
        time.sleep(2)
        self.check_fotastate(self.wd, u"PAUSE")
        print "RESUME the downloading in update interface seccessfully"

        self.click_state_button(self.wd, "PAUSE", 1) #在notification bar 点击 PAUSE
        time.sleep(2)
        self.check_fotastate(self.wd, u"RESUME")
        print "PAUSE the downloading in notification bar seccessfully"


        self.click_state_button(self.wd, "RESUME", 1)#在notification bar 点击 RESUME
        time.sleep(2)
        self.check_fotastate(self.wd, u"PAUSE")
        print "RESUME the downloading in notification bar seccessfully"

        common.change_network(self.wd,4)    #断开Wi-Fi后查看FOTA界面状态
        self.check_fotastate(self.wd, "RESUME")
        download_state = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra")
        download_statetext = download_state.get_attribute("text")
        download_statetext1 = download_statetext.split(',')
        self.assertEqual(download_statetext1[0],"Waiting for Wi-Fi")
        print "Wi-Fi disconnected,And FOTA interface display normally" + download_statetext1[0]

        common.change_network(self.wd, 6)       #恢复Wi-Fi后检查FOTA是否恢复下载
        time.sleep(10)
        self.check_fotastate(self.wd, "PAUSE")
        print "FOTA redownload seccussfully"

        #截取FOTA界面的下载百分比和notification中的下载百分比对比
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
        print "FOTA download %F%% and %s%% in notification" % (download_percent,noti_downloadpc)
        if abs(float(noti_downloadpc) - download_percent) > 10: #百分比不能超过10%
            print "download percent sync failed "
        self.wd.keyevent(4)
        print "download percent sync normally"

        while (True):  # 持续监控差分包是否下载完成

            try:
                fota_state = self.wd.find_element_by_id("com.tcl.ota:id/firmware_install")
            except NoSuchElementException, e:
                try:
                    download_depend = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message")
                except NoSuchElementException, e:
                    # 检测网络问题或者意外暂停了，点击retry
                    common.change_network(self.wd, 6)
                    try:
                        retry_button = self.wd.find_element_by_id("com.tcl.ota:id/firmware_update")
                    except NoSuchElementException, e:
                        print "Download failed and somthing wrong happend"
                        break

                    else:
                        if (retry_button.get_attribute("text") == "TRY AGAIN") or (
                                retry_button.get_attribute("text") == "RESUME"):
                            retry_button.click()
                        else:
                            print "Download failed and not network problem"
                            break


                else:
                    if download_depend.get_attribute("text") == "Downloading system update":
                        time.sleep(10)
                    else:
                        print "Download failed and somthing wrong happend1"

            else:
                print "Download complete"
                bettery_value1 = common.get_bettery(self.wd)
                self.wd.launch_app()
                print bettery_value1
                if bettery_value1 < 30:
                    # self.assertEqual(fota_state.get_attribute("clickable"), False)
                    bettery_info = self.wd.find_element_by_id("com.tcl.ota:id/firmware_battery_info")
                    self.assertEqual(bettery_info.get_attribute("text"),
                                     "Battery needs > 30% charge to start installation")
                    print "bettry to low need charge for a moment"
                    break
                else:
                    break

        time.sleep(10)
        self.wd.keyevent(3)
        self.wd.open_notifications()
        try:  # 点击LATER按钮并点击1 hour later
            later_button = self.wd.find_element_by_accessibility_id("LATER")
        except NoSuchElementException, e:
            print "Installing notification pop up failed"
        else:
            later_button.click()
            time.sleep(1)
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("1 hour")').click()
            self.wd.find_element_by_android_uiautomator('new UiSelector().text("OK")').click()
            print "Clicked the later-1hour button"
        self.wd.open_notifications()
        try:  # 如果notificaiton未消失，查看是否电量100%
            self.wd.find_element_by_accessibility_id("LATER")
        except NoSuchElementException, e:
            pass
        else:
            bettery_icon = self.wd.find_element_by_id("com.android.systemui:id/battery")
            bettery_value = int(bettery_icon.get_attribute("name").split(" ")[1])
            if bettery_value != 100:
                print "Installing notification did not disappeared after point later"
            else:
                print "Bettery 100% and notification poped up again"

        common.change_time_forfota(self.wd)  # 向后修改时间并check notification是否能正常再次弹出
        time.sleep(20)
        self.wd.open_notifications()
        time.sleep(2)
        try:
            install_button = self.wd.find_element_by_accessibility_id("Install")
        except NoSuchElementException, e:
            print "Installing notification pop up failed"
        else:
            install_button.click()  # 点击install按钮
            time.sleep(1)

        print "Clicked the install button in notification "
        install_tital = self.wd.find_element_by_id("com.tcl.ota:id/alertTitle").get_attribute("text")
        self.assertEqual(install_tital, "Install system update?")
        install_message = self.wd.find_element_by_id("android:id/message").get_attribute("text")
        self.assertEqual(install_message,
                         u"This improves your device's security, performance and software. It will keep your personal data safe.")

        later_button = self.wd.find_element_by_id("android:id/button2")
        self.assertEqual(later_button.get_attribute("text"), "Later")
        later_button.click()
        try:
            install_button = self.wd.find_element_by_id("com.tcl.ota:id/firmware_install")
        except NoSuchElementException, e:
            print "could not find installing button in FOTA interface"
        else:
            install_button.click()
            print "Clicked the install button in FOTA interface "
        install_button = self.wd.find_element_by_id("android:id/button1")
        self.assertEqual(install_button.get_attribute("text"), "Install")
        # install_button.click()
        print "now installing"

    def tearDown(self):

        self.wd.quit()

    def click_state_button(self,device,state,type):  # 在type页面点击state按钮
        if type == 0:   # 在update主界面点击state键
            state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")
            print "state 0"
        else:       #在notification bar上点击state键
            print "now open notification "
            device.open_notifications()
            print "state 1"
            '''
            updates_int = "PAUSE" 
            updates_noti = "Pause"
            updates_int = "RESUME"
            updates_noti = "RESUME"
            
            '''
            if (state == "PAUSE"):
                state = state.capitalize()
            time.sleep(2)
            print state
            device.open_notifications()
            time.sleep(2)
            state_button = device.find_element_by_accessibility_id(state)

        if state_button.get_attribute("text") == state:  # point Pause button in fota interface/notificationbar
            state_button.click()
        else:
            print " point button failed" + state

        if type == 1:       #如果在notification中点击state键需要在结束时点击back按钮
            device.keyevent(4)

    def check_fotastate(self,device, state):
        device.launch_app()
        time.sleep(2)
        state_button = device.find_element_by_id("com.tcl.ota:id/firmware_update")
        self.assertEqual(state_button.get_attribute("text"), state) #比较update interface中状态值与state

        device.open_notifications()         #比较update notification bar中状态值与state
        time.sleep(2)
        try:
            noti_button = device.find_element_by_id("android:id/action0")
        except NoSuchElementException, e:
            print "downloading page missing" + state
        else:
            if(state == u"PAUSE"):
                state = state.capitalize()
            self.assertEqual(noti_button.get_attribute("text"), state)

        finally:
            device.keyevent(4)

if __name__ == '__main__':
    unittest.main()