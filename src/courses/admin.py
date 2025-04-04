import helpers 

from django.contrib import admin
from cloudinary import CloudinaryImage
from .models import Course , Lesson
from django.utils.html import mark_safe, format_html


# Register your models here.

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    readonly_fields = ['public_id', 'updated', 'display_image', 'display_video']

    def display_image(self, obj):
        url = helpers.get_cloudinary_image_object(obj, field_name='thumbnail', width=200)
        return format_html(f'<img src="{url}" alt="Thumbnail" />')

    display_image.short_description = 'Thumbnail'

    def display_video(self, obj):
        html = helpers.get_cloudinary_video_object(obj, field_name='video', as_html=True, width=600)
        return mark_safe(html)
    
    display_video.short_description = 'current video' 




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title', 'status', 'access']
    fields = ['title', 'description', 'status', 'image', 'access', 'display_image', 'is_published', 'public_id']
    list_filter = ['status', 'access'] 
    readonly_fields = ['public_id', 'display_image' , 'is_published']

    def display_image(self, obj, *args, **kwargs):
        # Accessing the image attribute of the Course instance
        url = helpers.get_cloudinary_image_object(obj, field_name='image', width=200)
        return format_html(f'<img src="{url}"/>')
    