from django.urls import path
from .views import (
    DepartmentListAPIView,
    DepartmentDetailAPIView,
    ModuleDetailAPIView,
    ModuleAverageAPIView,
)

urlpatterns = [
    path('departments/search', DepartmentListAPIView.as_view(), name='departments-list'),
    path('departmentDetail/<int:pk>', DepartmentDetailAPIView.as_view(), name='department-detail'),
    path('modules/<int:id>', ModuleDetailAPIView.as_view(), name='module-detail'),
    path('modules/<int:id>/average', ModuleAverageAPIView.as_view(), name='module-average'),
]
