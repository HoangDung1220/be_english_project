from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from course.models.course import Course
from course.models.level import Level
from course.models.vocabulary import Vocabulary
from study.models.user_course import UserCourse
from study.models.course_level import CourseLevel
from group.models.group_course import GroupCourse
from group.models.group_member import GroupMember
from django.db.models import Q
from rating.models.rating_course import RatingCourse
from course.serializers.course import CourseBasic1Serializer
from course.serializers.course import CourseSerializer,CourseDetailSerializer,CourseInformationSerializer, CourseSuggestSerializer, CourseAdminSerializer, TagSerializer, CourseBasicSerializer
from rest_framework.response import Response
from suggest.suggest import Suggest



class CourseView(generics.ListCreateAPIView):
    queryset = Course.objects.filter(status="public")
    serializer_class = CourseSerializer

class CourseInformationlView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseInformationSerializer

    def get(self, request, *args, **kwargs):
        msg = "has error"
        id=self.kwargs['pk']
        id_level=self.kwargs['level']
        user=self.kwargs['user']
        percentage = 0
        try:
            level = Level.objects.get(id=id_level)
            course = Course.objects.get(id=id)
            user_course = UserCourse.objects.get(course__id = id, user__id= user)
            if user_course!=None:
                course_level = CourseLevel.objects.filter(user_course__id = user_course.id, level__id = id_level)
                if len(course_level) >0:
                    print(course_level)
                    if course_level[0].is_complete:
                        percentage = 100
                    else:
                        print(Vocabulary.objects.all())
                        num = Vocabulary.objects.filter(course__id = id, level__id = id_level).count()
                        if course_level[0].last_question_learned !=None and num>0:
                            percentage = float(course_level[0].last_question_learned.indexing / num) * 100
                else:
                    percentage = 0
                num_level = Level.objects.filter(course__id = id).count()
                print(num_level)
                next = None
                if (level.indexing+1<=num_level):
                    next_level = Level.objects.filter(course__id = id, indexing = level.indexing +1)
                    if len(next_level) > 0:
                        next = next_level[0]

                data = {
                    "course" : course,
                    "level" : level,
                    "percentage" : percentage,
                    "num_level":num_level,
                    "next_level": next
                }
                serializer = CourseInformationSerializer(data,context={"request": request})
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_400_BAD_REQUEST))

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(status="public")
    serializer_class = CourseDetailSerializer

    # moi chinh sua
    def get(self, request, *args, **kwargs):
        id=self.kwargs['pk']
        levels = Level.objects.filter(course__id=id)
        levels_id = [item.id for item in levels]
        vocabularys = Vocabulary.objects.filter(course__id = id).exclude(level__id__in=levels_id).order_by("indexing")
        course = Course.objects.filter(id=id)
        print(course)
        data = {
            "level" : levels,
            "course" : course[0],
            "vocabulary" : vocabularys
        }
        serializer = CourseDetailSerializer(data,context={"request": request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class CourseSuggestGroupView(viewsets.ViewSet):

    @action(methods=['GET'],detail=False)
    def suggest(self,request,*args, **kwargs):
        try:
            id = self.request.query_params.get("user",None)
            id_group = self.request.query_params.get("group",None)
            if (id!=None):
                group_course = GroupCourse.objects.filter(group__id = id_group).values("course")
                user_courses = UserCourse.objects.filter(course__status='public').exclude(course__user_created = id).values("course")
                public_courses = Course.objects.filter(Q(user_created__id = id) | Q(id__in=user_courses)).exclude(id__in = group_course).filter(status='public')[:10]
                private_courses = Course.objects.filter(Q(user_created__id = id)).exclude(id__in = group_course).filter(status='private')[:10]
                data = {
                    "public_course" : public_courses,
                    "private_course" : private_courses
                }
                d = CourseSuggestSerializer(data,context={"request": request}).data
                return Response(data=d,status=status.HTTP_200_OK)
        except:
            return Response(dict(msg="Having error. Please try again", status=status.HTTP_400_BAD_REQUEST))

class CourseAdminView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseAdminSerializer

    def get(self, request, *args, **kwargs):
        input = self.request.query_params.get("search",None)
        courses = Course.objects.filter(delete_flag=False).order_by("-created_at")

        if input!=None:
            courses = courses.filter(Q(title__contains=input) | Q(description__contains=input))
        lst = []
        for course in courses:
            ratings = RatingCourse.objects.filter(course__id= course.id)
            if len(ratings)>0:
                tong = sum([item.rating for item in ratings])/len(ratings)
            else:
                tong = 0
            d = {
                "course" :  course,
                "rating" : tong
            }
            lst.append(d)

        serializer = CourseAdminSerializer(lst,context={"request": request}, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class CoursePublicView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        category=self.kwargs['category']
        tag=self.request.query_params.get("tag",None)
        search=self.request.query_params.get("search",None)
        if category==0:
            courses = Course.objects.all()
        else: 
            courses = Course.objects.filter(category__id = category)
        courses = courses.filter(status="public").order_by("-number_user_learned")
        if tag !=None:
             courses = courses.filter(tag__contains=tag)
        if search !=None:
            courses = courses.filter(Q(title__contains=search) | Q(description__contains=search))

        serializer = CourseSerializer(courses,context={"request": request}, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class CourseHomeView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        user_id=self.kwargs['id']
        tag=self.request.query_params.get("tag",None)
        search=self.request.query_params.get("search",None)

        # suggestion
        ids = Suggest.suggestCourse(user_id)
        print(ids)
        if len(ids)>0:
            courses2 = Course.objects.filter(id__in=ids).distinct()
            if tag !=None:
                courses2 = courses2.filter(tag__contains=tag)
            if search !=None:
                courses2 = courses2.filter(Q(title__contains=search) | Q(description__contains=search))

            courses1 = Course.objects.filter(status="public").exclude(id__in=ids).order_by("-number_user_learned")
            if tag !=None:
                courses1 = courses1.filter(tag__contains=tag)
            if search !=None:
                courses1 = courses1.filter(Q(title__contains=search) | Q(description__contains=search))
            courses = courses2.union(courses1)
        else: 
            courses = Course.objects.filter(status="public").order_by("-number_user_learned")

        # if tag !=None:
        #     courses = courses.filter(tag__contains=tag)
        # if search !=None:
        #     courses = courses.filter(Q(title__contains=search) | Q(description__contains=search))

        serializer = CourseSerializer(courses,context={"request": request}, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    
class TagPublicView(generics.ListAPIView):
    serializer_class = TagSerializer
    
    def get(self, request, *args, **kwargs):
        category=self.kwargs['category']
        courses = Course.objects.filter(category__id = category, status="public")
        tags = {"default"}
        data = []
        for course in courses:
            if course.tag!=None:
                tag = course.tag.split()
                for t in tag:
                    tags.add(t)
        tags.remove("default")
        for t in tags:
            item = {
                    "tags" : t
                }
            data.append(item)
        serializer = TagSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class TagSearchView(generics.ListAPIView):
    serializer_class = TagSerializer
    
    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(status="public")
        tags = []
        data = []
        for course in courses:
            tag = course.tag.split()
            for t in tag:
                tags.append(t)
        dict = {}

        for t in tags:
            item = {
                    "tags" : t
                }
            data.append(item)
        serializer = TagSerializer(data, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class SearchCourseView(viewsets.ViewSet):

    @action(methods=['Post'],detail=False)
    def search(self,request,*args, **kwargs):
        tags = request.data.get("tags", None)
        value = request.data.get("input",None)
        if value!=None:
            courses = Course.objects.filter(Q(title__contains=value) | Q(description__contains=value)).filter(status="public")
        else:
            courses = Course.objects.filter(status="public")
        
        print(courses)
        if tags!=None:
            
            courses = courses.filter(tag__contains=tags)
        serializer = CourseSerializer(courses,context={"request": request}, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class SearchCoursePersonalView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        id_user = self.kwargs['user']
        status1 = self.request.query_params.get("status",None)
        value = self.request.query_params.get("input",None)
        # flag =1 > get data of me
        flag = self.request.query_params.get("flag",None)

        if flag == "1":
            courses = Course.objects.filter(user_created__id = id_user)
        else:
            # get course tu group course > lay group cua nguoi dung > lay course trong group do > va lay cac khoa hoc ben ngoai ma nguoi dung dang hoc
            user_courses = UserCourse.objects.filter(user__id = id_user)
            id_courses1 =[item.course.id for item in user_courses]

            groups = GroupMember.objects.filter(member__id = id_user).values("group")
            group_course = GroupCourse.objects.filter(group__id__in=groups).distinct()
            id_courses2 =[item.course.id for item in group_course]
            ids = id_courses1+id_courses2

            courses = Course.objects.filter(id__in=ids).exclude(user_created__id = id_user)
        
        if status1=='TO DO':
            user_course = UserCourse.objects.filter(user__id = id_user)
            ids = [item.course.id for item in user_course]
            courses = courses.exclude(id__in = ids)
        elif status1=='DOING':
            user_course = UserCourse.objects.filter(user__id = id_user,is_complete=False)
            ids = [item.course.id for item in user_course]
            courses = courses.filter(id__in = ids)
        elif status1=="COMPLETE":
            user_course = UserCourse.objects.filter(user__id = id_user,is_complete=True)
            ids = [item.course.id for item in user_course]
            courses = courses.filter(id__in = ids)

        if value!=None:
            courses = courses.filter(Q(title__contains=value) | Q(description__contains=value))
        
        serializer = CourseSerializer(courses,context={"request": request}, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class CreateImageCouse(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseBasicSerializer

class UpdateImageCouse(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseBasicSerializer

class CoursePublicEachUser(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseBasicSerializer         

    def get(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        courses = Course.objects.filter(user_created__id=id, status="public").order_by("-created_at")
        serializer = CourseBasicSerializer(courses,many=True,context={"request": request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class CourseEachUserAdmin(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseBasicSerializer         

    def get(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        courses = Course.objects.filter(user_created__id=id).order_by("-created_at")
        serializer = CourseBasicSerializer(courses,many=True,context={"request": request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class DeleteCourse(generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["pk"]

        courses = Course.objects.filter(id=id)
        if len(courses)>0:
            courses[0].delete_flag = True
            courses[0].save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(dict(msg="Can't delete course", status=status.HTTP_400_BAD_REQUEST)) 
    
class CoursePublicEachUserAdmin(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseBasicSerializer         

    def get(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        courses = Course.objects.filter(user_created__id=id, delete_flag=False).order_by("-created_at")
        serializer = CourseBasicSerializer(courses,many=True,context={"request": request})
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
class GetCourseView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(delete_flag = False)
    serializer_class = CourseBasic1Serializer



            



