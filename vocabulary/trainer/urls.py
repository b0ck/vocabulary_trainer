from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lesson/<int:lesson_id>/', views.show_question, name='lesson_view'),
    path('evaluate', views.evaluate_question, name='evaluate_question'),
    path('reset', views.reset_lesson_results, name='reset_lesson')
]
