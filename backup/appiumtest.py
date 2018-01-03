#coding=utf-8
from appium import webdriver
print "started"
capabilities = {};
# 测试平台，与测试设备名字，由于这里是真机，所以设备名字不生效
capabilities['platformName'] = 'Android'
capabilities['deviceName'] = 'Android Emulator'
# 安卓测试版本，真机这里也不生效
capabilities['platformVersion'] = '6.0'
# 设置支持的编码，这样设置后可以输入中文
capabilities['unicodeKeyboard'] = 'True'
capabilities['resetKeyboard'] = 'True'
# 设置APP的主包名和入口类
capabilities['appPackage'] = 'com.example.android.contactmanager'
#capabilities['app'] = "C:\Users\\77465\\eclipse-workspace\\appiumdemo\\apps\\ContactManager.apk"
capabilities['appActivity'] = '.ContactManager'
# 初始化
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', capabilities)
#发送一个JSON格式capabilities 给服务器暴露REST API _http://127.0.0.1:4723/wd/hub.返回session ID赋值给drive
add = driver.find_element_by_name('Add Contact')
#
add.click()
textFieldsList = driver.find_elements_by_class_name('android.widget.EditText')
textFieldsList[0].send_keys('ccc')
textFieldsList[1].send_keys('15684457157')
textFieldsList[2].send_keys('keingha@jig.com')
driver.swipe(100, 500, 100, 100, 2)
# driver.find_element_by_name('Save').click()
driver.quit()
print "finished"