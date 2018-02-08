from orm import *
import unittest
from app import app



class testRiskType(unittest.TestCase):

  def test_save(self):
    with app.app_context():
      test_risk = RiskType()
      test_risk.name = "test"
      test_risk.fields.append(("init","date"))
      test_risk.save()
      other_risk = risk_by_name("test")
      self.assertEqual(other_risk.name,test_risk.name)
      self.assertEqual(other_risk.fields[0][0],test_risk.fields[0][0])
      self.assertEqual(other_risk.fields[0][1],test_risk.fields[0][1])
      test_risk.delete()

  def test_delete(self):
    with app.app_context():
      test_risk = RiskType()
      test_risk.name = "test"
      test_risk.fields.append(("init","date"))
      test_risk.save()
      test_risk.delete()
      self.assertEqual(risk_by_name("test"),None)



