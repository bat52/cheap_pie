""" Pypi setup for cheap_pie """
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='cheap_pie',
    version='0.9.18',
    license='Apache 2.0',
    author="Marco Merlin",
    author_email='marcomerli@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description="A python tool for silicon validation.",
    url='https://github.com/bat52/cheap_pie',
    keywords='python silicon validation',
    install_requires=[
          'untangle',
          'hickle',
          # parsers
          'cmsis-svd',
          'ipyxact',
          'python-docx',
          'pyverilator',
          'peakrdl-ipxact',
          'peakrdl-uvm',
          'peakrdl-verilog',
          # transport layers
          #'pylink-square',
          #'pyocd',
          #'esptool',
          #'packaging' # for verilator version check
      ],
)

project_urls={
    "Source": "https://github.com/bat52/cheap_pie",
    "Tracker": "https://github.com/bat52/cheap_pie/issues"
}
