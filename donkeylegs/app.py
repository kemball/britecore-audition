from flask import Flask,render_template,jsonify

app=Flask(__name__)
from orm import *


@app.route("/risks")
def list_of_types():
  return jsonify(all_risk_names())

@app.route("/risks/<risk_type>")
def one_type(risk_type=None):
  return risk_by_name(risk_type).json()



@app.route("/")
def fallback():
  return render_template("index.html")

