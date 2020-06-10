### Model相关的概念与方法

#### model的组成部分

1. django.db.models.Model

   通过类之间的继承，Django主要对自定义的Model添加了两个属性。

   （1）id：Django规定，每一个Model必须有且仅有一个Field字段的primary_key属性设置为True，即必须要有主键。通常，在自定义Model的时候，不需要关注主键字段，基类会自动添加一个auto-incrementing id作为主键。

   （2）objects：它是Manager（django.db.models.Manager）类的实例，被称为查询管理器，是数据库查询的入口。每个Django Model都至少有一个Manager实例，可以通过自定义创建Manager以实现对数据库的定制访问，但通常是没有必要的，后面的内容会看到默认Manager的强大功能。

2. Meta内部类声明元数据

   Meta是一个类容器，Django会将容器中的元数据选项定义附加到Model中。常见的元数据定义有：数据表名称、是否是抽象类、权限定义、索引定义等。Meta定义的元数据相当于Model的配置信息，可以直接在shell环境中打印出来，例如，对于Topic的定义，可以使用如下方法查看:

   ```text
   >>> from post.models import Topic
   >>> Topic.Meta
   ```

3. \_\_str\_\_方法

   \_\_str\_\_方法是Python中的“魔术”方法，它是为print这样的打印函数设计的。如果没有这个方法定义，打印对象会显示对象的内存地址，但是，这样的显示方式不够友好，且不利于调试。Python的这个特性同样对Django的Model实例生效，例如针对Topic的实例直接打印的话，会显示id和title的前20个字符。不仅如此，将来管理后台也可以看到\_\_str\_\_方法发挥的作用，它会将函数的返回值作为对象的显示值。

#### Meta元数据类主要属性说明

1.  abstract

   一个布尔类型的变量，如果设置为True，则标识当前的Model是抽象基类，这个元选项不具有传递性，只对当前声明的类有效。例如，对于之前定义的BaseModel，用abstract声明为抽象基类，但是子类Topic和Comment不受影响。

2. proxy

   默认值是False，如果设置为True，则表示为基类的代理模型。

3. db_table

   这个字段用于指定数据表的名称。通常，如果没有特别的需要，默认会使用Django的表名生成规则，例如Topic会映射到post_topic表。如果想让Topic映射到topic表，定义db_table='topic'即可。
   db_table元选项对抽象基类是无效的，也不应该在抽象基类中去声明它。因为抽象基类可以被多个子类继承，如果数据表名也可以继承，那么，在数据库创建表的时候就会抛出错误。

4. ordering

   用于指定获取对象列表时的排序规则，它是一个字符串的列表或元组对象，其中的每一个字符串都是Model中定义的字段名，字符串前面可以加上“-”代表逆序，默认按照正序排序。

   ```
   ordering = ['created_time'] # 根据created_time正序排序
   ordering = ['-created_time'] # 根据created_time倒序排序
   ordering = ['created_time', '-last_modified'] # 根据created_time正序排序，再根据last_modified逆序排序
   ```

   排序对于数据库查询是有代价的，所以，只有当所有的查询都需要按照特定的规则排序时才需要设定这个元选项，否则，可以在特定的查询中指定排序规则，不要做统一的定义。

#### Field的通用字段选项

1. blank

   默认值是False，它是数据验证相关的字段，主要体现在管理后台录入数据的校验规则。对于任何一个属性，默认是不允许输入空值的，如果允许这种情况发生，需要设置blank=True。

2.  unique

   默认值是False，它是一个数据库级别的选项，规定该字段在表中必须是唯一的，但是对ManyToManyField和OneToOneField关系类型是不起作用的。
   需要注意的是，数据库层面对待唯一性约束会创建唯一性索引，所以，如果一个字段设置了unique=True，就不需要对这个字段加上索引选项了。

