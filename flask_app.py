import io
import yaml
import json
from flask import Flask, render_template, request, Response, url_for, jsonify
from textfsm import TextFSM

app = Flask(__name__, static_url_path="/static")
app.config["JSON_SORT_KEYS"] = False


config = {"name": "TextFSM", "data": "RAW", "rendered": "JSON"}


@app.route("/")
def index():
    return render_template("index.html", **config)


@app.route("/examples")
def examples():
    try:
        with open("examples.yaml", "r") as f:
            data = yaml.safe_load(f)
        resp = jsonify(data)
    except Exception as e:
        resp = jsonify({"error": f"Error {type(e).__name__}", "msg": str(e)})
        resp.status_code = 400
    finally:
        return resp


@app.route("/rend", methods=["POST"])
def rend():
    data = request.get_json()
    if not isinstance(data, dict):
        resp = jsonify({"error": "Invalid JSON"})
        resp.status_code = 400
        return resp
    textFSM_template = data.get("template", "")
    raw_data = data.get("data")

    try:
        template = io.StringIO(textFSM_template)
        parser = TextFSM(template)
        output = parser.ParseTextToDicts(text=raw_data)

        resp = jsonify({"result": json.dumps(output, indent=2)})
    except Exception as e:
        breakpoint()
        resp = jsonify({"error": f"Error {type(e).__name__}", "msg": str(e)})
        resp.status_code = 400
    finally:
        return resp


if __name__ == "__main__":
    app.run(debug=True)
