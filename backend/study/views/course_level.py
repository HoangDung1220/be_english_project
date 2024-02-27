from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from study.models.course_level import CourseLevel
from study.models.user_course import UserCourse
from course.models.vocabulary import Vocabulary
from study.serializers.course_level import CourseLevelSerializer,CourseLevelDetailSerializer

class CourseLevelView(generics.CreateAPIView):
    queryset = CourseLevel.objects.all()
    serializer_class = CourseLevelSerializer

    def post(self, request, *args, **kwargs):
        id_user_course = request.data.get("user_course",None)
        id_level = request.data.get("level",None)
        if (id_user_course!=None and id_level!=None):
            item = self.queryset.filter(user_course__id=id_user_course).filter(level__id=id_level)
            if len(item)==0:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(dict(status=status.HTTP_201_CREATED, headers=headers))
            elif len(item):
                if item[0].is_complete:
                    return Response(dict(msg="User had learned level before", status=status.HTTP_204_NO_CONTENT))
                else:
                    return Response(dict(msg="User was learning level", status=status.HTTP_204_NO_CONTENT))
                
class CourseLevelUser(viewsets.ViewSet):
    @action(methods=['GET'], detail=False)
    def course(self,request,*args, **kwargs):
        id_user = self.request.query_params.get("user",None) 
        id_course = self.request.query_params.get("course",None) 
        user_course = UserCourse.objects.get(course__id = id_course, user__id = id_user)
        print(user_course)
        if user_course!=None:
            course_level = CourseLevel.objects.filter(user_course__id = user_course.id)
            if len(course_level)>0:
                d = CourseLevelDetailSerializer(course_level, many=True).data
                return Response(dict(data=d, msg="Get data successfully", status=status.HTTP_200_OK))
            return Response(dict(msg="No data matching", status=status.HTTP_204_NO_CONTENT))
        else:
            return Response(dict(msg="No data matching", status=status.HTTP_204_NO_CONTENT))

    
class CourseLevelAfterView(viewsets.ViewSet):

    @action(methods=['PATCH'],detail=False)
    def exam_complete(self,request,*args, **kwargs):
        try:
            id_user = request.data.get("user",None)
            id_course = request.data.get("course",None)
            id_level = request.data.get("level",None)
            id_vocabulary = request.data.get("vocabulary",None)
            total_score = request.data.get("score",None)
            user_course = UserCourse.objects.filter(course=id_course,user=id_user)
            if len(user_course)>0:
                user_course[0].total_score = user_course[0].total_score + int(total_score)
                user_course[0].save()
                course_level = CourseLevel.objects.filter(user_course__id = user_course[0].id, level__id = id_level)
                if len(course_level)>0:
                    obj = Vocabulary.objects.get(id = id_vocabulary)
                    course_level[0].last_question_learned=obj
                    vocabu = Vocabulary.objects.filter(course__id = id_course, level__id = id_level).order_by("-indexing")
                    print(id_vocabulary)
                    print(vocabu[0].id)
                    if int(id_vocabulary) == vocabu[0].id:
                        course_level[0].is_complete = True
                    course_level[0].save()
        except:
            return Response(dict(msg="System has error", status=status.HTTP_204_NO_CONTENT))
        data = CourseLevel.objects.filter(user_course__id = user_course[0].id, level__id = id_level)[0]
        d = CourseLevelDetailSerializer(data).data
        return Response(dict(data=d,msg="Success", status=status.HTTP_200_OK))


