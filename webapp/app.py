import os
import tempfile
from pathlib import Path

from flask import render_template, send_file
from eve import Eve

from annodict.resource import AnnoScene


port = 5000
app = Eve(root_path=os.path.dirname(os.path.realpath(__file__)))


@app.route("/all_annoclasses", methods=["GET"])
def all_annoclasses():
    return render_template('all_annoclasses.html')


@app.route("/all_annotags", methods=["GET"])
def all_annotags():
    return render_template('all_annotags.html')


@app.route("/all_annoscenes", methods=["GET"])
def all_annoscenes():
    return render_template('all_annoscenes.html')


@app.route("/annoscene_detail/<annoscene_id>", methods=["GET"])
def annoscene_detail(annoscene_id):
    return render_template('annoscene_detail.html')


@app.route("/create_annoscene", methods=["GET"])
def create_annoscene():
    return render_template('create_annoscene.html')


@app.route("/component_demo", methods=["GET"])
def component_demo():
    return render_template('component_demo.html')


@app.route('/export_scene/<scene_id>/<export_type>')
def export_scene(scene_id, export_type):
    scene = AnnoScene.from_objectid(scene_id, f"http://localhost:{port}")

    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_file_path = Path(tmpdirname) / f'{scene_id}.{export_type}'
        if export_type == "csv":
            scene.export_csv(temp_file_path)
        elif export_type == "html":
            scene.export_html(temp_file_path, template_path="../templates/scene.html")
        else:
            raise ValueError(f"Unknown export type: {export_type}")
        
        return send_file(
            temp_file_path,
            as_attachment=True,  # This will tell the browser to download the file.
            download_name=temp_file_path.name  # Optional: specify the filename the user will see.
        )


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=port)
