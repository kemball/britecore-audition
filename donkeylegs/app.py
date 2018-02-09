from flask import Flask,render_template,jsonify,g,make_response,url_for
import flask as f
class sneakyFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
      block_start_string='<%',
      block_end_string='%>',
      variable_start_string='%%',
      variable_end_string='%%',
      comment_start_string='<#',
      comment_end_string='#>'))


app=sneakyFlask(__name__)


from orm import *


@app.route("/risks",methods=['GET'])
def list_of_types():
  names = all_risk_names()
  return make_response(jsonify([{"name":name} for name in names]),200)

@app.route("/risks",methods=['PUT'])
def update():
  #update existing risk_type with request data
  return make_response("",200)

@app.route("/risks",methods=['POST'])
def make_new():
  #make new risk_type with request data
  return make_response("",201)



@app.route("/risks/<risk_type>",methods=['GET'])
def one_type(risk_type=None):
  print("fetching risk: ",risk_type)
  risk = risk_by_name(risk_type)
  if risk:
    return make_response(risk.json(),200)
  else:
    return make_response(jsonify({"error":"not found"}),404)

@app.route("/risks/<risk_type>",methods=['DELETE'])
def delete_existing(risk_name=None):
  if risk_name is None:
    return make_response(jsonify({"error":"not found"}),404)
  risk_type = risk_by_name(risk_name)
  if risk_type:
    risk_type.delete()
    return make_response("",204)
  else:
    return make_response(jsonify({"error":"not found"}),404)

@app.route("/health")
def health():
  return "1"

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/<path:path>')
def fallback(path):
  return f.redirect(f.url_for('index'),302)

