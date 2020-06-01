pyinstaller打包方法
pyinstaller barometer.spec
生成的打包文件需要添加的资源文件包括以下：
cfg.ini #配置文件，配置答题服务器域名，ip，端口
log.txt #日志文件
VersionInfo.xml #配置文件，控制软件版本更新
test.ico #应用图标
loginfirst.png #首次登陆时的背景图
