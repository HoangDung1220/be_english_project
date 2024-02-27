from rest_framework import serializers
from course.models.vocabulary import Vocabulary

class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = "__all__"

class VocabularyMeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields =  ("mean","vocabulary","image")