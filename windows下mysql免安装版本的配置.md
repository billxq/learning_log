### windows下mysql免安装版本的配置

1. 在mysql根目录下创建mysql的配置文件my.ini，并输入一下内容，注意要用asni编码的形式保存

   ```reStructuredText
   [mysqld]
   basedir ="D:\mysql\mysql-8.0.12-winx64"       # 根据自己的情况自行更改
   datadir ="D:\mysql\mysql-8.0.12-winx64\data"
   port=3306
   server_id =10
   character-set-server=gbk
   character_set_filesystem=gbk
   [client]
   port=3306
   default-character-set=gbk
   [mysqld_safe]
   timezone="CST"
   [mysql]
   default-character-set=utf8
   
   ```

2. 配置环境变量，把根目录下的bin文件夹的路径输入到系统的环境变量中。
3. 配置mysql
   1.  进入mysql下的bin目录，执行`mysqld --install`, 会提示安装成功，Service successfully installed.，然后进入下一步。
   2. `mysqld --initialize --user=root --console` 初始化，成功后会在控制台的最后出现一串复杂的字符串，那个时root的登陆密码
   3. 启动mysql `net start msyql`
   4. `mysql -u root -p` 输入第2步记录的字符串，进入mysql命令行
   5. 可以对登陆密码进行修改`alter user user() identified by 'newpassword';`  