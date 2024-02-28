from rest_framework import serializers
from study.models.review_word import ReviewWord

class ReviewWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewWord
        fields = "__all__"
