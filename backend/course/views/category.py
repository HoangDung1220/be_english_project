from rest_framework import generics,status
from course.models.category import Category
from course.serializers.category import CategorySerializer
from suggest.suggest import Suggest
from rest_framework.response import Response

class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        Suggest.suggest()
        Suggest.getSuggestForUser(2)
        return Response(status=status.HTTP_200_OK)
    
class CategoryPublicView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_delete=False)

class CategoryDetailPublicView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_delete=False)