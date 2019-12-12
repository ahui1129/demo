import pytest
import yaml
from appium import webdriver
from selenium.webdriver.common.by import By

# 我的
from selenium.webdriver.support.wait import WebDriverWait

tab_mine = By.ID, 'com.gonglf.program:id/tab_mine'
# 请登录
user_name = By.ID, 'com.gonglf.program:id/user_name'
# 立即登录
button_login_now = By.ID, 'com.gonglf.program:id/button_login_now'
# 输入手机号
login_phone = By.ID, 'com.gonglf.program:id/login_phone'
# 输入密码
login_password = By.ID, 'com.gonglf.program:id/login_password'
# 是否登录成功
login_assert = By.XPATH, "//*[contains(@text,'请登录')]"
# 设置按钮
setting_button = By.ID, 'com.gonglf.program:id/iv_set'
# 退出按钮
login_out = By.XPATH, "//*[contains(@text,'退出')]"
# 退出确认
login_out_mow = By.XPATH, "//*[contains(@text,'确认')]"


def read_login_data(test):
    with open('login_data.yml', 'r') as f:
        return yaml.safe_load(f)[test]


class Test:
    def setup(self):
        desired_caps = {
            # 设备信息
            'platformName': 'Android',
            'platformVersion': '5.1',
            'deviceName': 'Y5TWYS8P99999999',
            # app信息
            'appPackage': 'com.gonglf.program',  # 包名
            'appActivity': '.activity.WelcomeActivity ',  # 启动名
            # 中文
            'unicodeKeyboard': True,
            'resetKeyboard': True
        }

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    @pytest.mark.parametrize('condition', read_login_data('user_name'))
    def test_login(self, condition):
        self.find_element(tab_mine).click()
        self.find_element(user_name).click()
        # self.find_element(button_login_now).click()
        self.find_element(login_phone).send_keys(condition)
        self.find_element(login_password).send_keys('123456')
        self.find_element(button_login_now).click()
        if not self.find_element(login_assert) and self.find_element(setting_button):
            print('进入到if')
            self.find_element(setting_button).click()
            self.find_element(login_out).click()
            self.find_element(button_login_now).click()

        self.driver.close()

    def find_element(self, loc):
        by = loc[0]
        value = loc[1]
        return WebDriverWait(self.driver, 10, 1).until(lambda x: x.find_element(by, value))


