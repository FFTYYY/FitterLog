import os
import sys
import argparse

def migrate():
	os.chdir(os.path.dirname(__file__))
	sys.path.append(os.path.abspath("."))

	if os.system("python manage.py migrate") > 0:
		os.system("python3 manage.py migrate")

def run():
	os.chdir(os.path.dirname(__file__))
	sys.path.append(os.path.abspath("."))

	C = argparse.ArgumentParser()
	C.add_argument("--port" , type = int , default = 8000)
	C = C.parse_args()

	if os.system("python manage.py migrate") > 0:
		os.system("python3 manage.py migrate")

	if os.system("python manage.py runserver 0.0.0.0:%d" % (C.port)) > 0:
		os.system("python3 manage.py runserver 0.0.0.0:%d" % (C.port))