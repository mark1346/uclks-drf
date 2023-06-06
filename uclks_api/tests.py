from rest_framework.test import APITestCase
from .models import DepartmentModule, Departments, Modules, Feedback
from .serializers import (
    DepartmentModuleSerializer,
    DepartmentSerializer,
    ModuleSerializer,
    FeedbackSerializer,
)
from django.urls import reverse
from rest_framework import status
from .models import Departments, Modules, DepartmentModule, Feedback
import json

class ModuleAverageAPITests(APITestCase):
    def setUp(self):
        self.module = Modules.objects.create(
            code='COMP0003',
            name='Theory of Computation'
        )
        Feedback.objects.create(
            module=self.module,
            is_compulsory=1,
            module_difficulty=5,
            amount_of_assignments=1,
            exam_difficulty=5,
            tips='힘들어요. 많이. 족보 많이 풀어보세요',
            evaluation=5,
            comments='컴싸 1학년 모듈 중 가장 어려운 모듈입니다. 힘내세요. 생각보다 점수는 꽤 잘 줍니다.'
        )
        Feedback.objects.create(
            module=self.module,
            is_compulsory=1,
            module_difficulty=4,
            amount_of_assignments=1,
            exam_difficulty=4,
            tips='어려운데 구글링하면서 공부하면 할 만 해요',
            evaluation=3,
            comments='개념 이해 먼저 해야돼요. 그래야 과제도 잘 할 수 있어요. 시험은 생각보다 쉬워요.'
        )
    
    def test_get_module_average(self):
        url = reverse('module-average', kwargs={'id': self.module.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['evaluation'], 4)
        self.assertEqual(response.data['module_difficulty'], 4.5)
        self.assertEqual(response.data['amount_of_assignments'], 1)
        self.assertEqual(response.data['exam_difficulty'], 4.5)

    def test_get_module_average_not_found(self):
        url = reverse('module-average', kwargs={'id': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Module not found')
    
class ModuleDetailAPITests(APITestCase):
    def setUp(self):
        self.module = Modules.objects.create(
            code='COMP0003',
            name='Theory of Computation'
        )
        Feedback.objects.create(
            module=self.module,
            is_compulsory=1,
            module_difficulty=5,
            amount_of_assignments=1,
            exam_difficulty=5,
            tips='힘들어요. 많이. 족보 많이 풀어보세요',
            evaluation=5,
            comments='컴싸 1학년 모듈 중 가장 어려운 모듈입니다. 힘내세요. 생각보다 점수는 꽤 잘 줍니다.'
        )
        Feedback.objects.create(
            module=self.module,
            is_compulsory=1,
            module_difficulty=4,
            amount_of_assignments=1,
            exam_difficulty=4,
            tips='어려운데 구글링하면서 공부하면 할 만 해요',
            evaluation=4,
            comments='개념 이해 먼저 해야돼요. 그래야 과제도 잘 할 수 있어요. 시험은 생각보다 쉬워요.'
        )
        
    def test_get_module_details_recent_true(self):
        # Set up the URL for the API endpoint
        url = reverse('module-detail', args=[self.module.id])
        # Send a GET request with "recent" parameter as "true"
        response = self.client.get(url, {'recent': 'true'})
        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify the order of feedbacks (most recent first)
        self.assertEqual(
            response.data['feedbacks'][0]['module_difficulty'], 4
        )
        self.assertEqual(
            response.data['feedbacks'][1]['module_difficulty'], 5
        )
        # print("response: ", response.data)

    def test_get_module_details_recent_false(self):
        # Set up the URL for the API endpoint
        url = reverse('module-detail', args=[self.module.id])
        # Send a GET request with "recent" parameter as "false"
        response = self.client.get(url, {'recent': 'false'})
        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify the order of feedbacks (oldest first)
        self.assertEqual(
            response.data['feedbacks'][0]['module_difficulty'], 5
        )
        self.assertEqual(
            response.data['feedbacks'][1]['module_difficulty'], 4
        )
        
        
class DepartmentAPITest(APITestCase):
    def test_get_departments(self):
        # Create test departments
        department1 = Departments.objects.create(name='Computer Science')
        department2 = Departments.objects.create(name='Pharmacy')
        department3 = Departments.objects.create(name='Mathematics')

        # Define the expected data
        expected_data = [
            {
                'id': department1.id,
                'name': department1.name,
            },
            {
                'id': department2.id,
                'name': department2.name,
            },
            {
                'id': department3.id,
                'name': department3.name,
            }
        ]

        # Set the query parameters
        keyword = ''
        descending = False

        # Build the URL with query parameters
        url = reverse('departments-list') + '?keyword={}&descending={}'.format(keyword, descending)

        # Make the GET request
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Trim created_at and updated_at from the response data
        trimmed_response_data = [
            {'id': item['id'], 'name': item['name']}
            for item in response.data
        ]
        trimmed_response_data = json.loads(json.dumps(trimmed_response_data))
        
        # Assert the response data matches the expected data
        # print("response.data", trimmed_response_data)
        self.assertEqual(trimmed_response_data, expected_data)

    def test_get_department(self):
        # Create a test department
        department = Departments.objects.create(name='Test Department')

        # Build the URL for the specific department
        url = reverse('department-detail', args=[department.id])

        # Make the GET request
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data matches the department data
        self.assertEqual(response.data['id'], department.id)
        self.assertEqual(response.data['name'], department.name)
        # Add other assertions for department fields as needed
