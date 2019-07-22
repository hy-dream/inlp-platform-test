
import configparser

cp=configparser.RawConfigParser()
cp.read("nlp.conf")

print(cp.get("db","baseURL"))
