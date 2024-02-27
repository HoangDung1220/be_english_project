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
            values = []
            for user in users:
                ratings = RatingCourse.objects.filter(course__id = course['id'], user__id= user['id']).values("rating")
                if (len(ratings)>0):
                    values.append(ratings[0]['rating'])
                else:
                    values.append(0)
            self.matrix_ratings.append(values)
            self.values = np.array(self.matrix_ratings)
 

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
        print(rs)
        return rs





        