3. null

   默认值是False，它是一个针对数据库的选项，影响表字段属性，规定这个字段的数据是否可以是空值。如果将其设置为True，则Django会在数据库中将空值存储为NULL。
   对于CharField和TextField这样的字符串类型，null字段应该总是设置为False，如果设置为True，对于“空数据”就会有两种概念：空字符串和NULL。有一个例外，是当CharField同时设置了unique=True和blank=True，那也需要设置null=True，这是为了防止在保存多个空白值时违反唯一性约束。

4. default

   用于给字段设置默认值。该选项可以设置为一个值或者是可调用对象，但是不能是可变对象，例如Model实例、列表、集合对象等。

5. primary_key

   默认值是False，如果某个字段设置该选项为True，则它会成为Model的主键字段，且不允许其他的字段再次将该选项设置为True。Model定义中如果没有设置该选项，那么Django会自动添加一个名称为id的AutoField类型的字段。通常情况下，Django的这种默认行为能够满足大部分的场景。
   同时，对于primary_key，需要注意它的两个特性。
   ①在数据库层面，primary_key=True就意味着对应的字段唯一且不能是NULL。
   ②主键字段是只读的，所以，如果用户修改了主键字段的值，并执行了保存动作，结果是创建了一条新的数据记录。

6. help_text

   这个选项用于在表单中显示字段的提示信息。例如在管理后台的编辑页面，对应在字段输入框的下方会显示该选项设定的值。由于表单通常提供给非技术人员，完善的提示信息将更加方便校验和录入字段数据，所以，对字段添加解释信息是很有必要的。

#### 常用基础字段类型

1. IntegerField

   整型字段，取值为-2147483648～2147483647，如果需要使用数字类型，且字段的取值范围符合要求，可以考虑使用该类型，例如Comment中的up和down。
   Django还提供了SmallIntegerField（小整数）、BigIntegerField（64位整数）和PositiveIntegerField（只允许存储大于等于0的整数）等字段类型用来满足存储整数的不同业务场景。

2. AutoField

   一个根据ID自增的IntegerField。如果Model中没有定义主键，那么，Django会自动添加一个名称为id的该类型字段作为主键。
   如果觉得AutoField的取值范围不够用，可以考虑使用BigAutoField，它继承自AutoField，但是它使用的是8个字节的存储空间。

3. CharField

   字符字段，是最常用的字段类型。它有一个必填的参数max_length，且取值只能是大于0的整数，将会在数据库中和表单验证的时候用到。

4. TextField

   与CharField类似，也是用于存储字符类型的字段，但是它用于存储大文本。在字符型字段的选择上，如果需要限制它的最大长度，例如Topic的title（标题），那么就选择CharField类型；反之，就选择TextField，例如Topic的content（内容）。

5. BooleanField

   布尔类型，在某个字段的取值只能是True或False的情况下选择使用该字段类型，例如Topic中的is_online。

6.  DateField和DateTimeField
   这两个字段类型是用来标识时间的，几乎在任何一个Model定义中都能看到会至少引用它们其中的一个。其中Date是日期，以Python中的datetime.date实例表示；DateTime是日期时间，以Python中的datetime.datetime实例表示。

   它们都有两个特殊的参数选项可以设置。
   ①auto_now：这个选项应用在对象保存的时候，会自动设置为当前时间。
   ②auto_now_add：当首次创建对象的时候，会自动将字段设置为当前时间。
   注意，auto_now和auto_now_add与default是互斥的，不应该将它们组合在一起使用。



#### 三种关系字段类型

