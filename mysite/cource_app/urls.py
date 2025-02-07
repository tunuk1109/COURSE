from rest_framework import routers
from .views import *
from django.urls import path, include



router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users_list'),
router.register(r'teacher', TeacherViewSet, basename='teacher_list'),
router.register(r'student', StudentViewSet, basename='student_list'),
router.register(r'rating', TeacherRatingViewSet, basename='rating_list')
router.register(r'history', HistoryViewSet, basename='history_list'),
router.register(r'cart', CartViewSet, basename='cart_list'),
router.register(r'cart_item', CartItemViewSet, basename='cart_item_list'),
router.register(r'favorite', FavoriteViewSet, basename='favorite_list'),
router.register(r'favorite_item', FavoriteItemViewSet, basename='favorite_item_list'),



urlpatterns = [
    path('', include(router.urls)),
    path('courses/', CourseListAPIView.as_view(), name='courses_list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course_detail'),
    path('categories/', CategoryListAPIView.as_view(), name='categories_list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('lesson/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('assignment_create/', AssignmentCreateAPIView.as_view(), name='assignment_create'),
    path('certificate_create/', CertificateCreateAPIView.as_view(), name='certificate_create',),
    path('reviews_create/', CourseReviewCreateAPIView.as_view(), name='review_create'),
    path('exams/', ExamListAPIView.as_view(), name='exam_list'),
    path('exam/<int:pk>/', ExamDetailAPIView.as_view(), name='exam_detail'),
    path('teacher_create/', TeacherCreateAPIView.as_view(), name='teacher_create'),
    path('student_create/', StudentCreateAPIView.as_view(), name='student_create'),
    path('category_create/', CategoryCreateAPIView.as_view(), name='category_greate'),
    path('course_create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('exam_create/', ExamCreateAPIView.as_view(), name='exam_create'),
    path('questions_create/', QuestionsCreateAPIView.as_view(), name='questions_create'),
    path('option_create/', OptionCreateAPIView.as_view(), name='option_create'),
    path('teacher_rating_create/', TeacherRatingCreateAPIView.as_view(), name='rating_create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


]