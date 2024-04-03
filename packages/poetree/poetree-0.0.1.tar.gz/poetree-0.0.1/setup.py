from setuptools import setup
#python3 setup.py sdist
#twine check dist/*
#twine upload dist/*

with open(('README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'poetree',
  long_description_content_type='text/markdown',
  long_description=long_description,
  packages = ['poetree'],   
  version = '0.0.1',      
  license='MIT',        
  description = 'An easy way to get data from PoeTree dataset',   
  author = 'Petr Plechac',                   
  author_email = 'plechac@ucl.cas.cz',      
  url = 'https://github.com/versotym/poetree',
  download_url = 'https://github.com/versotym/poetree/archive/v0.0.1.tar.gz',
  keywords = ['poetry', 'corpus', 'versification'],
  install_requires=[           
          'typing',
          'pandas',
          'tabulate',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',      
    'Topic :: Text Processing :: Linguistic',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.1',      
    'Programming Language :: Python :: 3.2',      
    'Programming Language :: Python :: 3.3',      
    'Programming Language :: Python :: 3.4',      
    'Programming Language :: Python :: 3.5',      
    'Programming Language :: Python :: 3.6',      
    'Programming Language :: Python :: 3.7',      
    'Programming Language :: Python :: 3.8',      
    'Programming Language :: Python :: 3.9',      
    'Programming Language :: Python :: 3.10',      
  ],
)
