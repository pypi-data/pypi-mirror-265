#-*- coding: utf-8 -*-

from distutils.core import setup


packages = (
	"flaskws",
)

setup(
	name="flaskws3",
	version="3.0.0.1",
	packages=packages,
	install_requires=["flask", "tornado"],
	description="WebSockets for Flask.",
	author="RixTheTyrunt",
	author_email="rixthetyrunt@gmail.com",
	url="https://github.com/your-username/your-repo"
)


