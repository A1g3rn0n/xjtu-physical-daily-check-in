import logging
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from common.mail import send_email


# 全局变量 邮件配置
email_config = None
need_mail = False
smtp_server = None
sender_email = None
sender_password = None
receiver_email = None

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, '../physic_log.log')


logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def read_mail_config_from_json():
    """
    读取邮件配置文件
    :return: config
    """
    global email_config
    if email_config is None:
        try:
            # 读取配置文件，优先加载自定义的 myMail.json 文件
            if not os.path.exists(os.path.join(current_dir, 'myMail.json')):
                with open(os.path.join(current_dir, 'mail.json'), 'r') as f:
                    email_config = json.load(f)
            else:
                with open(os.path.join(current_dir, 'myMail.json'), 'r') as f:
                    email_config = json.load(f)

        except Exception as e:
            logging.error("No mail.json file found. Please check the file path.")
            logging.error(str(e))
            email_config = {}
    return email_config


def load_mail_config():
    """
    从配置文件中加载邮件配置
    :return:
    """
    json_config = read_mail_config_from_json()
    # 从配置文件中获取参数
    global need_mail, smtp_server, sender_email, sender_password, receiver_email
    try:
        need_mail = json_config['need_mail']
        if need_mail:
            smtp_server = json_config['smtp_server']
            sender_email = json_config['sender_email']
            sender_password = json_config['sender_password']
            receiver_email = json_config['receiver_email']
    except Exception as e:
        logging.error("Failed to load mail config")
        logging.error(str(e))


def init_browser():
    """
    初始化浏览器
    :return: driver
    """
    try:
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

    except Exception as e:
        logging.error("browser init failed")
        logging.error(str(e))
        driver = webdriver.Chrome()

    return driver


def config(driver, latitude, longitude):
    """
    通过执行JavaScript设置地理位置
    :param driver: 浏览器驱动
    :param latitude: 纬度
    :param longitude: 经度
    """
    try:
        # 通过执行JavaScript设置地理位置
        driver.execute_cdp_cmd("Browser.grantPermissions", {
            "origin": "https://ipahw.xjtu.edu.cn/pages/index/hdgl/hdgl_run",
            # 要访问的网站
            "permissions": ["geolocation"]
        })
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": 100
        })
        logging.info("browser configured")
    except Exception as e:
        logging.error("browser config failed")
        logging.error(str(e))


def login(driver, netid, password):
    """
    执行登录
    :param driver: 浏览器驱动
    :param netid: NetID
    :param password: 密码
    """
    try:
        driver.get('https://ipahw.xjtu.edu.cn/pages/tabbar/index')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//uni-view[text()="统一身份认证"]')))
        driver.find_element(By.XPATH, '//uni-view[text()="统一身份认证"]').click()

        if driver.current_url == "https://org.xjtu.edu.cn/openplatform/login.html":
            driver.implicitly_wait(0.5)
            # driver.find_element(By.CLASS_NAME, "username").send_keys(netid)
            driver.find_element(By.CLASS_NAME, "username").send_keys(netid)
            driver.implicitly_wait(0.5)
            driver.find_element(By.CLASS_NAME, "pwd").send_keys(password)
            driver.implicitly_wait(0.5)
            driver.find_element(By.ID, "account_login").click()

        logging.info("login success")
    except Exception as e:
        logging.error("login failed")
        logging.error(str(e))


def go_to_my_activity(driver):
    """
    进入我的活动
    :param driver:
    :return:
    """
    try:
        WebDriverWait(driver, 10, 0.5).until(EC.url_contains("ipahw.xjtu.edu.cn"))
        driver.get('https://ipahw.xjtu.edu.cn/pages/tabbar/index')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//uni-text/span[text()="我的活动"]')))
        driver.find_element(By.XPATH, '//uni-text/span[text()="我的活动"]').click()
        time.sleep(3)

    except Exception as e:
        logging.error("visit my activity failed")
        logging.error(str(e))


