

import sqlite3

from flask import g,jsonify
from app import app

DATABASE = './database.db'

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()




class RiskType:
  def __init__(self):
    self.fields = []
    self.name = ""

  def json(self):
    return jsonify((self.name,self.fields))






def all_risk_names():
  cur = get_db().execute('select distinct name from risk_types;')
  return [x[0] for x in cur.fetchall()]

def risk_by_name(name):
  print(name)
  cur = get_db().execute("""
                    select
                      risk_types.name,
                      fields.name,
                      field_types.name
                    from
                      fields
                      left join field_types on fields.type==field_types.id
                      left join risk_types on fields.parent_risk==risk_types.id
                    where
                      risk_types.name == ?;""",(name,))
  named_risk = RiskType()
  named_risk.name = name
  for (name,field_name,field_type) in cur.fetchall():
    named_risk.fields.append((field_name,field_type))
  return named_risk
