# -*- coding:utf-8 -*-
# !/usr/bin/env python
import re
import scrapy
import time
from selenium import webdriver
from xm_xiecheng_clainhotel.items import XieChengItem
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
import mzgeohash
import requests

class XieChengSpider(scrapy.spiders.Spider):
    def __init__(self):
        pass

    name = "xcjd"  # 爬虫的名称
    allowed_domains = ["hotels.ctrip.com"]  # 允许的域名
    start_urls = [
        "http://hotels.ctrip.com/hotel/xiamen25#ctm_ref=ctr_hp_sb_lst"
    ]

    def parse(self, response):
        driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
        driver.get(response.url)
        driver.maximize_window()
        handle = driver.current_window_handle
        # 关闭遮挡页
        try:
            close = driver.find_element_by_class_name("fl_wrap_close")
            close.click()
            time.sleep(1)
        except:
            pass

        brandclasses = driver.find_elements_by_xpath(".//div[@id='J_brandBanner']/a")
        for listnum in range(1,3):
            brandclasses[listnum].click()
            moreBrand = driver.find_elements_by_class_name("J_moreBrand")
            time.sleep(1)
            moreBrand[listnum-1].click()
            lenBrands = len(driver.find_elements_by_xpath(".//div[@class='filter_item_sub J_brandlist"+str(listnum-1)+" sta-all']/label"))
            for brand_i in range(7,lenBrands):
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_class_name("ctriplogo"))
                economicBrands = driver.find_elements_by_xpath(
                    ".//div[@class='filter_item_sub J_brandlist" + str(listnum - 1) + " sta-all']/label")
                try:
                    economicBrands[brand_i].click()
                except:
                    raw_input()
                time.sleep(2)
                page = 1
                sumh = 0
                while 1:
                    sumhotel = int(driver.find_element_by_id("lblAmount").text)
                    print sumhotel
                    try:
                        ui.WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, ".//div[@class='hotel_new_list']")))
                        hotels = driver.find_elements_by_xpath(".//div[@class='hotel_new_list']")
                    except TimeoutException:
                        print "--MAIN time out--"
                        raw_input()
                    i = 0
                    for hotel in hotels:
                        print sumh, sumhotel
                        sumh += 1
                        if sumh > sumhotel:
                            break
                        if i != 0:
                            driver.execute_script("arguments[0].scrollIntoView();", detail[i - 1])
                        item = XieChengItem()
                        item['brand'] = economicBrands[brand_i].text
                        item['title'] = hotel.find_element_by_xpath(".//h2[@class='hotel_name']/a").get_attribute(
                            "title")  # 标题
                        item['addr'] = \
                        hotel.find_element_by_xpath(".//p[@class='hotel_item_htladdress']").text.split(u'】')[-1].split(
                            u'，')[0].split(' ')[0].split('(')[0].split(u'（')[0]  # 地址
                        # print item['addr']
                        # 添加经纬度
                        base = u"http://api.map.baidu.com/geocoder/v2/?address=厦门市" + item[
                            'addr'] + "&output=json&ak=LGZ3SAK9jNMhBYgvC6tj4NkhRa09lUlj"
                        try:
                            map_response = requests.get(base)
                            answer = map_response.json()
                        except requests.exceptions.ConnectionError:
                            print "Error1: Max retries exceeded with url"
                            time.sleep(10)
                        item['lat'] = answer['result']['location']['lat']  # 纬度
                        item['lng'] = answer['result']['location']['lng']  # 经度
                        # 添加城市、区县、行政区代码、哈希代码等相关字段
                        base_contra = "http://api.map.baidu.com/geocoder/v2/?location=" + str(item['lat']) + "," \
                                      + str(item['lng']) + "&output=json&pois=1&ak=LGZ3SAK9jNMhBYgvC6tj4NkhRa09lUlj"
                        try:
                            map_response = requests.get(base_contra)
                            answer = map_response.json()
                        except requests.exceptions.ConnectionError:
                            print "Error2: Max retries exceeded with url"
                            time.sleep(10)
                        item['city'] = answer['result']['addressComponent']['city']  # 城市
                        item['district'] = answer['result']['addressComponent']['district']  # 区县
                        item['adcode'] = answer['result']['addressComponent']['adcode']  # 行政区编码
                        item['geohash'] = mzgeohash.encode((float(item['lng']), float(item['lat'])), length=6)[
                                          :5]  # 哈希编码
                        # print item['lat'],item['lng'],item['city'],item['district'],item['adcode'],item['geohash']
                        try:
                            item['type'] = \
                            hotel.find_element_by_xpath(".//span[@class='hotel_ico']/span[last()]").get_attribute(
                                "title").split(u'（')[0][-3:]  # 类型
                            if item['type'] == u'.5钻' or item['type'] == u'为1钻':
                                item['type'] = u'其他'
                        except:
                            item['type'] = u'其他'
                        try:
                            item['value'] = hotel.find_element_by_xpath(
                                ".//li[@class='hotel_item_judge no_comment ']/div[1]/a/span[@class='hotel_value']").text  # 客户评分
                            item['recommend'] = hotel.find_element_by_xpath(
                                ".//li[@class='hotel_item_judge no_comment ']/div[1]/a/span[@class='total_judgement_score']").text[
                                                :-5]  # 用户推荐百分比
                            item['comment_num'] = hotel.find_element_by_xpath(
                                ".//li[@class='hotel_item_judge no_comment ']/div[1]/a/span[@class='hotel_judgement']").text[
                                                  2:-5]  # 用户推荐数
                        except:
                            item['value'] = -1
                            item['recommend'] = -1
                            item['comment_num'] = -1
                        item['low_price'] = hotel.find_element_by_class_name("J_price_lowList").text  # 房间最低价
                        # 详情页
                        detail = driver.find_elements_by_xpath(".//h2[@class='hotel_name']/a")
                        detail[i].click()
                        handles = driver.window_handles
                        for newhandle in handles:
                            # 筛选新打开的窗口B
                            if newhandle != handle:
                                # 切换到新打开的窗口B
                                driver.switch_to_window(newhandle)
                        changebtn = driver.find_element_by_id("changeBtn")
                        driver.execute_script("arguments[0].scrollIntoView();", changebtn)
                        try:
                            meetingroom = driver.find_elements_by_class_name("icons-facility16")
                            if len(meetingroom) > 0:
                                item['meetingroom'] = 1
                            else:
                                item['meetingroom'] = 0
                        except:
                            item['meetingroom'] = 0
                        try:
                            sum = driver.find_element_by_xpath(".//div[@id='htlDes']/p").text.split(u'间房')[0].split()
                            item['sum'] = int(sum[-1])
                        except:
                            item['sum'] = -1
                        try:
                            ui.WebDriverWait(driver, 20).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, "btns_base22_main")))
                            sumroom = len(driver.find_elements_by_class_name("btns_base22_main"))
                            closeroom = len(driver.find_elements_by_class_name("btns_base22_dis"))
                            item['closerate'] = float(closeroom) / sumroom
                        except TimeoutException:
                            item['closerate'] = -1
                            print "--time out--"
                        i += 1
                        driver.close()
                        driver.switch_to_window(handle)
                        yield item
                    driver.switch_to_window(handle)

                    if sumh >= sumhotel:
                        break
                    try:
                        nextpage = driver.find_element_by_class_name('c_down')
                        nextpage.click()
                        page += 1
                    except:
                        break
                driver.execute_script("arguments[0].scrollIntoView();",driver.find_element_by_class_name("ctriplogo"))
                economicBrands = driver.find_elements_by_xpath(
                    ".//div[@class='filter_item_sub J_brandlist" + str(listnum - 1) + " sta-all']/label")
                try:
                    economicBrands[brand_i].click()
                except:
                    raw_input()
                time.sleep(1)