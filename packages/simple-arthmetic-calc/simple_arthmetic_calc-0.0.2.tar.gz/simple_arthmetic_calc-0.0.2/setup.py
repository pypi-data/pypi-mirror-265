from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='simple_arthmetic_calc',
  version='0.0.2',
  description='Arithmetic calculator with basic functions like addition, subtraction, multiplication, division, factorial, power, square root, modulus, LCM, GCD, prime number, even number, odd number.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Manoahar Naidu',
  author_email='beesettim27@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['calculator', 'simple calculator', 'arithmetic calculator', 'basic calculator', 'simple arithmetic calculator', 'simple arithmetic calculator with basic functions', 'simple arithmetic calculator with basic functions like addition, subtraction, multiplication, division, factorial, power, square root, modulus, LCM, GCD, prime number, even number, odd number.'], 
  packages=find_packages(),
  install_requires=[''] 
)
