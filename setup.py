from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cheap_pie',
    version='0.1.17',
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
          'cmsis-svd',
          'ipyxact',
          'pylink-square',
          'pyocd',
          'esptool',
          'python-docx',
          'pyverilator',
          'peakrdl-ipxact',
          'peakrdl-uvm',
          'peakrdl-verilog',
          'hickle',
          'packaging'
      ],
)