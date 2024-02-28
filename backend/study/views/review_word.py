from rest_framework import generics, status,viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from course.models.vocabulary import Vocabulary
from course.models.course import Course
from study.serializers.review_word import ReviewWordSerializer
from study.models.review_word import ReviewWord
from account.models.users import User

class ReviewWordView(generics.CreateAPIView):
    queryset = ReviewWord.objects.all()
    serializer_class = ReviewWordSerializer

    def post(self, request, *args, **kwargs):
        id_user = request.data.get("user",None)
        id_level = request.data.get("level",None)

        if (id_user!=None and id_level!=None):
            item = self.queryset.filter(user__id=id_user).filter(level__id=id_level)
            if len(item)==0:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(dict(status=status.HTTP_201_CREATED, headers=headers))
            return Response(dict(status=status.HTTP_204_NO_CONTENT))
 
class CourseLevelAfterReviewView(viewsets.ViewSet):

    @action(methods=['PATCH'],detail=False)
    def exam_review(self,request,*args, **kwargs):
        try:
            id_user = request.data.get("user",None)
            id_level = request.data.get("level",None)
            id_vocabulary = request.data.get("vocabulary",None)
            total_score = request.data.get("score",None)
            review_word = ReviewWord.objects.filter(level__id = id_level, user__id=id_user)

            if len(review_word)>0:
                vocabulary = Vocabulary.objects.get(id=id_vocabulary)
                review_word[0].id_word_last = vocabulary
                review_word[0].save()

                account = User.objects.get(id=id_user)
                account.total_mark_learned = account.total_mark_learned + int(total_score)
                account.save()
        except:
            return Response(dict(msg="System has error", status=status.HTTP_204_NO_CONTENT))
        return Response(dict(msg="Success", status=status.HTTP_200_OK))