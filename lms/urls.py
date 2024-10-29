from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),
    path('course-materials/', CourseMaterialListCreateView.as_view(), name='course-material-list-create'),
    path('course-materials/<int:pk>/', CourseMaterialRetrieveUpdateDestroyView.as_view(), name='course-material-detail'),
    path('enrollments/', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('enrollments/me/', EnrollmentRetrieveView.as_view(), name='my-enrollments'),  # Get enrollments for the logged-in user
    path('payment/', PaymentView.as_view(), name='payment'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz-detail'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-detail'),
    path('threads/', ThreadListCreateView.as_view(), name='thread-list-create'),
    path('threads/<int:pk>/', ThreadRetrieveUpdateDestroyView.as_view(), name='thread-detail'),
    path('replies/', ReplyListCreateView.as_view(), name='reply-list-create'),
    path('replies/<int:pk>/', ReplyRetrieveUpdateDestroyView.as_view(), name='reply-detail'),
    path('progress/', ProgressListCreateView.as_view(), name='progress-list-create'),
    path('progress/<int:pk>/', ProgressRetrieveUpdateDestroyView.as_view(), name='progress-detail'),
    path('generate-certificate/<int:course_id>/', GenerateCertificateView.as_view(), name='generate-certificate'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('api/admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