def sign_in(driver):
    """
    签到
    :param driver:
    """
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//uni-button[text()="签到"]')))
        driver.find_elements(By.XPATH, '//uni-button[text()="签到"]')[1].click()
        # 这里不可以注释 等几秒才可以点击签到 签到成功
        time.sleep(3)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//uni-button[text()="锻炼过程积分签到"]')))
        driver.find_element(By.XPATH, '//uni-button[text()="锻炼过程积分签到"]').click()

        logging.info("sign in success")

    except Exception as e:
        logging.error("sign in failed")
        logging.error(str(e))


def sign_out(driver):
    """
    签退
    :param driver:
    :return:
    """
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//uni-button[text()="签退"]')))
        driver.find_elements(By.XPATH, '//uni-button[text()="签退"]')[1].click()
        time.sleep(3)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//uni-button[text()="锻炼过程积分签退"]')))
        driver.find_element(By.XPATH, '//uni-button[text()="锻炼过程积分签退"]').click()
        time.sleep(3)
        logging.info("sign out success")

    except Exception as e:
        logging.error("sign out failed")
        logging.error(str(e))


def time_wait():
    """
    等待时间
    """

    # debug 暂停5s，控制台输出倒计时
    # for i in range(5):
    #     print(f"倒计时 {5 - i} 秒")
    #     time.sleep(1)

    # 随机31-35min后签退
    rand_time = 31 + 4 * random.random()
    time.sleep(rand_time * 60)


def main(netid, password, latitude=34.257116, longitude=108.652905):
    """
    主函数

    :param netid: NetID
    :param password: 密码
    :param latitude: 纬度
    :param longitude: 经度
    """

    load_mail_config()

    driver = init_browser()

    config(driver, latitude, longitude)

    login(driver, netid, password)

    go_to_my_activity(driver)

    # 解除注释
    sign_in(driver)

    time_wait()

    sign_out(driver)

    validate(driver)

    logging.info("browser closed")
    driver.quit()


def validate(driver):
    """
    验证打卡结果
    :param driver: 浏览器驱动
    :return:
    """

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//uni-view[text()="查看详情"]')))
        driver.find_elements(By.XPATH, '//uni-view[text()="查看详情"]')[1].click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//uni-text/span[text()="锻炼记录"]')))
        driver.find_element(By.XPATH, '//uni-text/span[text()="锻炼记录"]').click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//uni-view[text()="序号"]')))
        # 找到第一条锻炼记录
        score_element = driver.find_element(By.XPATH, (
            '//uni-view[contains(@class, "list_names") '
            'and text()="得分"]/following-sibling::uni-view'
        ))

        date_element = driver.find_elements(By.XPATH, (
            '//uni-view[contains(@class, "list_names") '
            'and text()="签到时间"]/following-sibling::uni-view'
        ))[0]

        # 截图路径
        screenshot_path = os.path.join(current_dir, '最新打卡详情截图.png')
        # 截图并保存为screenshot.png
        driver.save_screenshot(screenshot_path)

        # 检查"得分"元素的文本是否为"1" 且 格式化后的日期为今天
        if score_element.text == "1" and date_element.text.split(" ")[0] == time.strftime("%Y-%m-%d"):
            logging.info("日期：{} 打卡成功".format(date_element.text))
            if need_mail:
                send_email(smtp_server, sender_email, sender_password, receiver_email, '打卡成功',
                           '日期：{} 打卡成功'.format(date_element.text), screenshot_path)
        else:
            logging.info("日期：{} 打卡失败，请手动打卡".format(time.strftime("%Y-%m-%d %H:%M:%S")))
            if need_mail:
                send_email(smtp_server, sender_email, sender_password, receiver_email, '打卡失败',
                           '日期：{} 打卡失败，请手动打卡'.format(time.strftime("%Y-%m-%d")), screenshot_path)

        time.sleep(5)

    except Exception as e:
        logging.error("validate failed")
        logging.error(str(e))


if __name__ == "__main__":
    # 测试
    if not os.path.exists(os.path.join(current_dir, '../myProfile.json')):
        with open(os.path.join(current_dir, '../profile.json'), 'r') as f:
            profileConfig = json.load(f)
    else:
        with open(os.path.join(current_dir, '../myProfile.json'), 'r') as f:
            profileConfig = json.load(f)
    # 从配置文件中获取参数
    netid = profileConfig['netid']
    password = profileConfig['password']
    main(netid, password)
