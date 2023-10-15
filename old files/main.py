import os
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request, flash, redirect, url_for, session
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
        # print("testing")
        # print(request.files.get('mapping-file'))
        # exit()
        mapping_file = request.files.pop("mapping-file")
        files = request.files.getlist("source-data")
        source_files = []
        print(mapping_file)
        for file in files:
            print(file)
            source_filename = file.filename
            if source_filename:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], source_filename))
                source_files.append(source_filename)
        if not mapping_file:
            return 'Please upload a Mapping File!'
        mapping_filename = secure_filename(mapping_file.filename)
        if not mapping_filename.endswith(".ttl"):
            return 'Mapping file must be a Turtle file (.ttl)'
        mapping_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename))
        # exit()
        mapping_result = execute_mapping(mapping_filename)
        rdf_generated = mapping_result.get("rdf_data")
        mapping_error = mapping_result.get("error_message")
        # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], mapping_filename))
        for file in source_files:
            pass
            # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        print(rdf_generated)
        if mapping_error:
            # flash(mapping_error)
            print(mapping_error)
            return mapping_error
        session["rdf_generated"] = rdf_generated
        return redirect(url_for("result"))
        # return {"html": render_template("results.html",
        #                        rdf_generated=rdf_generated) }


@app.route('/result', methods=["GET", "POST"])
def result():
    rdf_generated = session.get("rdf_generated")
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


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
