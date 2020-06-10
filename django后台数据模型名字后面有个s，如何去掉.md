只要修改每个数据类的meta就好了，例子：

```python
class Topic(BaseModel):
    class Meta:
        verbose_name = u'话题'
        verbose_name_plural = u'话题'
        
class Comment(BaseModel):
    class Meta:
        verbose_name = u'话题评论'
        verbose_name_plural = u'话题评论'

```

