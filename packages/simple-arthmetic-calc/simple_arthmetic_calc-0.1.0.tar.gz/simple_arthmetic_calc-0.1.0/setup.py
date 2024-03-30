from setuptools import setup, find_packages

# Read the long description from a file
with open('README.md', 'r') as f:
    long_description = f.read()
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='simple_arthmetic_calc',
  version='0.1.0',
  description='Arithmetic Operations on Decimal and Binary numbers.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Manoahar Naidu',
  author_email='beesettim27@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['calculator', 'simple calculator', 'arithmetic operations'], 
  packages=find_packages(),
  install_requires=[''] 
)
