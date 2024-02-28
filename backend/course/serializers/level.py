from rest_framework import serializers
from course.models.level import Level
from course.models.vocabulary import Vocabulary
from course.serializers.vocabulary import VocabularySerializer

class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = "__all__"

class LevelBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        try:
            vocabulary = Vocabulary.objects.filter(level__id=instance.id).count()
            ret['num_vocabulary']= vocabulary
        except Exception:
            print("err")
        return ret
    
class CourseLevelSerializer(serializers.Serializer):

    level = LevelSerializer()
    vocabularys = VocabularySerializer(many=True)
