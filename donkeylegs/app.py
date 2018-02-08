from flask import Flask,render_template,jsonify,g
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


@app.route("/risks")
def list_of_types():
  return jsonify(all_risk_names())

@app.route("/risks/<risk_type>")
def one_type(risk_type=None):
  risk = risk_by_name(risk_type)
  if risk:
    return risk.json()
  else:
    return ""





@app.route("/")
def fallback():
  return render_template("index.html")

