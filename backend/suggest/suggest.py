from account.models.users import User
from course.models.course import Course
from group.models.group import Group
from rating.models.rating_group import RatingGroup
from rating.models.rating_course import RatingCourse
import numpy as np
from numpy.linalg import norm

class Suggest:
    # get data from database anf store matrix
    matrix_ratings = []
    values = []

    # calculation average
    averages=[]

    # Utility Matrix
    utility_matrix = []

    # Utility Matrix
    results = []



    @classmethod
    def initialData(self):
        users = User.objects.order_by("id").values("id")
        courses = Course.objects.filter(status="public").order_by("id").values("id")
        for course in courses:
            print(course)
            values = []
            for user in users:
                ratings = RatingCourse.objects.filter(course__id = course['id'], user__id= user['id']).values("rating")
                if (len(ratings)>0):
                    values.append(ratings[0]['rating'])
                else:
                    values.append(0)
            self.matrix_ratings.append(values)
            self.values = np.array(self.matrix_ratings)
        print("Rating ban dau:")
        print(len(self.values))
        print(self.values)
 

    @classmethod
    def nomilizerData(self):
        self.utility_matrix = [[0 for _ in range(len(self.values[0]))] for _ in range(len(self.values))]

        for i in range(0, len(self.values[0])):
            col = self.values[:, i]
            tmp = [i for i in col if i != 0]
            if len(tmp) > 0:
                self.averages.append(sum(tmp)/len(tmp))
            else:
                self.averages.append(0)
            for j in range(0, len(self.values)):
                if self.values[j][i] !=0:
                    self.utility_matrix[j][i] = self.values[j][i] - self.averages[i]    
        print("ma tran sau khi chuan hoa:")
        print(np.array(self.utility_matrix))
  

    @classmethod
    def result(self):
        self.utility_matrix = np.array(self.utility_matrix)
        self.results = [[0 for _ in range(len(self.utility_matrix[0]))] for _ in range(len(self.utility_matrix[0]))]
        for i in range(len(self.utility_matrix[0])):
            rating_i = self.utility_matrix[:, i]
            for j in range(len(self.utility_matrix[0])):
                rating_j = self.utility_matrix[:, j]
                self.results[i][j] = np.dot(rating_i,rating_j)/(norm(rating_i)*norm(rating_j))
        self.results = np.array(self.results)
        print("tinh do tuong quan")
        print(self.results)
         

    @classmethod
    def suggest(self):
        self.matrix_ratings = []
        self.values = []
        self.averages = []
        self.utility_matrix = []
        self.results = []
        self.initialData()
        self.nomilizerData()
        self.result()

    @classmethod
    def getSuggestForUser(self,user):
        self.suggest()
        users = User.objects.order_by("id").values("id")
        ids = [user['id'] for user in users]
        index = ids.index(user)
        vals = self.results[index ,:]
        rs = []
        for i in range(len(vals)):
            if vals[i]>0 and vals[i]<0.99:
                rs.append(ids[i])
        return rs

    @classmethod
    def predictUser(self):
        self.suggest()
        # get gia tri ma tran value = 0 de bat dau du doan
        for i in range(len(self.values[0])): # 0-4
            for j in range(len(self.values)): # 0-9
                if self.values[j][i]==0:
                   
                    index_max = []
                    value_max = []
                    similarity_max = []
                    for k in range(len(self.values[0])):
                        if self.values[j][k] != 0:
                            index_max.append(k)
                            value_max.append(self.values[j][k])
                    for u in range(len(index_max)):
                        similarity_max.append(self.results[i][index_max[u]])
                  
                    # thuc hien sort
                    if (len(index_max)>2):
                        for n in range(len(index_max)-1):
                            for m in range(1,len(index_max)):
                                if similarity_max[n]<similarity_max[m]:
                                    tmp = similarity_max[n]
                                    similarity_max[n] = similarity_max[m]
                                    similarity_max[m] = tmp

                                    tmp1 = value_max[n]
                                    value_max[n] = value_max[m]
                                    value_max[m] = tmp1
                    if (len(index_max)>=2):
                        self.utility_matrix[j][i] = (similarity_max[0]*value_max[0] + similarity_max[1]*value_max[1]) / (abs(similarity_max[0])+abs(similarity_max[1]))
        print(np.array(self.utility_matrix))

    @classmethod
    def suggestCourse(self,user):
        self.predictUser()

        users = User.objects.order_by("id").values("id")
        ids = [user['id'] for user in users]
        index = ids.index(user)
       
        courses = Course.objects.filter(status="public").order_by("id").values("id")
        ids = [course['id'] for course in courses]

        value_rat = self.utility_matrix[:,index]
        lst = []
        tmp = []
        for i in range(len(value_rat)):
            lst.append(value_rat[i])
            tmp.append(value_rat[i])
        lst.sort()
        rs = []
        for i in range(len(lst)-5, len(lst)):
            rs.append(ids[tmp.index(lst[i])])
        return rs

                   
        

       
        



        


