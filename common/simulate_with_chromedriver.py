import logging
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from mail import send_email


# 读取配置文件，优先加载自定义的 myMail.json 文件
if not os.path.exists('myMail.json'):
    with open('mail.json', 'r') as f:
        config = json.load(f)
else:
    with open('myMail.json', 'r') as f:
        config = json.load(f)

# 从配置文件中获取参数
need_mail = config['need_mail']
if need_mail:
    smtp_server = config['smtp_server']
    sender_email = config['sender_email']
    sender_password = config['sender_password']
    receiver_email = config['receiver_email']


# 设置日志记录格式
logging.basicConfig(filename='../physic_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 设置浏览器启用地理位置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 1  # 允许地理位置
})

# 设置浏览器无头模式，即不显示浏览器窗口
chrome_options.add_argument("--headless")
# 设置浏览器窗口大小，避免部分元素无法获取和点击
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)


def config(latitude, longitude):
    """
    通过执行JavaScript设置地理位置

    :param latitude: 纬度
    :param longitude: 经度
    """

    # 通过执行JavaScript设置地理位置
    driver.execute_cdp_cmd("Browser.grantPermissions", {
        "origin": "https://ipahw.xjtu.edu.cn/pages/index/hdgl/hdgl_run?courseType=7&signType=1&activityAddress=&courseInfoId=1759468647346147329",
        # 要访问的网站
        "permissions": ["geolocation"]
    })
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })
    logging.info("browser configured")


def login(netid, password):
    """
    执行登录

    :param netid: NetID
    :param password: 密码
    """

    driver.get('https://ipahw.xjtu.edu.cn/pages/tabbar/index')

    driver.implicitly_wait(5)
    element = driver.find_element_by_css_selector('.w-360.h-90.u-flex.u-col-center.u-row-center').click()

    if driver.current_url == "https://org.xjtu.edu.cn/openplatform/login.html":
        driver.implicitly_wait(0.5)
        driver.find_element_by_class_name("username").send_keys(netid)
        driver.implicitly_wait(0.5)
        driver.find_element_by_class_name("pwd").send_keys(password)
        driver.implicitly_wait(0.5)
        driver.find_element_by_id("account_login").click()

    logging.info("login success")


def go_to_my_activity():

    element = WebDriverWait(driver, 10, 0.5).until(EC.url_contains("ipahw.xjtu.edu.cn"))
    driver.get('https://ipahw.xjtu.edu.cn/pages/tabbar/index')

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//uni-text/span[text()="我的活动"]')))
    driver.find_element_by_xpath('//uni-text/span[text()="我的活动"]').click()
    time.sleep(3)


def sign_in():
    """
    签到
    """

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//uni-button[text()="签到"]')))
    driver.find_elements_by_xpath('//uni-button[text()="签到"]')[1].click()
    # 这里不可以注释 等几秒才可以点击签到 签到成功
    time.sleep(3)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//uni-button[text()="锻炼过程积分签到"]')))
    driver.find_element_by_xpath('//uni-button[text()="锻炼过程积分签到"]').click()

    logging.info("sign in success")


def sign_out():
    """
    签退
    :return:
    """
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//uni-button[text()="签退"]')))
    driver.find_elements_by_xpath('//uni-button[text()="签退"]')[1].click()
    time.sleep(3)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//uni-button[text()="锻炼过程积分签退"]')))
    driver.find_element_by_xpath('//uni-button[text()="锻炼过程积分签退"]').click()
    time.sleep(3)
    logging.info("sign out success")


def time_wait():
    """
    等待时间
    """

    # debug 暂停10s，控制台输出倒计时
    # for i in range(5):
    #     print(f"倒计时 {5 - i} 秒")
    #     time.sleep(1)

    # 随机31-44min后签退
    rand_time = 31 + 13 * random.random()
    time.sleep(rand_time * 60)


def main(netid, password, latitude=34.123456, longitude=108.123456):
    """
    主函数

    :param netid: NetID
    :param password: 密码
    :param latitude: 纬度
    :param longitude: 经度
    """

    config(latitude, longitude)

    login(netid, password)

    go_to_my_activity()

    sign_in()

    time_wait()

    sign_out()

    validate()

    logging.info("browser closed")
    driver.quit()


def validate():
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//uni-view[text()="查看详情"]')))
    driver.find_elements_by_xpath('//uni-view[text()="查看详情"]')[1].click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//uni-text/span[text()="锻炼记录"]')))
    driver.find_element_by_xpath('//uni-text/span[text()="锻炼记录"]').click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//uni-view[text()="序号"]')))
    # 找到第一条锻炼记录
    score_element = driver.find_element_by_xpath(
        '//uni-view[contains(@class, "list_names") '
        'and text()="得分"]/following-sibling::uni-view'
    )

    date_element = driver.find_elements_by_xpath(
        '//uni-view[contains(@class, "list_names") '
        'and text()="签到时间"]/following-sibling::uni-view'
    )[0]

    # 截图并保存为screenshot.png
    driver.save_screenshot('最新打卡详情截图.png')

    # 检查"得分"元素的文本是否为"1" 且 格式化后的日期为今天
    if score_element.text == "1" and date_element.text.split(" ")[0] == time.strftime("%Y-%m-%d"):
        logging.info("日期：{} 打卡成功".format(date_element.text))
        if need_mail:
            send_email(smtp_server, sender_email, sender_password, receiver_email, '打卡成功',
                     '日期：{} 打卡成功'.format(date_element.text), '最新打卡详情截图.png')
    else:
        logging.info("日期：{} 打卡失败，请手动打卡".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        if need_mail:
            send_email(smtp_server, sender_email, sender_password, receiver_email, '打卡失败',
                     '日期：{} 打卡失败，请手动打卡'.format(time.strftime("%Y-%m-%d")), '最新打卡详情截图.png')

    time.sleep(10)


if __name__ == "__main__":
    # 测试
    if not os.path.exists('../myProfile.json'):
        with open('../profile.json', 'r') as f:
            profileConfig = json.load(f)
    else:
        with open('../myProfile.json', 'r') as f:
            profileConfig = json.load(f)
    # 从配置文件中获取参数
    netid = profileConfig['netid']
    password = profileConfig['password']
    main(netid, password)

