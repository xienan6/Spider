# -*- coding:utf-8 -*-
# !/usr/bin/env python
import re
import scrapy
import time
from selenium import webdriver
from xm_qunar_hotel.items import qunarItem
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
import mzgeohash
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image,ImageEnhance
import datetime

class qunarSpider(scrapy.spiders.Spider):
    def __init__(self):
        pass

    name = "qnjd"  # 爬虫的名称
    allowed_domains = ["hotel.qunar.com"]  # 允许的域名
    start_urls = [
        "https://user.qunar.com/passport/login.jsp?ret=http%3A%2F%2Fhotel.qunar.com%2Fcity%2Fxiamen%2F%23%26cityurl%3Dxiamen%26from%3DqunarHotel"
    ]

    def parse(self, response):
        # # 伪装测试
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
        driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
        driver.get(response.url)
        driver.maximize_window()
        handle = driver.current_window_handle
        driver.find_elements_by_class_name("textbox_focus")[0].send_keys("18515693080")
        driver.find_elements_by_class_name("textbox")[1].send_keys("czm123456")
        try:
            driver.find_element_by_class_name("pwd-login").click()
        except:
            pass
        # # 识别验证码
        # vcode_xy = driver.find_element_by_id("vcodeImg").location
        # vcode_size = driver.find_element_by_id("vcodeImg").size
        # driver.get_screenshot_as_file('fullscreen.png')  # 比较好理解
        # im = Image.open('fullscreen.png')
        # box = (vcode_xy['x'], vcode_xy['y'], vcode_xy['x'] + vcode_size['width'], vcode_xy['y'] + vcode_size['height'])
        # region = im.crop(box)
        # region.save("vcode.png")
        # im = Image.open("vcode.png")
        # imgry = im.convert('L')  # 图像加强，二值化
        # sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
        # sharp_img = sharpness.enhance(2.0)
        # sharp_img.save("vcode2.png")
        # image = Image.open("vcode2.png")

        print u"输入验证码后回车"
        raw_input()
        page = 1
        # 设置从第几页开始
        start_page = 1
        while 1:
            if datetime.datetime.now().hour == 16 and datetime.datetime.now().minute == 30:
                while 1:
                    try:
                        ui.WebDriverWait(driver, 30).until(
                            EC.visibility_of_element_located((By.XPATH, ".//div[@class='item_hotel_info']")))
                        hotels = driver.find_elements_by_xpath(".//div[@class='item_hotel_info']")
                    except TimeoutException:
                        print "--MAIN time out--"
                        raw_input()
                    i = 0
                    if start_page > page:
                        detail = driver.find_elements_by_xpath(".//span[@class='hotel_item']/a[1]")
                        driver.execute_script("arguments[0].scrollIntoView();", detail[-1])
                        time.sleep(1)
                        detail = driver.find_elements_by_xpath(".//span[@class='hotel_item']/a[1]")
                        driver.execute_script("arguments[0].scrollIntoView();", detail[-1])
                        hotels = []
                        # js修改源码跳转
                        driver.execute_script(
                            "document.getElementsByClassName('num icon-tag')[0].setAttribute('data-page'," + str(
                                start_page) + ");")
                        page = start_page
                    for hotel in hotels:
                        if i != 0:
                            driver.execute_script("arguments[0].scrollIntoView();", detail[i - 1])
                        item = qunarItem()
                        item['title'] = hotel.find_element_by_xpath(".//span[@class='hotel_item']/a").text  # 标题
                        item['addr'] = \
                        hotel.find_element_by_xpath(".//p[@class='adress']/span/em").text.strip(u'，').strip().split(
                            u'，')[0]  # 地址
                        # 添加经纬度
                        base = u"http://api.map.baidu.com/geocoder/v2/?address=厦门" + item[
                            'addr'] + "&output=json&ak=LGZ3SAK9jNMhBYgvC6tj4NkhRa09lUlj"
                        try:
                            map_response = requests.get(base)
                            answer = map_response.json()
                        except requests.exceptions.ConnectionError:
                            print "Error1: Max retries exceeded with url"
                            time.sleep(10)
                        isyield = True
                        try:
                            item['lat'] = answer['result']['location']['lat']  # 纬度
                            item['lng'] = answer['result']['location']['lng']  # 经度
                        except:
                            item['lat'] = 0
                            item['lng'] = 0
                            isyield = False
                        # 添加城市、区县、行政区代码、哈希代码等相关字段
                        base_contra = "http://api.map.baidu.com/geocoder/v2/?location=" + str(item['lat']) + "," + str(
                            item['lng']) + "&output=json&pois=1&ak=LGZ3SAK9jNMhBYgvC6tj4NkhRa09lUlj"
                        try:
                            map_response = requests.get(base_contra)
                            answer = map_response.json()
                        except requests.exceptions.ConnectionError:
                            print "Error2: Max retries exceeded with url"
                            time.sleep(10)
                        item['city'] = answer['result']['addressComponent']['city']  # 城市
                        item['district'] = answer['result']['addressComponent']['district']  # 区县
                        item['adcode'] = answer['result']['addressComponent']['adcode']  # 行政区编码
                        item['geohash'] = mzgeohash.encode((float(item['lng']), float(item['lat'])), length=6)  # 哈希编码
                        item['recommend'] = -1
                        item['meetingroom'] = 2
                        item['sum'] = -1
                        # print item['lat'],item['lng'],item['city'],item['district'],item['adcode'],item['geohash']
                        try:
                            item['type'] = hotel.find_element_by_xpath(".//em[@class='dangci']").text  # 类型
                        except:
                            item['type'] = u"其他"
                        # 详情页
                        detail = driver.find_elements_by_xpath(".//span[@class='hotel_item']/a[1]")
                        try:
                            if len(hotel.find_elements_by_class_name("icon-sell")) > 0:
                                raise Exception
                            item['low_price'] = hotel.find_element_by_xpath(
                                ".//div[@class='js_list_price']/p/a/b").text  # 房间最低价
                            try:
                                item['comment_num'] = hotel.find_element_by_xpath(
                                    ".//p[@class='user_comment']/a/cite").text  # 评论数
                                item['value'] = hotel.find_element_by_xpath(".//p[@class='score']/a/b").text  # 评分
                            except:
                                item['comment_num'] = -1
                                item['value'] = -1
                            # 点进去

                            detail[i].click()
                            handles = driver.window_handles
                            for newhandle in handles:
                                # 筛选新打开的窗口B
                                if newhandle != handle:
                                    # 切换到新打开的窗口B
                                    driver.switch_to_window(newhandle)
                            try:
                                ui.WebDriverWait(driver, 20).until(
                                    EC.visibility_of_element_located((By.CLASS_NAME, "btn-book")))
                                closeroom = len(driver.find_elements_by_class_name("btn-book-ct"))
                                sumroom = len(driver.find_elements_by_class_name("btn-book"))
                                # print closeroom,sumroom
                                item['closerate'] = float(closeroom) / sumroom
                            except TimeoutException:
                                item['closerate'] = -1
                                print "--time out--"
                            driver.close()
                        except:
                            item['low_price'] = -1
                            item['value'] = -1
                            item['comment_num'] = -1
                            item['type'] = u"其他"
                            item['closerate'] = -1
                        # print item['low_price'],item['value'],item['comment_num'],item['type']
                        driver.switch_to_window(handle)
                        if isyield == True:
                            yield item
                        i += 1
                        if i == 15:
                            hotels += (driver.find_elements_by_xpath(".//div[@class='item_hotel_info']")[i:])
                        try:
                            print "Page %s , %s" % (page, item['title'])
                        except:
                            pass
                    driver.switch_to_window(handle)
                    try:
                        nextpage = driver.find_elements_by_class_name('icon-tag')
                        nextpage[-1].click()
                        page += 1
                    except:
                        break
            else:
                time.sleep(1)