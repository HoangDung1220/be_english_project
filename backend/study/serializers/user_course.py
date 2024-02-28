from rest_framework import serializers
from study.models.user_course import UserCourse
from study.models.course_level import CourseLevel
from account.serializers.UserSerializers import UserDetailSerializer
from course.models.vocabulary import Vocabulary
from course.models.level import Level

class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ["user","course"]

class UserCourseDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = UserCourse
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            level_course = CourseLevel.objects.filter(user_course__id = instance.id)
            sum = 0
            for item in level_course:
                 if (item.last_question_learned!=None):
                    vocabulary = Vocabulary.objects.get(id = item.last_question_learned.id)
                    sum = sum + Vocabulary.objects.filter(level__id = item.level.id, indexing__lte=vocabulary.indexing).count()
            total_num = Vocabulary.objects.filter(course__id=instance.course.id).count()
            ret['percentage']= round((sum/total_num)*100)
            
        except Exception:
            print("err")
        return ret