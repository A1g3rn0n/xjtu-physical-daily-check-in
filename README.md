## XJTU体育每日打卡
暂时仅在windows环境下测试过
### 使用
1. 安装依赖
    ```shell
    pip install schedule selenium
    ```
2. 下载chrome驱动，解压后将`chromedriver.exe`放在`python.exe`同目录下
    - [chromedriver最新版本下载地址](https://getwebdriver.com/chromedriver/)
3. 在`profile.json`中填写你的统一认证账号和密码与打卡经纬度。示例中使用4号楼南篮球场的经纬度和7点打卡时间
    ```json
    {
        "username": "学号",
        "password": "密码",
        "latitude": 34.257116,
        "longitude": 108.652905,
        "target_time": "07:00"
    }
    ```
4. 运行`daily.py` 
   ```shell
    python daily.py
   ```

### 目录结构
```
│  daily.py # 调用simulate_with_chromedriver.py模拟打卡，每日定时执行
│  physic_log.log # 日志文件
│  profile.json # 配置文件
│  README.md 
└─common 
      simulate_with_chromedriver.py # 模拟打卡流程
```

### todo
- 可能导致程序异常退出
- [ ] 验证打卡是否成功的实现欠考虑
- [ ] 并不确定 是否每天都只执行**一次**打卡
- [ ] 自主锻炼未开放时间段 执行打卡任务会异常退出

- 优化
- [ ] 支持Linux 无窗口模式
- [ ] 有效范围内随机经纬度
- [ ] 随机打卡时间
- [ ] 邮件通知
