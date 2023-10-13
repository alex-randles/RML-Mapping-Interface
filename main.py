import os
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import morph_kgc


app = Flask(__name__)
app.config['SECRET_KEY'] = "x633UE2xYRC"
app.config['UPLOAD_FOLDER'] = "uploads"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        if os.getcwd().endswith("uploads"):
            os.chdir("..")
        mapping_file = request.files.get("mapping-file")
        source_data_file = request.files.get("source-data")
        # print(file)
        if mapping_file.filename == '' or source_data_file.filename == '':
            flash('No mapping or source data file uploaded! Both are required to execute the mapping')
            return redirect(request.url)
        mapping_filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(mapping_file.filename))
        mapping_filename = secure_filename(mapping_file.filename)
        mapping_file.save(mapping_filename)
        source_filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(source_data_file.filename))
        source_data_file.save(source_filename)
        rdf_generated = execute_mapping(mapping_filename, source_filename)
        flash("jshshss")
        print(rdf_generated)
        return render_template("results.html",
                               rdf_generated=rdf_generated)

def execute_mapping(mapping_filename, source_filename):
    # generate the triples and load them to an RDFLib graph
    mapping_file = "./SPORTS/mapping.ttl"
    output_file = "output.ttl"
    config = f"""
                [DataSource1]
                mappings: {mapping_filename}
             """
    os.chdir("./uploads")
    # print(os.getcwd())
    # exit()
    # print(config)
    # exit()
    g = morph_kgc.materialize(config)

    # work with the RDFLib graph
    with open(output_file, "w") as f:
        print(g.serialize(format="turtle"), file=f)
        return g.serialize(format="turtle")

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
