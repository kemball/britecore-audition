from flask import Flask,render_template,jsonify,g

app=Flask(__name__)
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

@app.route("/test/<risk_type>")
def test(risk_type=None):
  thisrisk = risk_by_name(risk_type)
  if thisrisk is not None:
    print(risk_type," ",thisrisk.name)
    thisrisk.name += " 1"
    if thisrisk.save():
      return "saved successfully"
    else:
      return "oh no something bad"
  else:
    return "risk not found"




@app.route("/")
def fallback():
  return render_template("index.html")

