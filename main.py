import os
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import morph_kgc
import rdflib


app = Flask(__name__)
app.config['SECRET_KEY'] = "x633UE2xYRC"
app.config['UPLOAD_FOLDER'] = "uploads"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        mapping_file = request.files.get("mapping-file")
        # source_data_file = request.files.get("source-data")
        files = request.files.getlist("source-data")
        source_files = []
        for file in files:
            source_filename = file.filename
            if source_filename:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], source_filename))
                source_files.append(source_filename)
        # exit()
        # print(file)
        mapping_filename = secure_filename(mapping_file.filename)
        # source_filename = secure_filename(source_data_file.filename)
        if mapping_filename == '':
            flash('Please upload a Mapping File!')
            return redirect(request.url)
        if not mapping_filename.endswith(".ttl"):
            flash('Mapping file must be a Turtle file (.ttl)')
            return redirect(request.url)
        mapping_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename))
        # source_data_file.save(os.path.join(app.config['UPLOAD_FOLDER'], source_filename))
        mapping_result = execute_mapping(mapping_filename)
        rdf_generated = mapping_result.get("rdf_data")
        mapping_error = mapping_result.get("error_message")
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename))
        for file in source_files:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        print(rdf_generated)
        if mapping_error:
            flash(mapping_error)
            print(mapping_error)
            return redirect(request.url)
        return render_template("results.html",
                               rdf_generated=rdf_generated)


def execute_mapping(mapping_filename):
    output_file = "output.ttl"
    config = f"""
                [DataSource1]
                mappings: {mapping_filename}
             """
    os.chdir("./uploads")
    results = {}
    try:
        g = morph_kgc.materialize(config)
        with open(output_file, "w") as f:
            print(g.serialize(format="turtle"), file=f)
            results["rdf_data"] = g.serialize(format="turtle").strip()
    except Exception as e:
        results["error_message"] = str(e)
        print(e)
    os.chdir("..")
    return results



@app.route('/search-graph', methods=["GET", "POST"])
def search_graph():
    query_parameter = request.form.get("query_parameter")
    graph_uri = request.form.get("graph_uri")
    print(query_parameter, graph_uri)
    # SPARQL query executed on endpoint
    # {query_parameter} is replaced by the term entered into the interface
    sparql_query = """
    PREFIX crm: <http://erlangen-crm.org/current/>
    PREFIX vrti: <http://ont.virtualtreasury.ie/ontology#>
    SELECT DISTINCT ?person ?occupation ?gender
    WHERE {
      ?person ?predicate ?object; 
          crm:P1_is_identified_by ?name;
           crm:P2_has_type  ?gender;
          a crm:E21_Person .
      ?occupation crm:P107_has_current_or_former_member ?person ;
                  rdfs:label ?occupationName   .
      ?name rdfs:label ?nameLabel  ;
            a   crm:E41_Appellation  . 
      FILTER CONTAINS(LCASE(?nameLabel),'{query_parameter}')     
     }
    LIMIT 100
    """
    sparql_query = sparql_query.replace("{query_parameter}", query_parameter.lower())
    table_rows = {}
    try:
        sparql = SPARQLWrapper(graph_uri)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        row_count = 0
        sparql_variables = sorted(results["head"]["vars"])
        print(f"The following variables are returned by the SPARQL query: {sparql_variables}")
        for result in results["results"]["bindings"]:
            new_row = {}
            for variable in sparql_variables:
                if result.get(variable):
                    current_value = result.get(variable).get("value")
                    new_row[variable] = current_value
            table_rows[row_count] = new_row
            row_count += 1
        print(f"The results of the query: {table_rows}")
        print(f"The SPARQL query executed:\n {sparql_query}")
        return table_rows
    except Exception as e:
        exception_message = f"Exception: {e}"
        print(exception_message)
        return exception_message


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
