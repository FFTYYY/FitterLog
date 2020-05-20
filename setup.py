from setuptools import setup, find_packages
from setuptools.command.install import install
import os

with open("README.md" , encoding = "utf-8") as f:
	readme = f.read()

with open("LICENSE" , encoding = "utf-8") as f:
	license = f.read()

with open("requirements.txt", encoding = "utf-8") as f:
	reqs = f.read()

pkgs = [p for p in find_packages() if p.startswith("fitterlog")]
print(pkgs)

setup(
	name 								= "fitterlog",
	version 							= "0.2.1",
	url 								= "http://github.com/FFTYYY/fitterlog",
	description 						= "",
	license 							= "MIT",
	long_description 					= readme,
	long_description_content_type 		= "text/markdown",
	author 								= "Yang Yongyi",
	author_email 						= "yongyyang17@fudan.edu.cn",
	python_requires 					= ">=3.6",
	packages 							= pkgs,
	install_requires				 	= reqs.strip().split("\n"),
	entry_points			= {"console_scripts": [
		"fitterlog-start-server=fitterlog_server_module.start_server:run" ,
	]},

	include_package_data = True ,
)