1. 多对一

   `class django.db.models.ForeignKey(to, on_delete, **options)`

   to: 指定所关联的Model，它的取值可以是直接引用其他的Model，也可以是Model对应的字符串名称。如果要创建递归的关联关系，即Model自身存在多对一的关系，可以设置为字符串self。
   on_delete：当删除关联表的数据时，Django将根据这个参数设定的值确定应该执行什么样的SQL约束。在django.db.models中定义了on_delete的可选值如下。
   CASCADE：级联删除，它是大部分ForeignKey的定义应该选择的约束。它的表现是删除了“一”，则“多”会被自动删除。以Topic和Comment的关系举例：如果删除了Topic，那么所有与该Topic关联的Comment都会被删除。
   PROTECT：删除被引用对象时，将会抛出ProtectedError异常。以Topic和Comment的关系举例：当一个Topic对象被一个或多个Comment对象关联时，删除这个Topic就会触发异常。当然，如果一个Topic还没有被Comment关联，是可以被删除的。
   SET_NULL：设置删除对象所关联的外键字段为null，但前提是设置了选项null为True，否则会抛出异常。以Topic和Comment的关系举例：删除了Topic，与之相关联的Comment的topic字段会被设置为null。
   SET_DEFAULT：将外键字段设置为默认值，但前提是设置了default选项，且指向的对象是存在的。以Topic和Comment的关系举例：id是1的Topic有2个Comment关联，且Comment的外键字段设置了default=2，那么，删除了id是1的Topic之后，与之关联的Comment的外键字段就会被置为2了。
   SET(value)：删除被引用对象时，设置外键字段为value。value如果是一个可调用对象，那么就会被设置为调用后的结果。以Topic和Comment的关系举例：Comment的外键字段设置了on_delete=models.SET(1)，删除id是2的Topic，与之相关联的Comment的外键字段就会被设置为1。
   DO_NOTHING：不做任何处理。但是，由于数据表之间存在引用关系，删除关联数据，会造成数据库抛出异常。
   除了必填的参数之外，ForeignKey还有一些常用的可选参数需要关注。
   to_field：关联对象的字段名称。默认情况下，Django使用关联对象的主键（大部分情况下是id），如果需要修改成其他字段，可以设置这个参数。但是，需要注意，能够关联的字段必须有unique=True的约束。
   db_constraint：默认值是True，它会在数据库中创建外键约束，维护数据完整性。通常情况下，这符合大部分场景的需求。但是，如果数据库中存在一些历史遗留的无效数据，则可以将其设置为False，这时就需要自己去维护关联关系的正确性了。
   related_name：这个字段设置的值用于反向查询，默认不需要设置，Django会设置其为“小写模型名_set”。如果不想创建反向关联关系，可以将它设置为“+”或者以“+”结尾。
   related_query_name：这个名称用于反向过滤。如果设置了related_name，那么将用它作为默认值，否则Django会把模型的名称作为默认值。

2. 一对一

   `class django.db.models.OneToOneField(to, on_delete, parent_link=False, **options)`

   根据定义可以看出，它与ForeignKey的参数几乎是一样的，只是多了一个可选参数parent_link：当其设置为True并在继承自另一个非抽象的Model中使用时，那么该字段就会变成指向父类实例的应用，而不是用于扩展父类并继承父类的属性。
   通常一对一关系类型用在对已有Model的扩展上。例如通过对内置的User进行扩展，添加类似爱好、签名等字段时，就可以新建一个Model，并定义一个字段与User进行一对一的关联。

3. 多对多

   `class django.db.models.ManyToManyField(to, **options)`

   它有一个必填的参数to，与ForeignKey和OneToOneField在概念上是一致的，都是用来指定与当前的Model关联的Model。
   另外，ManyToManyField还有一些重要的可选参数需要关注。
   related_name：与ForeignKey中的related_name作用相同，都是用于反向查询。
   db_table：用于指定中间表的名称。如果没有提供，Django会使用多对多字段的名称和包含这张表的Model的名称组合起来构成中间表的名称（仍然会有App的前缀）。
   through：用于指定中间表。这个参数通常不需要设置，因为Django会默认生成隐式的through Model。由于Django有自己的中间表生成策略，因此如果用户想自己去控制表之间的关联关系或者增加一些额外的信息，就可能会使用这个参数，例如，在关联表中增加描述性字段。



