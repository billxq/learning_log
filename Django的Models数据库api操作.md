#### Django的Models数据库api操作

#### 进入shell

1. 在django项目目录下，输入`python manager.py shell`，进入交互式的shell，进行api操作

2. 导入post.models下的两个类

   ```
   from post.models import Comment, Topic
   from django.contrib.auth.models import User
   ```

#### 使用save方法创建实例

```
user = User.objects.get(username='root')
topic = Topic(title='first topic', content='This is the first topic!', user=user)
topic.save()
comment = Comment(title='first comment', content='very good', up=88, down=11, topic=topic)
comment.save()
```

#### 使用create方法创建实例

```
topic_2 = Topic.objects.create(title='second topic', content='This is the second topic!', user=user)
comment_2 = Comment(title='second comment', content='good', up=55, down=40, topic=topic_2)
topic_3 = Topic.objects.create(title='third topic', content='This is the third topic!', user=user)
comment_3 = Comment(title='third comment', content='bad', up=30, down=70, topic=topic_3)
```

#### 查询方法

1. 用get查询

   ```python
   Topic.objects.get(title='first topic') # 查询title是first topic的topic对象
   Topic.objects.get(id=1, title='first topic') # 多个条件的查询
   # ===================================================================================
   # 为了保证不抛出异常，可以这么操作
   try:
       topic = Topic.objects.get(id=1, title='first topic')
   except Topic.DoesNotExists:
       #do something
   except Topic.MultipulObjectsReturned:  # 返回多个结果
       #do something
       
   # ===================================================================================
   # 可以使用pk来代替id作为主键来查询
   Topic.objects.get(pk=1) 
   ```

2. 使用get_or_create查询

   这个方法的查询过程与get类似，都需要传递查询参数，但是与get不同的是，它返回的是一个tuple对象，即(object,created)。其中第一个元素是实例对象，第二个元素是布尔值，标识返回的实例对象是否是新创建的。

   ```python
   Topic.objects.get_or_create(title='new title', content='This is a new topic!', user=user) # 数据库没有这条数据，故而会新建一条数据。Manager提供的方法中不仅有get和get_or_create方法会返回单个Model实例，类似的还有first、last等方法，
   ```

#### 返回queryset的查询方法

> 当需要返回多条数据记录时，就需要用到QuerySet对象。可以简单地把QuerySet理解为Model集合，它可以包含一个、多个或者零个Model实例。Manager提供了很多接口可以返回QuerySet对象，常用的有all、filter、exclude、reverse、order_by等方法。

1. 使用all方法获得所有数据记录`Topic.objects.all()`

2. 使用reverse方法获取逆序数据记录
   reverse方法也会获取全量的数据记录，这一点与all方法是相同的。但是，它返回的数据记录的顺序与all方法相反，即逆序查询。

3. 使用order_by方法自定义排序规则
   无论是all方法还是reverse方法，它们返回数据结果的排序规则都会受到BaseModel的影响，假如需要自定义排序规则，就需要使用order_by方法了。
   order_by中可以指定多个排序字段，例如，对所有的Topic对象先按照title逆序排列，再按照created_time正序排列：

   ```
   Topic.objects.order_by('-title', 'created_time')
   ```

4. 使用filter方法过滤数据记录
   通常对数据表的检索都只会获取全量数据的一个子集，即使用WHERE子句过滤不符合条件的记录。filter方法完成的就是这样的功能，它会将传递的参数转换成WHERE子句实现过滤查询。在不传递任何参数的情况下，查询效果和all方法是一样的。

#### 使用delete方法删除Model实例

```python
comment = Comment.objects.all(id=1)
comment.delete()
```



