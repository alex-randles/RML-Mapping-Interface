import os
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import morph_kgc
import rdflib


app = Flask(__name__)
app.config['SECRET_KEY'] = "x633UE2xYRC"
app.config['UPLOAD_FOLDER'] = "uploads"

@app.route('/', methods=["GET", "POST"])
def index():
    # the main endpoint for the interface
    if request.method == "GET":
        # returns the initial view
        return render_template("index.html")
    else:
        # returns the result page of the mapping process
        mapping_file = request.files.get("mapping-file")
        # source_data_file = request.files.get("source-data")
        mapping_filename = secure_filename(mapping_file.filename)
        # check mapping is uploaded and is a turtle file
        if mapping_filename == '':
            flash('Please upload a Mapping File!')
            return redirect(request.url)
        if not mapping_filename.endswith(".ttl"):
            flash('Mapping file must be a Turtle file (.ttl)')
            return redirect(request.url)
        # save mapping file
        mapping_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename))
        files = request.files.getlist("source-data")
        source_files = []
        # save each source file uploaded
        for file in files:
            source_filename = file.filename
            if source_filename:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], source_filename))
                source_files.append(source_filename)
        # compare the source files defined in mapping to uploaded files
        file_errors = compare_mapping_sources(mapping_filename, source_files)
        # execute the mapping and retrieve RDF data and any error messages
        mapping_result = execute_mapping(mapping_filename)
        rdf_generated = mapping_result.get("rdf_data")
        mapping_error = mapping_result.get("error_message")
        print(rdf_generated)
        print(mapping_error)
        # remove the files from server
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename))
        for file in source_files:
            pass
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        # check if any source files defined in mapping were not uploaded
        if file_errors:
            # join returned list of source files not uploaded and create a HTML list to display
            file_listing = "<ul>"
            for file_name in file_errors:
                file_listing += f"<li> {file_name} </li>"
            file_listing += "</ul>"
            file_error_message = f"The following source file(s) were not uploaded: {file_listing}"
            flash(file_error_message)
            return redirect(request.referrer)
        if mapping_error:
            # returns a list with source files defined in mapping but not uploaded
            flash(mapping_error)
            return redirect(request.referrer)
        return render_template("results.html",
                               rdf_generated=rdf_generated)


def compare_mapping_sources(mapping_filename, uploaded_sources):
    # compares each mapping source to uploaded source files
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename)
    mapping_graph = rdflib.Graph().parse(file_path, format="ttl")
    query = """
    PREFIX rml: <http://w3id.org/rml/>
    SELECT DISTINCT ?sourceName
    WHERE { 
        ?subject rml:source ?sourceName . 
        FILTER(isLiteral(?sourceName)) 
    }
    """
    query_results = mapping_graph.query(query)
    source_names = []
    # store source names retrieved from SPARQL query
    for row in query_results:
        current_source = str(row.get("sourceName"))
        source_names.append(current_source)
    # compare sources from query result to uploaded files
    file_error_message = []
    for source in source_names:
        if source not in uploaded_sources:
            file_error_message.append(source)
    return file_error_message


def execute_mapping(mapping_filename):
    # creates the config string and executes the morph kgc engine and outputs.ttl
    output_file = "output.ttl"
    config = f"""
                [DataSource1]
                mappings: {mapping_filename}
             """
    os.chdir("uploads")
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


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)