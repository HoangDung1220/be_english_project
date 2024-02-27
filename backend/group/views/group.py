from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from group.serializers.group import GroupSerializer, GroupDetailSerialzer, GroupSpaceSerializer, GroupAdminSerializer
from group.models.group import Group
from group.models.group_course import GroupCourse
from group.models.group_member import GroupMember
from course.models.course import Course
from study.models.user_course import UserCourse
from rating.models.rating_group import RatingGroup
from django.db.models import Q



class GroupView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetailView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user']
        lst = []
        groups = Group.objects.filter(create_by__id=user_id)
        for group in groups:
            id = group.id
            courses = GroupCourse.objects.filter(group__id=id)
            members = GroupMember.objects.filter(group__id = id)
            members_course = []
            if len(courses) >0 and len(members)>0:
                for course in courses:
                    item_course = Course.objects.get(id=course.course.id)
                    user_courses = UserCourse.objects.filter(course__id = course.course.id)
                    data = {
                        "course":item_course,
                        "members" : user_courses
                    }
                    members_course.append(data)
            group_course = GroupCourse.objects.filter(group__id = id).values("course")
            user_courses = UserCourse.objects.filter(course__status='public').exclude(course__user_created = user_id).values("course")
            public_courses = Course.objects.filter(Q(user_created__id = user_id) | Q(id__in=user_courses)).exclude(id__in = group_course).filter(status='public')[:10]
            private_courses = Course.objects.filter(Q(user_created__id = user_id)).exclude(id__in = group_course).filter(Q(status='private') | Q(status='protected'))[:10]
    
            data = {
                "group" : group,
                "courses" : courses,
                "members" : members,
                "members_course" :members_course,
                "public_course" : public_courses,
                "private_course" : private_courses
            }
            lst.append(data)

        d = GroupDetailSerialzer(lst,many=True,context={"request": request}).data
        return Response(d, status=status.HTTP_201_CREATED)
    
class GroupSpaceView(generics.ListAPIView):
    queryset = Group.objects.filter()
    serializer_class = GroupSpaceSerializer()

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['user']
            group_member = GroupMember.objects.filter(member__id=id)
            ids = [item.group.id for item in group_member]
            datas =[]
            groups = Group.objects.filter(id__in = ids)
            for group in groups:
                members = GroupMember.objects.filter(group__id= group.id).count()
                courses = GroupCourse.objects.filter(group__id= group.id).count()
                d = {
                    "group" : group,
                    "number_member" : members,
                    "number_course" : courses
                }
                datas.append(d)
            serializers = GroupSpaceSerializer(datas, many=True,context={"request": request}).data
            return Response(data = serializers, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GroupAdminView(generics.ListAPIView):
    queryset = Group.objects.filter()
    serializer_class = GroupAdminSerializer()

    def get(self, request, *args, **kwargs):
        try:
            datas =[]
            groups = Group.objects.all()
            for group in groups:
                members = GroupMember.objects.filter(group__id= group.id).count()
                courses = GroupCourse.objects.filter(group__id= group.id).count()
                ratings = RatingGroup.objects.filter(group__id= group.id)
                if len(ratings)>0:
                    tong = sum([item.rating for item in ratings])/len(ratings)
                else:
                    tong = 0
                d = {
                    "group" : group,
                    "number_member" : members,
                    "number_course" : courses,
                    "rating" : tong
                }
                datas.append(d)
            serializers = GroupAdminSerializer(datas, many=True,context={"request": request}).data
            return Response(data = serializers, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class GroupDetailAdminView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        group_id = self.kwargs['group']
        group = Group.objects.get(id=group_id)
        courses = GroupCourse.objects.filter(group__id=group_id)
        members = GroupMember.objects.filter(group__id = group_id)
        members_course = []
        if len(courses) >0 and len(members)>0:
            for course in courses:
                item_course = Course.objects.get(id=course.course.id)
                user_courses = UserCourse.objects.filter(course__id = course.course.id)
                data = {
                        "course":item_course,
                        "members" : user_courses
                    }
                members_course.append(data)
        group_course = GroupCourse.objects.filter(group__id = group_id).values("course")
        user_courses = UserCourse.objects.all().values("course")
        public_courses = Course.objects.all().exclude(id__in = group_course).filter(status='public')[:10]
        private_courses = Course.objects.all().exclude(id__in = group_course).filter(Q(status='private') | Q(status='protected'))[:10]
    
        data = {
                "group" : group,
                "courses" : courses,
                "members" : members,
                "members_course" :members_course,
                "public_course" : public_courses,
                "private_course" : private_courses
        }

        d = GroupDetailSerialzer(data,context={"request": request}).data
        return Response(d, status=status.HTTP_201_CREATED)
    