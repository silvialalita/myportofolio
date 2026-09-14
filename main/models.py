import uuid
from django.db import models

# Create your models here.
# Model bertugas untuk mengatur dan mengelola data pada sebuah aplikasi.
class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
        ('committee', 'Committee'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, default='')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    EDUCATION_TYPES = [
        ('formal', 'Formal Education'),
        ('program', 'Educational Program'),
        ('certification', 'Certification'),
        ('course', 'Course / Training'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=EDUCATION_TYPES, default='formal')
    thumbnail = models.URLField(blank=True, default='')
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.institution
    
    @property
    def is_ongoing(self):
        return self.ended_at is None