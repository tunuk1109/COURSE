from rest_framework import viewsets, generics, permissions, status
from urllib3 import request

from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import CoursePagination, ExamPagination, CategoryPagination
from .permissions import CheckStudent, CheckTeacher
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'detail': f'{e}, Maalymat tuura emes'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': f'Oshibka v servere, {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'detail': f'Oshibka v servere, {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'detail': 'Key tuura emes'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Oshibka v servere, {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return UserProfile.objects.filter(id=self.request.user.id)
        except Exception as e:
            return Response({'detail': f'Server, {e}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckTeacher]


class TeacherCreateAPIView(generics.CreateAPIView):
    serializer_class = TeacherSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            teacher = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'detail': f'{e}, Maalymat tuura emes berildi'}, status.HTTP_400_BAD_REQUEST)
        except NameError as e:
            return Response({'detail': f'{e}, Oshibka v kode'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'detail': 'Server ne rabotaet'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckStudent]


class StudentCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, CheckStudent]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = CategoryPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryCreateAPIView(generics.CreateAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['course_name']
    ordering_fields = ['price']
    pagination_class = CoursePagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated, CheckTeacher]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, CheckTeacher]


class CertificateCreateAPIView(generics.CreateAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated, CheckTeacher]


class AssignmentCreateAPIView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, CheckTeacher]


class ExamListAPIView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamListSerializer
    pagination_class = ExamPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExamCreateAPIView(generics.CreateAPIView):
    serializer_class = ExamListSerializer
    permission_classes = [permissions.IsAuthenticated, CheckTeacher]


class QuestionsCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionsSerializer
    permission_classes = [permissions.IsAuthenticated, CheckTeacher]


class OptionCreateAPIView(generics.CreateAPIView):
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticated, CheckTeacher]


class ExamDetailAPIView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamDetailSerializer
    pagination_class = ExamPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class CourseReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckStudent]


class TeacherRatingViewSet(viewsets.ModelViewSet):
    queryset = TeacherRating.objects.all()
    serializer_class = TeacherRatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckStudent]

    def get_queryset(self):
        return TeacherRating.objects.filter(student_user=self.request.user)


class TeacherRatingCreateAPIView(generics.CreateAPIView):
    serializer_class = TeacherRatingSerializer
    permission_classes = [permissions.IsAuthenticated, CheckStudent]

    def get_queryset(self):
        return TeacherRating.objects.filter(student_user=self.request.user)


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(student__user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(student__user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__student__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(student__user=self.request.user)
        serializer.save(cart=cart)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]









































































