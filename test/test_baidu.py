#!/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
from time import sleep
import time
import unittest
from selenium.webdriver.common.by import By
from utils.config import Config,BASE_PATH,DATA_PATH,REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner_PY3 import HTMLTestRunner
from utils.mail import Email


class TestBaidu(unittest.TestCase):
    '''百度搜索测试'''
    URL = Config().get('URL')
    excel = DATA_PATH + '/data.xls'
    driver_path = (BASE_PATH + '\drivers\chromedriver.exe')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')
    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')

    def sub_setUp(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.get(self.URL)
        sleep(2)

    def sub_tearDown(self):
        self.driver.quit()

    def test_search(self):
        '''内容搜索'''
        datas = ExcelReader(self.excel).data
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                self.driver.find_element(*self.locator_kw).send_keys(d['selenium'])
                self.driver.find_element(*self.locator_su).click()
                sleep(2)
                links = self.driver.find_elements(*self.locator_result)
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()

    # def test_search_02(self):
    #     self.driver.find_element(*self.locator_kw).clear()
    #     self.driver.find_element(*self.locator_kw).send_keys("admin")
    #     self.driver.find_element(*self.locator_kw).submit()
    #     sleep(2)
    #     links = self.driver.find_elements(*self.locator_result)
    #     for link in links:
    #         logger.info(link.text)


if __name__ == '__main__':
    time = time.strftime("%Y-%m-%d %H_%M_%S")
    report = REPORT_PATH + "\\" + time + 'report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='自动化测试', description='测试报告')
        runner.run(TestBaidu('test_search'))

    e = Email(title="测试报告",
              message="最新的报告",
              sender='18511069163@163.com',
              receiver='16601184986@163.com',
              password='qwer123456',
              server='smtp.163.com'
              )
    e.send()



