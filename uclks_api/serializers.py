from rest_framework import serializers
from .models import DepartmentModule, Departments, Modules, Feedback

class DepartmentModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentModule
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
