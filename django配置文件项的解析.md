### settings.py 的配置项解析 

#### 配置项解析

1. BASE_DIR : 定义了my_bbs所在的完整路径，怎么来的？

   ```text
   __file__是值当前文件的位置；
   os.path.abspath(__file__)返回当前文件的绝对路径
   os.path.dirname(os.path.abspath(__file__))得到当前文件所在的目录；
   os.path.dirname(os.path.dirname(os.path.abspath(__file__)))返回目录的上一级，对应于当前的项目。
   ```

2. SECRET_KEY: 这个变量本质上是一个加密盐，用于对各种需要加密的数据做Hash处理，例如密码重置、表单提交、session数据等。

3. DEUBG: 通常在开发环境中将它设置为True，项目在运行的过程中会暴露出一些出错信息和配置信息以方便调试。但是在线上环境中应该修改其为False，避免敏感信息泄露。

4. ALLOWED_HOSTS: 用于配置可以访问当前站点的域名，当DEBUG配置为False时，它是一个必填项，设置ALLOWED_HOSTS=['*']允许所有的域名访问。

5.  INSTALLED_APPS: 这个参数配置的是当前项目需要加载的App包路径列表。Django默认会把admin（管理后台）、auth（权限系统）、sessions（会话系统）加入进去，可以根据项目的需要对其增加或删除配置。

6. MIDDLEWARE: 当前项目中需要加载的中间件列表配置。与INSTALLED_APPS变量类似，Django也会默认加入一些中间件，例如用于处理会话的SessionMiddleware、用于处理授权验证的AuthenticationMiddleware等。同样，可以根据项目的需要对其增加或删除配置。

7. ROOT_URLCONF: 这个变量标记的是当前项目的根URL配置，是Django路由系统的入口点。

8. TEMPLATES: 这是一个列表变量，用于项目的模板配置，列表中的每一个元素都是一个字典，每个字典代表一个模板引擎。Django默认会配置自带的DTL（DjangoTemplates）模板引擎。

9. WSGI_APPLICATION: Django的内置服务器将使用的WSGI应用程序对象的完整Python路径。

10. DATABASES: 这是一个字典变量，标识项目的数据库配置，Django默认会使用自带的数据库sqlite3，同时，Django项目支持多数据库配置，如果需要，可以配置多个键值对。在实际的项目开发中会使用功能更强大的数据库（如MySQL），所以，这个变量通常会被改动。

11. AUTH_PASSWORD_VALIDATORS:  Django默认提供了一些支持插拔的密码验证器，且可以一次性配置多个。其主要目的是避免直接通过用户的弱密码配置申请。

12. LANGUAGE_CODE和TIME_ZONE: 这两个变量分别代表项目的语言环境和时区。

13. USE_I18N和USE_L10N: 
    Web服务搭建完成之后，可以面向不同国家的用户提供服务，这就要求应用支持国际化和本地化。这两个布尔类型的变量标识当前的项目是否需要开启国际化和本地化功能。
    I18N是国际化的意思，名字的由来是“国际化”的英文单词Internationalization开头和结尾的字母分别是I和N，且I和N的中间有18个字母，简称I18N。
    L10N是本地化的意思，名字的由来是“本地化”的英文单词Localization开头和结尾的字母分别是L和N，且L和N的中间有10个字母，简称L10N。

14. USE_TZ:  标识对于时区的处理，如果设置为True，不论TIME_ZONE设置的是什么，存储到数据库中的时间都是UTC时间。

15. STATIC_URL:  用于标记当前项目中静态资源的存放位置。

16. STATICFILES_DIRS: 静态资源的存储目录



#### 修改项目的默认配置

1. 配置语言环境和时区

   ```text
   LANGUAGE_CODE = 'zh-Hans'  # 默认语言环境设置成中文简体
   TIME_ZONE = 'Asia/Shanghai'  # 默认时区设置成上海
   USE_TZ= False  # 设置成对时区不敏感，这样就不用特殊处理数据库中的时间了
   
   ```

2.  配置开发数据库

   默认自带的是sqlite3，不适合做项目的数据库，所以可以用mysql数据库替代，修改DATABASES的配置：

   ```python
   DATABASES = {
   	'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'django_bbs', # 数据库名
           'USER': 'work',  # 数据库用户
           'PASSWORD': 'Djangobbs', # 该用户指定的密码
           'HOST': '127.0.0.1', # 数据库地址
           'PORT': '3306',  # mysql服务监听端口
       }
   }
   ```

   *由于MySQLdb不支持python3， 所以需要安装mysqlclient，因此在虚拟环境中执行命令： `pip install mysqlclient` ，安装完成后，可以在虚拟环境中尝试导入mysqldb，import MySQLdb, 如果没有出错，代表成功了*   

#### 初始化项目环境

1. INSTALLED_APPS中应用的数据库迁移 `python manage.py makemigrates && python manage.py migrate` 

2. 创建超级用户登陆的管理后台 `python manage.py createsuperuser` 用于创建超级用户，创建完成后，可以登陆http://127.0.0.1:8000/admin/  进行登陆管理。

3. 给bbs项目创建应用

   `python manage.py startapp post`  

4. python项目的requirements文件，需要重建当前项目环境的时候，可以执行下面的命令：

   `pip isntall -r requirements.txt`

5. 将项目装载到IDE中

   1. 打开pycharm

   2. 给当前项目选择配套的虚拟环境

      （1）打开Preferences，找到项目设置，对于my_bbs项目即为Project:my_bbs。
      （2）Add Project Interpreter，即添加虚拟环境，需要将之前创建的bbs_python37添加进来，选择bbs_python37/bin/python3.7即可。
      （3）最后，选择刚刚添加的虚拟环境。

      

