import os
from app import app
import unittest
from orm import *

class test_REST(unittest.TestCase):

  def setUp(self):
    self.app = app.test_client()

  def test_fallback(self):
    res = self.app.get("/not_a_real_endpoint_ever")
    self.assertNotEqual(404,res.status_code)
    self.assertNotEqual(500,res.status_code)


  def test_health(self):
    res = self.app.get("/health")
    self.assertEqual("1",str(res.data,encoding='utf-8'))

  def test_risks(self):
    res = self.app.get("/risks")
    self.assertNotEqual(res.data,None)
    self.assertEqual(res.status_code,200)

  def test_one_risk(self):
    res = self.app.get("/risks/not_a_real_type_of_risk_only_for_testing")
    self.assertEqual(res.status_code,404)