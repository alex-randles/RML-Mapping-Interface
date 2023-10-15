import rdflib

def compare_mapping_sources(mapping_filename, uploaded_sources):
    # file_path = os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename)
    file_path = mapping_filename
    mapping_graph = rdflib.Graph().parse(file_path, format="ttl")
    query = """
    SELECT DISTINCT ?sourceName
    WHERE { ?subject rml:source ?sourceName . }
    """
    query_results = mapping_graph.query(query)
    source_names = []
    # store source names retrieved from SPARQL query
    for row in query_results:
        current_source = str(row.get("sourceName"))
        source_names.append(current_source)
    # compare sources in mapping to uploaded files
    file_error_message = []
    for source in source_names:
        if source not in uploaded_sources:
            file_error_message.append(source)
    print(file_error_message)

uploaded_sources = ['weatherstations.csv']
compare_mapping_sources("static/uploads/mapping.ttl", uploaded_sources)