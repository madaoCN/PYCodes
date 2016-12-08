# -*-coding=utf-8
from selenium import webdriver
# 打开Firefox，selenium原生支持
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
# firefox_capabilities['binary'] = '/Users/raymondyee/bin/geckodriver'
# os.environ["PATH"] += ":/Users/liangxiansong/Desktop/geckodriver"
URL = "http://onlineclass.4i-test.com/web/my/teaching/material/question/bill/%s"

def openWindow(idArr):

    #初始化
    driverPath = '/Users/liangxiansong/Desktop/geckodriver'
    profile = webdriver.FirefoxProfile('/Users/liangxiansong/Library/Application Support/Firefox/Profiles/ta0bshzl.default')
    profile.set_preference('browser.link.open_newwindow',3)
    # driver = webdriver.Chrome(driverPath)
    driver = webdriver.Firefox(firefox_profile=profile)

    #打开页面
    driver.get(URL % idArr[0])
    for item in idArr[1:]:
        js='window.open("%s", target="_blank");' % (URL % item)
        driver.execute_script(js)


if __name__ == "__main__":
    # itemArr = [3070,
    #            3095,
    #            3110,
    #            3116,
    #            3123,
    #            3191,
    #            3192,3193,3104,
    #            3207,]
    itemArr = []
    for i in range(6200, 6230):
        itemArr.append(i)
    openWindow(itemArr)