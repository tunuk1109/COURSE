from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
       try:
           user = UserProfile.objects.create_user(**validated_data)
           return user
       except Exception as e:
           return f'{e} Oshinbka pri sohranenii dannyh'

    def to_representation(self, instance):
        try:
            refresh = RefreshToken.for_user(instance)
            return {
                'user': {
                    'username': instance.username,
                    'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        except Exception as e:
            return f'{e} Oshibka pri sozdanii tokena'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        try:
            refresh = RefreshToken.for_user(instance)
            return {
                'user': {
                    'username': instance.username,
                    'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        except Exception as e:
            return f'{e} Oshibka pri sozdanii tokena'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'video', 'content']


class AssignmentSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = ['certificate_url',]


class ReviewStudentInfoSerializer(serializers.ModelSerializer):
    user = UserProfileCourseSerializer()

    class Meta:
        model = Student
        fields=  ['user']


class CourseReviewSerializer(serializers.ModelSerializer):
    user = ReviewStudentInfoSerializer()

    class Meta:
        model = CourseReview
        fields = ['id', 'text', 'stars', 'user']


class CourseCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name']


class CourseListSerializer(serializers.ModelSerializer):
    author = UserProfileCourseSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    get_change_price = serializers.SerializerMethodField()
    count_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_image', 'level', 'type_course',
                  'price', 'get_change_price', 'old_price', 'author', 'avg_rating', 'count_people', 'count_lesson']

    def get_avg_rating(self, obj):
        try:
            return obj.get_avg_rating()
        except Exception as e:
            return f'{e}, Oshibka pri sozdanii funksii get_avg_rating'

    def get_count_people(self, obj):
        try:
            return obj.get_count_people()
        except Exception as e:
            return f'{e} Osibka funksii get_count_people'

    def get_change_price(self, obj):
        try:
            return obj.get_change_price()
        except Exception as e:
            return f'{e} Oshibka funksii get_change_price'

    def get_count_lesson(self, obj):
        try:
            return obj.get_count_lesson()
        except Exception as e:
            return f'{e} Osibka funksii get_count_lesson'


class CourseDetailSerializer(serializers.ModelSerializer):
    author = UserProfileCourseSerializer(many=True)
    category = CategoryCourseSerializer(many=True)
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    updated_ap = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    course_lesson = LessonSerializer(many=True, read_only=True)
    course_assignment = AssignmentSerializer(many=True, read_only=True)
    certificate_course = CertificateSerializer(many=True, read_only=True)
    course_review = CourseReviewSerializer(many=True, read_only=True)


    class Meta:
        model = Course
        fields = ['course_name', 'description', 'category', 'course_image', 'author', 'level', 'price', 'course_certificate',
                  'created_at', 'updated_ap',  'avg_rating', 'count_people', 'course_lesson',
                  'course_assignment', 'certificate_course', 'course_review']

    def get_avg_rating(self, obj):
        try:
            return obj.get_avg_rating()
        except Exception as e:
            return f'{e} Oshibka funksii get_avg_rating'

    def get_count_people(self, obj):
        try:
            return obj.get_count_people()
        except Exception as e:
            return f'{e} Oshibka funksii get_count_people'


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_course = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_course']


class ExamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'title', 'end_time']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['variants', 'option_check']


class QuestionsSerializer(serializers.ModelSerializer):
    question_option = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ['title', 'score', 'question_option']


class ExamDetailSerializer(serializers.ModelSerializer):
    exam_questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['title', 'exam_questions']



class TeacherRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRating
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    student = ReviewStudentInfoSerializer()
    course = CourseCartSerializer()
    date = serializers.DateTimeField(format('%d-%B-%Y %H:%M'))

    class Meta:
        model = History
        fields = ['id', 'student', 'course', 'date']


class CartItemSerializer(serializers.ModelSerializer):
    course = CourseCartSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')


    class Meta:
        model = CartItem
        fields = ['id', 'course', 'course_id', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    get_total_price = serializers.SerializerMethodField()
    student = ReviewStudentInfoSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'student', 'get_total_price']

    def get_total_price(self, obj):
        try:
            return obj.get_total_price()
        except Exception as e:
            return f'{e} Oshibka funksii get_total_price'


class FavoriteItemSerializer(serializers.ModelSerializer):
    course = CourseCartSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')


    class Meta:
        model = FavoriteItem
        fields = ['id', 'course', 'course_id']


class FavoriteSerializer(serializers.ModelSerializer):
    favorite_items = FavoriteItemSerializer(many=True, read_only=True)
    get_favorite_item = serializers.SerializerMethodField()
    student = ReviewStudentInfoSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'student', 'favorite_items', 'get_favorite_item']

    def get_favorite_item(self, obj):
        try:
            return obj.get_favorite_item()
        except Exception as e:
            return f'{e} Oshibka funksii get_favorite_item'













































































































