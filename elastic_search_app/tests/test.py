from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model

@patch('elastic_search_app.views.OctoxlabsJWTAuthentication.authenticate', return_value=(None, None))
@patch('elastic_search_app.views.IsAuthenticated.has_permission', return_value=True)
class CreateIndexViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('elastic_search_app.views.create_index_with_mapping')
    def test_create_index_success(self, mock_create_index, mock_has_permission, mock_authenticate):
        url = reverse('create_index')
        data = {
            "index_name": "test_index",
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "hostname": {"type": "text"},
                    "ip": {"type": "ip"}
                }
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertTrue(mock_create_index.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], f"Index {data['index_name']} created successfully.")

    def test_create_index_no_index_name(self, mock_authenticate, mock_has_permission):
        url = reverse('create_index')
        data = {}  # Missing index_name
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Index name is required.")

@patch('elastic_search_app.views.OctoxlabsJWTAuthentication.authenticate', return_value=(None, None))
@patch('elastic_search_app.views.IsAuthenticated.has_permission', return_value=True)
class AddDataViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser2', password='testpassword2')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('elastic_search_app.views.add_document_to_index')
    def test_add_data_success(self, mock_add_document, mock_has_permission, mock_authenticate):
        url = reverse('add_data')
        data = {
            "index_name": "test_index",
            "data": [
                {"hostname": "example.com", "ip": "192.168.1.1"},
                {"hostname": "testsite.com", "ip": "192.168.1.2"}
            ]
        }
        response = self.client.post(url, data, format='json')

        self.assertTrue(mock_add_document.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], f"Data added to {data['index_name']} successfully.")

    def test_add_data_invalid_input(self, mock_authenticate, mock_has_permission):
        url = reverse('add_data')
        data = {
            "index_name": "",  # Invalid (empty) index name
            "data": "not a list"  # Invalid data format
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid index name or data format.")

class GetDocumentViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser3', password='testpassword3')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('elastic_search_app.views.get_document')
    def test_get_document_success(self, mock_get_document):
        mock_get_document.return_value = {"hostname": "example.com", "ip": "192.168.1.1"}
        url = reverse('get_document')
        params = {
            "index_name": "test_index",
            "document_id": "1"
        }
        response = self.client.get(url, params)

        self.assertTrue(mock_get_document.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("document", response.data)
        self.assertEqual(response.data["document"], mock_get_document.return_value)

    def test_get_document_missing_parameters(self):
        url = reverse('get_document')
        # Missing both index_name and document_id
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Index name and document ID are required.")

    @patch('elastic_search_app.views.get_document', return_value=None)
    def test_get_document_not_found(self, mock_get_document):
        url = reverse('get_document')
        params = {
            "index_name": "test_index",
            "document_id": "nonexistent"
        }
        response = self.client.get(url, params)

        self.assertTrue(mock_get_document.called)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Document not found.")

class SearchViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='searchuser', password='searchpassword')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('elastic_search_app.views.search_documents')
    def test_search_success(self, mock_search_documents):
        mock_search_documents.return_value = [{"hostname": "example.com", "ip": "192.168.1.1"}]
        url = reverse('search')
        params = {
            "index_name": "test_index",
            "hostname": "example"
        }
        response = self.client.get(url, params)

        self.assertTrue(mock_search_documents.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"], mock_search_documents.return_value)

    def test_search_missing_parameters(self):
        url = reverse('search')
        # Missing index_name and hostname
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Both index_name and hostname are required.")

    @patch('elastic_search_app.views.search_documents')
    def test_search_exception(self, mock_search_documents):
        mock_search_documents.side_effect = Exception("Unexpected error")
        url = reverse('search')
        params = {
            "index_name": "test_index",
            "hostname": "failsearch"
        }
        response = self.client.get(url, params)

        self.assertTrue(mock_search_documents.called)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Unexpected error")

class MappingViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='mappinguser', password='mappingpassword')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('elastic_search_app.views.get_index_mapping')
    def test_get_mapping_success(self, mock_get_index_mapping):
        mock_mapping_data = {"properties": {"hostname": {"type": "text"}, "ip": {"type": "ip"}}}
        mock_get_index_mapping.return_value = mock_mapping_data
        url = reverse('mapping')
        params = {"index_name": "test_index"}
        response = self.client.get(url, params)

        self.assertTrue(mock_get_index_mapping.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("mapping", response.data)
        self.assertEqual(response.data["mapping"], mock_mapping_data)

    def test_get_mapping_missing_index_name(self):
        url = reverse('mapping')
        response = self.client.get(url)  # No index_name parameter provided

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "index_name parameter is required.")

    @patch('elastic_search_app.views.get_index_mapping')
    def test_get_mapping_exception(self, mock_get_index_mapping):
        mock_get_index_mapping.side_effect = Exception("Unexpected error")
        url = reverse('mapping')
        params = {"index_name": "test_index"}
        response = self.client.get(url, params)

        self.assertTrue(mock_get_index_mapping.called)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Unexpected error")