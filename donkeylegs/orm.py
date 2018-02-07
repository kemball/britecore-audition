
import sqlalchemy
import json
import pymysql
from sqlalchemy import create_engine,Column,Integer,String,Table
from sqlalchemy import ForeignKey,MetaData
metadata = MetaData()
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(metadata=metadata)


from flask import g,jsonify
from app import app
with open('app_settings.json','r') as config_file:
  settings = json.load(config_file)




def pms_connect():
  return pymysql.connect(
    user=settings['db_user'],
    host=settings['db_host'],
    passwd=settings['db_pass'],
    port=settings['db_port'],
    db = settings['db_name'])


engine =create_engine("mysql+pymysql://",creator=pms_connect)
metadata.bind = engine

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = engine.connect()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class RiskType(Base):
  __tablename__="risk_types"
  name = Column('name',String(255),unique=True,nullable=False)
  id_num = Column('id',Integer,primary_key=True)

  fields=[]

  def __repr__(self):
    return '<Risk Type %s >' % self.name

  def json(self):
    return jsonify((self.name,self.fields))

  def save(self):
    print(self.name)
    with app.app_context():
      conn = get_db()
      cur = conn.execute("""insert into risk_types
                        (name)
                      values
                        (%s)""",(self.name,))
      new_id = cur.lastrowid
      insertable_fields = [(f[0],f[1],new_id) for f in self.fields]
      conn.executemany("""
                      insert into fields
                        (name,type,parent_risk)
                      values
                        (%s,(select field_types.id from field_types where name=%s),%s);
                      """,insertable_fields)
      return True


field_types = Table('field_types',metadata,
                    Column('name',String(20),unique=True,nullable=False),
                    Column('id',Integer, primary_key=True))

fields = Table('fields',metadata,
               Column('name',String(200)),
               Column('type',Integer,ForeignKey('field_types.id'),nullable=False),
               Column('parent_risk',Integer,ForeignKey('risk_types.id')))





def all_risk_names():
  rv = get_db().execute('select distinct name from risk_types;')
  return [x[0] for x in rv]

def risk_by_name(name):
  print("fetching name: ",name)
  rv = get_db().execute("""
                    select
                      risk_types.name,
                      fields.name,
                      field_types.name
                    from
                      fields
                      left join field_types on fields.type=field_types.id
                      left join risk_types on fields.parent_risk=risk_types.id
                    where
                      risk_types.name = %s;""",(name,))

  if rv.rowcount==0:
    return None
  named_risk = RiskType()
  named_risk.name = name
  for (name,field_name,field_type) in rv.fetchall():
    named_risk.fields.append((field_name,field_type))
  return named_risk
