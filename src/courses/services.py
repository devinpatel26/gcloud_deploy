
from .models import Course, Lesson, PublishedStatus


def get_publish_courses():
    return Course.objects.filter(status=PublishedStatus.PUBLISHED)

def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(status=PublishedStatus.PUBLISHED, public_id=course_id)
    except:
        pass
    return obj

def get_course_lessons(course_obj=None):
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.lesson_set.filter(
        course__status=PublishedStatus.PUBLISHED,
        status__in=[PublishedStatus.PUBLISHED, PublishedStatus.COMING_SOON]
    ).order_by('id')  # Replace 'id' with the desired field to order by
    return lessons

def get_lesson_detail(lesson_id=None, course_id=None):
    if lesson_id is None or course_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course__public_id=course_id,
            course__status = PublishedStatus.PUBLISHED,     
            status__in=[PublishedStatus.PUBLISHED,PublishedStatus.COMING_SOON],
            public_id= lesson_id)
    except Exception as e:
        print("lesson_details" , e )
    return obj