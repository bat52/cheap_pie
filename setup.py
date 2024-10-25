""" Pypi setup for cheap_pie """
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='cheap_pie',
    version='1.1.0',
    license='Apache 2.0',
    author="Marco Merlin",
    author_email='marcomerli@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description="A python tool for silicon validation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bat52/cheap_pie',
    keywords='python silicon validation',
    install_requires=[
          'untangle',
          'hickle',
          # parsers
          'cmsis-svd',
          'ipyxact',
          'python-docx',
          'wavedrom',
          'wavedrom-ascii',
          'pyverilator-mm',
          'peakrdl-ipxact',
          'peakrdl-uvm',
          'peakrdl-verilog',
          'peakrdl-cheader',
          # 'lxml', # for xlst ipxact conversions
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
