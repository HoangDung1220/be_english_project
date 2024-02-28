from rest_framework import generics,status
from rating.serializers.rating_course import RatingCourseSerializer
from rating.models.rating_course import RatingCourse
from rest_framework.response import Response


class RatingCourseView(generics.CreateAPIView):
    queryset = RatingCourse.objects.all()
    serializer_class = RatingCourseSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.data.get("user",None)
        course = self.request.data.get("course",None)
        rating = self.request.data.get("rating",None)

        item = RatingCourse.objects.filter(user__id = user, course__id=course)
        if (len(item)==0):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            item[0].rating = rating
            item[0].save()
            serializer = self.get_serializer(item[0])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetRatingCourseView(generics.ListAPIView):
    queryset = RatingCourse.objects.all()
    serializer_class = RatingCourseSerializer

    def get(self, request, *args, **kwargs):
        user = self.kwargs.get("user",None)
        course = self.kwargs.get("course",None)

        item = RatingCourse.objects.filter(user__id = user, course__id=course)
        if len(item)>0:
            serializer = self.get_serializer(item[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)




