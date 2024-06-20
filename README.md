## XJTU体育每日打卡
暂时仅在windows环境下测试过
### 使用
1. 安装依赖
    ```shell
    pip install schedule selenium
    ```
2. 下载chrome驱动，解压后将`chromedriver.exe`放在`python.exe`同目录下
    - [chromedriver最新版本下载地址](https://getwebdriver.com/chromedriver/)
3. 在`profile.json`中填写你的统一认证账号和密码与打卡经纬度。示例中使用4号楼南篮球场的经纬度和7点打卡时间(24小时制，请保证有4位数字。7:00而不是07:00可能会异常)
    ```json
    {
        "username": "学号",
        "password": "密码",
        "latitude": 34.257116,
        "longitude": 108.652905,
        "target_time": "07:00"
    }
    ```
4. 如果需要启用邮件通知服务，请在`commom/mail.json`中填写你的邮箱信息.
    - need_mail: 是否启用邮件通知 `true` or `false`
    - smtp_server: 邮箱SMTP服务器
    - sender_email: 发送邮件的邮箱
    - sender_password: 发送邮件的邮箱授权码，请在邮箱设置中开启SMTP服务获取
    - receiver_email: 接收邮件的邮箱
    ```json
    {
        "need_mail": true,
        "smtp_server": "smtp.example.com",
        "sender_email": "your_email@example.com",
        "sender_password": "Your STMP auth code",
        "receiver_email": "Receiver email"
    }
    ```
   
5. 运行`daily.py`，默认是无浏览器窗口模式
   ```shell
    python daily.py
   ```

### 目录结构
```
│  daily.py # 调用simulate_with_chromedriver.py模拟打卡，每日定时执行
│  physic_log.log # 日志文件
│  profile.json # 个人信息配置文件
│  README.md 
└─common 
   │  mail.json # 邮件配置文件
   │  mail.py # 邮件通知
   └─ simulate_with_chromedriver.py # 模拟打卡
```

### todo
- 可能导致程序异常退出
- [ ] 验证打卡是否成功的实现，因为签到时 a. 今日以获得分数 b. 距指定位置超过100m 会导致页面不跳转，
找不到元素抛出异常。 后面会改成直接访问 详情-锻炼记录 页 
- [ ] 并不确定 是否每天都执行且只执行**一次**签到签退任务
- [ ] 本学期自主锻炼未开放的时间段内 执行打卡任务会异常退出
- [x] 终端运行可能存在Import和读取文件路径错误的问题
- [ ] 在`simulate_with_chromedriver.py`中 签到 签退 和 查看详情 是直接通过`[1]`定位然后点击的，
如果我的活动中第二个标签并不是自主锻炼， 可能会出现异常退出


- 优化
- [ ] **我请问了，有没有不用selenium，直接request发请求获得sso验证的方法呢？**
现在是在尝试优化项目结构，解耦与减少selenium的使用
- [x] 无窗口模式
- [ ] 其他系统支持
- [ ] 验证今日自主锻炼未得分时 重试签到签退
- [ ] 有效范围内随机经纬度
- [ ] 随机打卡时间
- [x] 邮件通知
