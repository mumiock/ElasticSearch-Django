from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .authentication import OctoxlabsJWTAuthentication
from .elasticsearch import create_index_with_mapping, add_document_to_index, get_document, search_documents, get_index_mapping
from rest_framework import status

class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        index_name = request.query_params.get('index_name')
        hostname_pattern = request.query_params.get('hostname')

        if not index_name or not hostname_pattern:
            return Response({"error": "Both index_name and hostname are required."}, status=400)

        try:
            results = search_documents(index_name, hostname_pattern)
            return Response({"results": results})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class MappingView(APIView):
    def get(self, request, *args, **kwargs):
        index_name = request.query_params.get('index_name')

        if not index_name:
            return Response({"error": "index_name parameter is required."}, status=400)

        try:
            mapping = get_index_mapping(index_name)
            return Response({"mapping": mapping})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class CreateIndexView(APIView):
    authentication_classes = [OctoxlabsJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        index_name = request.data.get('index_name')
        settings = request.data.get('settings', {})
        mappings = request.data.get('mappings', {})

        if not index_name:
            return Response({"error": "Index name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            create_index_with_mapping(index_name, settings=settings, mappings=mappings)
            return Response({"message": f"Index {index_name} created successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AddDataView(APIView):
    authentication_classes = [OctoxlabsJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        index_name = request.data.get('index_name')
        data_list = request.data.get('data')

        if not index_name or not isinstance(data_list, list):
            return Response({"error": "Invalid index name or data format."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            add_document_to_index(index_name, data_list)
            return Response({"message": f"Data added to {index_name} successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetDocumentView(APIView):
    def get(self, request, *args, **kwargs):
        index_name = request.query_params.get('index_name')
        doc_id = request.query_params.get('document_id')

        if not index_name or not doc_id:
            return Response({"error": "Index name and document ID are required."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        document = get_document(index_name, doc_id)
        if document:
            return Response({"document": document})
        else:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)