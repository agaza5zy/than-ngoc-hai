from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên khóa học")
    description = models.TextField(verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    # Quan hệ nhiều-nhiều (Many-to-Many)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    def __str__(self):
        return self.title