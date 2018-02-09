
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
    my_data = {"name":self.name,
              "fields":[{"name":x[0],"type":x[1]} for x in self.fields]
              }
    return jsonify(my_data)

  def save(self):
    with app.app_context():
      conn = get_db()
      cur = conn.connection.cursor()

      cur.execute("""insert into risk_types
                        (name)
                      values
                        (%s)""",(self.name,))
      conn.connection.commit()
      new_id = cur.lastrowid
      insertable_fields = [(f[0],f[1],new_id) for f in self.fields]
      cur.executemany("""
                      insert into fields
                        (name,type,parent_risk)
                      values
                        (%s,(select field_types.id from field_types where name=%s),%s);
                      """,insertable_fields)
      conn.connection.commit()
      return True

  def delete(self):
    if self.name is None:
      return True
    with app.app_context():
      conn = get_db()
      cur = conn.connection.cursor()
      cur.execute("""select name,id from risk_types where name=%s;""",self.name)
      info = cur.fetchone()
      if info is None:
        return True
      else:
        name,id_num = info
      try:
        conn.connection.begin()
        cur.execute("""delete from fields where parent_risk=%s;""",[id_num])
        cur.execute("""delete from risk_types where id=%s;""",[id_num])
        conn.connection.commit()
      except:
        conn.connection.rollback()
        raise


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
  rv = get_db().execute('select name,id from risk_types where name=%s;',(name,))
  row = rv.first()
  if row is None:
    return None
  else:
    name,id_num = row

  rv = get_db().execute("""
                    select
                      fields.name,
                      field_types.name
                    from
                      fields
                      left join field_types on fields.type=field_types.id
                    where
                      fields.parent_risk = %s;""",(id_num,))
  rows = rv.fetchall()
  named_risk = RiskType()
  named_risk.name = name
  named_risk.fields = []
  for (field_name,field_type) in rows:
    named_risk.fields.append((field_name,field_type))
  return named_risk
