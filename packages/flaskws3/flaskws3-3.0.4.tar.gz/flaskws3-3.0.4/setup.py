#-*- coding: utf-8 -*-

from distutils.core import setup


packages = (
	"flaskws",
)

setup(
	name="flaskws3",
	version="3.0.4",
	packages=packages,
	install_requires=["flask", "tornado"],
	description="WebSockets for Flask.",
	author="RixTheTyrunt",
	author_email="rixthetyrunt@gmail.com",
	url="https://github.com/RixInGithub/flaskws3",
	long_description=open("README.md", "r").read(),
	long_description_content_type="text/markdown"
)