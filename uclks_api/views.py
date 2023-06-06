from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Departments, Modules, DepartmentModule, Feedback
from .serializers import (DepartmentSerializer, ModuleSerializer, DepartmentModuleSerializer, FeedbackSerializer)
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from django.db.models import Avg


class DepartmentListAPIView(ListAPIView):
    serializer_class = DepartmentSerializer
    
    def get_queryset(self):
        keyword = self.request.GET.get('keyword', None)
        descending = self.request.GET.get('descending', None) # 이렇게 받으면 다 string으로 받아짐
        queryset = Departments.objects.all()
        
        if keyword is not None:
            # Filter departments based on the keyword
            queryset = queryset.filter(name__icontains=keyword)
        
        if descending == 'True':
            # Sort departments in descending order
            queryset = queryset.order_by('-id')

        return queryset

class DepartmentDetailAPIView(RetrieveAPIView):
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
    
    
class ModuleDetailAPIView(APIView):
    def get(self, request, id, format=None):
        recent = request.query_params.get('recent', None)
        try:
            module = Modules.objects.get(id=id)
            if recent == 'true':
                feedbacks = module.feedbacks.order_by('-created_at')
            else:
                feedbacks = module.feedbacks.order_by('created_at')
        except Modules.DoesNotExist:
            return Response({'error': 'Module Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        module_serializer = ModuleSerializer(module)
        feedback_serializer = FeedbackSerializer(feedbacks, many=True)
        
        
        return Response({
            'module': module_serializer.data, 
            'feedbacks': feedback_serializer.data,
        }, status=status.HTTP_200_OK)
        
class ModuleAverageAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            module = Modules.objects.get(id=id)
            feedbacks = module.feedbacks.all()
        except Modules.DoesNotExist:
            return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate average ratings from feedbacks
        evaluation_avg = feedbacks.aggregate(Avg('evaluation'))['evaluation__avg']
        module_difficulty_avg = feedbacks.aggregate(Avg('module_difficulty'))['module_difficulty__avg']
        amount_of_assignments_avg = feedbacks.aggregate(Avg('amount_of_assignments'))['amount_of_assignments__avg']
        exam_difficulty_avg = feedbacks.aggregate(Avg('exam_difficulty'))['exam_difficulty__avg']
        
        return Response({
            'evaluation': evaluation_avg,
            'module_difficulty': module_difficulty_avg,
            'amount_of_assignments': amount_of_assignments_avg,
            'exam_difficulty': exam_difficulty_avg
        }, status=status.HTTP_200_OK)