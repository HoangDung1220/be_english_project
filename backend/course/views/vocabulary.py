from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from course.serializers.vocabulary import VocabularySerializer,VocabularyMeanSerializer
from course.models.vocabulary import Vocabulary
from course.models.course import Course
from rest_framework.decorators import action

from study.models.course_level import CourseLevel
from study.models.user_course import UserCourse
from study.models.review_word import ReviewWord

class VocabularyTestView(generics.ListAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer

class VocabularyInLevel(generics.ListAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer

    def get(self, request, *args, **kwargs):
        id_level = self.kwargs['id_level']
        id_course = self.kwargs['id_course']
        vocabularys = self.queryset.filter(course__id = id_course).filter(level__id=id_level).order_by("indexing")
        data = self.serializer_class(vocabularys, many=True,context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)
    
class VocabularyInCourse(generics.ListAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer

    def get(self, request, *args, **kwargs):

        id_course = self.kwargs['id_course']
        vocabularys = self.queryset.filter(course__id = id_course).order_by("indexing")
        d = vocabularys
        if (len(vocabularys)<4):
            courses = Course.objects.filter(status="public").exclude(id = id_course)
            vocabulary1s = self.queryset.filter(course__id__in = courses)[:4]
            d = vocabularys.union(vocabulary1s)
        data = VocabularyMeanSerializer(d, many=True,context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)
    

    
class VocabularyView(generics.CreateAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer

    def post(self, request, *args, **kwargs):
        vocabulary = request.data.get("vocabulary",None)
        course = request.data.get("course",None)
        mean = request.data.get("mean",None)
        sample = request.data.get("sample",None)
        description = request.data.get("description",None)
        image = request.data.get("image",None)
        audio = request.data.get("audio",None)
        level = request.data.get("level",None)

        indexing = 1
        data = Vocabulary.objects.filter(level__id = level).order_by("-indexing")
        if len(data)>0:
            indexing = data[0].indexing +1
        
        data = {
            "vocabulary" : vocabulary,
            "course":course,
            "mean":mean,
            "sample":sample,
            "description":description,
            "image":image,
            "audio":audio,
            "level":level,
            "indexing":indexing
        }
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



        
class VocabularyUserView(viewsets.ViewSet):

    @action(methods=['GET',],detail=False)
    def learn(self,request,*args, **kwargs):
        id_level = self.request.query_params.get("level",None)
        id_course = self.request.query_params.get("course",None) 
        id_user = self.request.query_params.get("user",None) 
        course_level = CourseLevel.objects.filter(user_course__user__id = id_user).filter(user_course__course__id=id_course).filter(level__id=id_level)
        if (len(course_level)>0):
            if course_level[0].last_question_learned!=None:
                last_question = course_level[0].last_question_learned.indexing
            else:
                last_question = 0
            num_vocabularys = len(Vocabulary.objects.filter(course__id = id_course).filter(level__id = id_level))
            if last_question!=0:
                num_begin= last_question+1 
            else: 
                num_begin=1

            if last_question+2<num_vocabularys:
                num_last = last_question + 2
            else:
                num_last = num_vocabularys
            vocabularys = Vocabulary.objects.filter(course__id = id_course,level__id = id_level).filter(indexing__gte=num_begin, indexing__lte=num_last).order_by("indexing")
            data = VocabularySerializer(vocabularys, many=True,context={"request": request}).data
            return Response(dict(data=data,msg="Get successful", status=status.HTTP_200_OK))
        else:
            return Response(dict(msg="No data", status=status.HTTP_204_NO_CONTENT))

class VocabularyInCoursePublic(generics.ListAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer

    def get(self, request, *args, **kwargs):

        id_course = self.kwargs['id_course']
        vocabularys = self.queryset.filter(course__id = id_course).order_by("id")[:100]
        data = VocabularyMeanSerializer(vocabularys, many=True,context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)

class ManagementVocabulary(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer


class VocabularyUserReviewView(viewsets.ViewSet):

    @action(methods=['GET',],detail=False)
    def review(self,request,*args, **kwargs):
        id_level = self.request.query_params.get("level",None)
        id_user = self.request.query_params.get("user",None) 
        vocabularys = Vocabulary.objects.filter(level__id = id_level).order_by("-indexing")
        review_word = ReviewWord.objects.filter(user__id = id_user).filter(level__id=id_level)
        if (len(review_word)>0):
            if review_word[0].id_word_last!=None and review_word[0].id_word_last!=vocabularys[0]:
                last_question = review_word[0].id_word_last.indexing
            else:
                last_question = 0
            num_vocabularys = len(Vocabulary.objects.filter(level__id = id_level))
            if last_question!=0:
                num_begin= last_question+1 
            else: 
                num_begin=1

            if last_question+2<num_vocabularys:
                num_last = last_question + 2
            else:
                num_last = num_vocabularys
            vocabularys = Vocabulary.objects.filter(level__id = id_level).filter(indexing__gte=num_begin, indexing__lte=num_last).order_by("indexing")
            data = VocabularySerializer(vocabularys, many=True,context={"request": request}).data
            return Response(dict(data=data,msg="Get successful", status=status.HTTP_200_OK))
        else:
            return Response(dict(msg="No data", status=status.HTTP_204_NO_CONTENT))

