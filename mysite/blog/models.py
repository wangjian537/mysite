from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail

class BlogType(models.Model):
    """
    博客类型
    """
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
    """
    定义博客内容
    """
    # 标题
    title = models.CharField(max_length=50)
    # 博客类型
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    # 内容
    content =RichTextUploadingField()
    # 作者
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 发布时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 最后一次修改时间
    last_update_time = models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)
    def __str__(self):
        return "<blog: %s>" % self.title

    class Meta:
        ordering = ['-create_time']
