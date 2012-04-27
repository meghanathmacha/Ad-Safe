from setuptools import find_packages 
from distutils.core import setup
version = ''
#README = os.path.join(os.path.dirname(__file__), 'README.txt')
#long_description = open(README).read() + 'nn'
setup(name='Chisafe',
      py_modules = ['contentanalyzer','directory','google_safe_browser','util','link_processor','expression','chisafe'],
      version=version,
      packages = find_packages(),
      include_package_data = True,
      package_data = {
        '': ['*.txt', '*.html'],
      },
      description=("A package that deals with Adsafe"),
      keywords='Algorithm',
      author='MM',
      url='http://www.chitika.com',
      license='GPL',
      scripts = ['contentanalyzer.py'],
      test_suite = "unittest_agg",
      install_requires = ['numpy','nltk','pycurl','redis','BeautifulSoup'],
      entry_points = {
          'setuptools.installation': [
            'eggsecutable = contentanalyzer.ContentAnalyzer:Classify_1',
        ]
    }

      )
