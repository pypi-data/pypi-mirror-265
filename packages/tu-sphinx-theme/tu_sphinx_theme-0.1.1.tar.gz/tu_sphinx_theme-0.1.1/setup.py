from setuptools import setup
from tu_sphinx_theme import __version__

# Taken from pytorch_sphinx_theme
setup(
    name="tu_sphinx_theme",
    version=__version__,
    author="TorchUncertainty Contributors",
    author_email="olivier.laurent@ensta-paris.fr",
    url="https://github.com/torch-uncertainty/tu_sphinx_theme",
    docs_url="https://github.com/torch-uncertainty/tu_sphinx_theme",
    description="TorchUncertainty Sphinx Theme",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=["tu_sphinx_theme"],
    packages=["tu_sphinx_theme"],
    include_package_data=True,
    zip_safe=False,
    package_data={
        "tu_sphinx_theme": [
            "theme.conf",
            "*.html",
            "static/css/*.css",
            "static/js/*.js",
            "static/js/*/*.js",
            "static/fonts/*/*.*",
            "static/images/*.*",
            "theme_variables.jinja",
        ]
    },
    entry_points={
        "sphinx.html_themes": [
            "tu_sphinx_theme = tu_sphinx_theme",
        ]
    },
    license="MIT License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Documentation",
    ],
    install_requires=["sphinx"],
)
