import logging
import schedule
import time
import os
from common.simulate_with_chromedriver import main
import json
# import argparse

# # 创建解析器
# parser = argparse.ArgumentParser(description='Process some integers.')
# # 添加参数
# parser.add_argument('--needWindow', type=int, help='是否需要显示浏览器窗口')
# # 解析参数
# args = parser.parse_args()
# # 使用参数
# print(args.argument)

# 读取配置文件
if not os.path.exists('myProfile.json'):
    with open('profile.json', 'r') as f:
        config = json.load(f)
else:
    with open('myProfile.json', 'r') as f:
        config = json.load(f)
# 从配置文件中获取参数
netid = config['netid']
password = config['password']
latitude = config['latitude']
longitude = config['longitude']


# 设置日志记录
logging.basicConfig(filename='physic_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def log_message(message):
    logging.info(message)


def run_task_once():
    # 记录任务执行时间
    log_message("Task is starting.")
    main(netid, password, latitude, longitude)
    log_message("Task completed.")


if __name__ == "__main__":
    # 设置目标时间
    target_time = config['target_time']
    # target_time = "16:33"

    # 安排任务并启动调度器
    schedule.every().day.at(target_time).do(run_task_once)

    while True:
        schedule.run_pending()
        time.sleep(1)
