from course.models.level import Level
from rest_framework import generics, status
from rest_framework.response import Response
from course.serializers.level import LevelSerializer, LevelBasicSerializer,CourseLevelSerializer
from course.models.vocabulary import Vocabulary

class LevelView(generics.CreateAPIView):
    serializer_class = LevelSerializer
    queryset = Level.objects.all()

    def create(self, request, *args, **kwargs):
        indexing = 1
        request_data = request.data
        id_course = request_data.get("course")
        level = Level.objects.filter(course__id=id_course).order_by("-indexing")
        if (len(level)>0):
            indexing = level[0].indexing + 1
        data={
            "indexing" : indexing,
            "title" : request_data.get("title","Default level"),
            "course" : id_course
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LevelShowView(generics.ListAPIView):
    serializer_class = LevelBasicSerializer
    queryset = Level.objects.all()

    def get(self, request, *args, **kwargs):
        id_course = self.kwargs['id']
        level = Level.objects.filter(course__id=id_course).order_by("indexing")
        serializer = LevelBasicSerializer(level, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LevelUpdateView(generics.UpdateAPIView):
    serializer_class = LevelSerializer
    queryset = Level.objects.all()

class LevelVocabularyView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        id_course = self.kwargs['id']
        data = []
        levels = Level.objects.filter(course__id=id_course).order_by("indexing")
        for level in levels:
            vocabularys = Vocabulary.objects.filter(level__id=level.id)
            item = {
                "level" : level,
                "vocabularys" : vocabularys
            }
            data.append(item)
        serializer = CourseLevelSerializer(data,many=True,context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)