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

        self.wd.set_network_connection(0)
        self.wd.reset()
        # need to clear the app's data.ok
        #common.enable_fota_advance(self.wd, "FOTA")
        self.wd.find_element_by_accessibility_id("More options").click()
        self.wd.find_element_by_android_uiautomator('new UiSelector().text("Settings")').click()
        elm1 = self.wd.find_elements_by_class_name("android.widget.Switch")
        str1 = elm1[0].get_attribute("text")
        print "%r" %str1
        if str1 == u'On':
            elm1[0].click()
        self.wd.keyevent(4)
        time.sleep(2)
        self.wd.set_network_connection(2)
        for i in range(1, 6):

            try:
                elm2 = self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text")
            except NoSuchElementException, e:
                pass
            else:
                if elm2 != u"CHECK FOR UPDATES NOW":
                    svn_value = self.wd.find_element_by_id("com.tcl.ota:id/firmware_system_version").get_attribute("text")
                    self.assertEqual(svn_value, u"6.0-01007")
                    package_size = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra").get_attribute("text")
                    print "%r" %package_size
                    self.assertEqual(package_size, u'01008\x08(50.5 MB)')
                    state_message = self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message").get_attribute("text")
                    print "%r" %state_message
                    self.assertEqual(state_message, u"System update available")
                    #self.wd.find_element_by_id("com.tcl.ota:id/firmware_info").click()
                    #detail_title = self.wd.find_element_by_id("com.tcl.ota:id/firmware_detail_title_shadow")
                    #self.assertEqual(detail_title, "New in this version")
                    #detail_content = self.wd.find_element_by_id("com.tcl.ota:id/firmware_detail_content")
                    #self.assertEqual(detail_content, "UPDATE TO A8")
                    self.wd.keyevent(4)
                    break
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_bottomright").click()
            time.sleep(20)
            if i > 4:
                raise common.CantSearchedFotaPackage


        # Notification check
        time.sleep(5)
        self.wd.open_notifications()
        try:
            fota_noti = self.wd.find_element_by_android_uiautomator(
                'new UiSelector().text("System update available")')
        except NoSuchElementException, e:
            pass
        else:
            fota_noti.click()

        self.assertEqual(self.wd.current_activity, ".SystemUpdatesActivity")
        self.wd.keyevent(3)
        self.wd.open_notifications()

        # point "Download" in different ways
        time.sleep(2)
        self.wd.find_element_by_accessibility_id("Download").click()
        self.wd.launch_app()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"), "PAUSE")
        download_button = common.click_checkfota(self.wd, 0, 2)# point download button
        download_button.click()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"), "PAUSE")
        download_icon = common.click_checkfota(self.wd, 1, 2) # point download image icon
        download_icon.click()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"), "PAUSE")


        download_button = common.click_checkfota(self.wd, 0, 0)  # point download button when no network
        download_button.click()
        time.sleep(3)
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message").get_attribute("text"), u"No internet connection")
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra").get_attribute("text")[0:23], u"Couldn't start download")
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"), u"TRY AGAIN")

        common.click_checkfota(self.wd, 0, 4)  # point download when only data nerwork
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message").get_attribute("text"),
                         u"System update available")
        self.assertEqual(
            self.wd.find_element_by_id("com.tcl.ota:id/firmware_state_message_extra").get_attribute("text"),
            u'01008\x08(50.5 MB)')
        self.assertEqual(self.wd.find_element_by_id("com.tcl.ota:id/firmware_update").get_attribute("text"),
                         u"DOWNLOAD UPDATE")
        #common.fill_ram()     #now will not add the fill ram function
        #common.click_checkfota(self.wd, 0, 2)

        common.write_logs(s1_logs, 'D:/test/logs/openupdates_total.log')
    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()

