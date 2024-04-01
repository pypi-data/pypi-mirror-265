from setuptools import setup, find_packages


setup(
    name="geckocheck",
    version="1.0.0",
    license="MIT",
    url="https://github.com/ayuk977/geckocheck",
    author="ayuk977",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author_email="ayuk977@gmail.com",
    packages=find_packages(),
    keywords="geckocheck",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    install_requires=[
        "requests",
        "dmacheck",
    ],
    entry_points={
        "console_scripts": [
            "geckocheck = geckocheck.main:main",
        ],
    },
    project_urls={
        "Source": "https://github.com/ayuk977/geckocheck",
    },
    zip_safe=False,
)
