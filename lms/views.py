from rest_framework import generics, permissions
from .serializers import *
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from .certificate_generator import generate_certificate
from .tasks import send_notification
from .models import CustomUser
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all() 
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class Login(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

    
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,  
            }

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data,  
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
# Category 
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

# Course 
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

# Course 
class CourseMaterialListCreateView(generics.ListCreateAPIView):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class CourseMaterialRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user as the currently logged-in user
        enrollment = serializer.save()
        send_notification.delay(enrollment.user.id, f"You have enrolled in {enrollment.course.title}.")
        serializer.save(user=self.request.user)

class EnrollmentRetrieveView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return enrollments for the currently logged-in user
        return Enrollment.objects.filter(user=self.request.user)
    


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class PaymentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            charge = stripe.Charge.create(
                amount=data['amount'],  # Amount in cents
                currency='usd',
                description='Course enrollment fee',
                source=data['source'],  # obtained with Stripe.js
            )
            return Response({'charge_id': charge.id}, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ThreadListCreateView(generics.ListCreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ThreadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ReplyListCreateView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ReplyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProgressListCreateView(generics.ListCreateAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProgressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class GenerateCertificateView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_id):
        progress = Progress.objects.filter(user=request.user, course_id=course_id).first()
        if not progress or progress.progress_percentage < 100:
            return Response({"error": "Course not completed yet."}, status=400)

        user_name = request.user.username
        course_title = progress.course.title
        output_path = f"certificates/{user_name}_{course_title.replace(' ', '_')}_certificate.pdf"

        generate_certificate(user_name, course_title, output_path)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename=os.path.basename(output_path))

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter notifications by the authenticated user
        return self.queryset.filter(user=self.request.user)
    
class AdminDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Fetch statistics
        total_users = User.objects.count()
        total_courses = Course.objects.count()
        total_enrollments = Enrollment.objects.count()
        total_notifications = Notification.objects.filter(is_read=False).count()
        
        # Calculate course completion rates
        completed_courses = Enrollment.objects.filter(is_completed=True).count()
        completion_rate = (completed_courses / total_courses * 100) if total_courses > 0 else 0

        # Fetch quiz results (example; adjust according to your models)
        total_quizzes = Quiz.objects.count()
        
        data = {
            'total_users': total_users,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'unread_notifications': total_notifications,
            'completion_rate': completion_rate,
            'total_quizzes': total_quizzes,
        }
        return Response(data)
    
class AnalyticsView(APIView):
    def get(self, request):
        # Course performance metrics
        courses = Course.objects.annotate(
            total_enrollments=Count('enrollment'),
            completion_rate=Avg('enrollment__is_completed'),
            average_score=Avg('enrollment__score')
        )

        course_data = [
            {
                'title': course.title,
                'total_enrollments': course.total_enrollments,
                'completion_rate': course.completion_rate * 100 if course.completion_rate is not None else 0,
                'average_score': course.average_score or 0,
            }
            for course in courses
        ]

        # User engagement metrics
        active_users_count = Enrollment.objects.values('user').distinct().count()

        data = {
            'courses': course_data,
            'active_users_count': active_users_count,
        }
        
        return Response(data)