from setuptools import setup

setup(
    name="django-querycount",
    version="0.0.0",
    author="Brad Montgomery, Morgan Phillips",
    author_email="brad@bradmontgomery.net, winter2718@gmail.com",
    description=("Middleware that Prints the number of DB queries to the runserver console."),
    install_requires=[],
    license="MIT",
    keywords="django querycount database performance",
    url="https://github.com/bradmontgomery/django-querycount/tarball/0.0.0",
    packages=[
        "querycount",
    ],
    long_description="this project gives you a middleware that"
    "prints DB query counts in Django's runserver console output.",
    classifiers=[
        "Topic :: Utilities",
    ],
)
