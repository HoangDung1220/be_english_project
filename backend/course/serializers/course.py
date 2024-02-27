from rest_framework import serializers
from course.models.course import Course
from account.models.users import User
from study.models.user_course import UserCourse
from course.models.vocabulary import Vocabulary
from course.serializers.level import LevelSerializer
from course.serializers.vocabulary import VocabularySerializer
from course.serializers.category import CategorySerializer

class CourseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    category = CategorySerializer()

    class Meta:
        model = Course
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            user = User.objects.get(pk=instance.user_created.id)
            ret['user_name']= user.username
            number_user_course = UserCourse.objects.filter(course__id = instance.id).count()
            ret['number_user_learn'] = number_user_course
            number_vocabulary = Vocabulary.objects.filter(course__id = instance.id).count()
            ret['number_vocabulary'] = number_vocabulary
        except Exception:
            print("err")
        return ret
    
class CourseBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id','category','user_created', 'title','description','tag','image') 

class CourseDetailSerializer(serializers.Serializer):
    course = CourseBasicSerializer()
    level = LevelSerializer(many=True)
    vocabulary = VocabularySerializer(many=True)


class CourseInformationSerializer(serializers.Serializer):
    course = CourseSerializer()
    level = LevelSerializer()
    next_level = LevelSerializer()
    percentage = serializers.FloatField()
    num_level = serializers.IntegerField()

class CourseSuggestSerializer(serializers.Serializer):
    public_course = CourseBasicSerializer(many=True)
    private_course = CourseBasicSerializer(many=True)

class CourseAdminSerializer(serializers.Serializer):
    course = CourseSerializer()
    rating = serializers.IntegerField()

class TagSerializer(serializers.Serializer):
    tags = serializers.CharField()
