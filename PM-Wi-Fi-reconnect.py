#coding=utf-8
import unittest
import time
import os
import subprocess
import xlwt
import codecs



class AppTest(unittest.TestCase):

    def setUp(self):
        self.reconnect_time = 100  #重连时间设置
        self.mobiledate = '03-19'   #手机日期设置
        self.excel_output_index = 'C:\\Users\\77465\\Desktop\\pm45_wifireconnect.xls' #excel表格输出路径设置

    def test_wifireconnect(self):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        sheet.write(0, 0, '开机时间')
        sheet.write(0, 1, 'Wi-Fi重连时间')
        sheet.write(0, 2, '耗时(s)')
        for i in range(0,self.reconnect_time):
            cmd = "adb reboot"
            os.popen(cmd)
            print("开始重启")
            time.sleep(15)
            filename = "D:\\reconnectlog\\reconnect%i.txt" % i  # 日志文件名添加当前时间
            logcat_file = open(filename, 'w')
            logcmd = "adb logcat -v time"
            Poplog = subprocess.Popen(logcmd, stdout=logcat_file, stderr=subprocess.PIPE)
            print("开始抓取log")
            time.sleep(60)
            logcat_file.close()
            Poplog.terminate()
            print("第%i次重启完成" % i)

        for i in range(0,self.reconnect_time):
            print ("第%i个Log正在处理" % i)
            filename = 'D:\\reconnectlog\\reconnect%i.txt' % i
            fd = codecs.open(filename,'rb')
            fdd = fd.read()
            begin_location = fdd.find(b'03-19')
            if begin_location == -1:
                print("ERROR:Wrong date!")
            else:
                begintime = fdd[(begin_location + 6):(begin_location +18)]
                endtime_location = fdd.find(b'ASSOCIATING -> ASSOCIATED')
                if endtime_location == -1:
                    print("Haven't reconnect  in 60s,you can check the D:\\reconnectlog\\reconnect%i.txt" %i)
                else:
                    endtime = fdd[(endtime_location + 32):(endtime_location + 44)]
                    sheet.write(i + 1, 0, str(begintime,'gbk'))
                    sheet.write(i + 1, 1, str(endtime,'gbk'))
                    begin_min = int(begintime.split(b":")[1])
                    begin_sec = float(begintime.split(b":")[2])
                    end_min = int(endtime.split(b":")[1])
                    end_sec = float(endtime.split(b":")[2])

                    min_def = 0
                    if begin_min != end_min:
                        min_def = end_min - begin_min

                    duringtime = end_sec + min_def * 60 - begin_sec
                    sheet.write(i + 1, 2, duringtime)
        wbk.save('C:\\Users\\77465\\Desktop\\pm45_wifireconnect.xls')


    def tearDown(self):
       print("finished")

if __name__ == '__main__':
    unittest.main()


