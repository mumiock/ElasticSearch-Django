from elasticsearch_dsl import Document, Text, Keyword, Ip, Index, connections, Search, Q
from elasticsearch import Elasticsearch

connections.create_connection(hosts=['https://localhost:9200'])

class MyDocument(Document):
    hostname = Text(fields={'raw': Keyword()})
    ip = Ip()

    class Index:
        name = 'default_index'

def get_index_mapping(index_name):
    """
    Retrieves the mapping of a specific Elasticsearch index.

    :param index_name: The name of the Elasticsearch index.
    :return: The mapping of the index as a dictionary.
    """
    try: 
        client = Elasticsearch()
        mapping = client.indices.get_mapping(index=index_name)
        return mapping
    except Exception as e:
        return None 

def create_index_with_mapping(index_name, settings=None, mappings=None):
    """
    Create an index with the given name, settings, and mappings.
    
    :param index_name: The name of the index to create.
    :param settings: The settings for the index.
    :param mappings: The mappings for the index.
    """
    try:
        index = Index(index_name)
        if settings:
            index.settings(**settings)
        if mappings:
            index.mapping(mappings)
        index.create()
    except Exception as e:
        return None 
    
def add_document_to_index(index_name, data_list):
    """
    Adds a list of documents to a specific index.
    
    :param index_name: The name of the index to add documents to.
    :param data_list: A list of dictionaries, each representing a document.
    """
    try:
        MyDocument.Index.name = index_name
        MyDocument.init(index=index_name)
        
        for data in data_list:
            hostname = data.get('Hostname')
            ips = data.get('Ip', [])
            if not hostname or not ips:
                continue 
            ip_address = ips[0]
            
            doc = MyDocument(hostname=hostname, ip=ip_address)
            doc.save(index=index_name) 
    except Exception as e:
        return None 
    
def get_document(index_name, doc_id):
    """
    Retrieves a document by ID from a specific index.

    :param index_name: The name of the index to retrieve the document from.
    :param doc_id: The ID of the document to retrieve.
    :return: The document as a dictionary, or None if not found.
    """
    try:
        MyDocument.Index.name = index_name
        document = MyDocument.get(id=doc_id, index=index_name)
        return document.to_dict()
    except Exception as e:
        return None
    
def search_documents(index_name, hostname_pattern):
    """
    Searches for documents in a specific index where the hostname matches a given pattern.

    :param index_name: The name of the Elasticsearch index to search.
    :param hostname_pattern: The pattern to match the hostname against.
    :return: A list of matching documents.
    """
    try:
        search = Search(index=index_name)

        query = Q("wildcard", hostname=hostname_pattern) | Q("match", hostname=hostname_pattern)

        response = search.query(query).execute()

        results = [hit.to_dict() for hit in response.hits]

        return results
    except Exception as e:
        return None