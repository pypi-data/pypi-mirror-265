from distutils.core import setup
from setuptools import find_packages

# with open("README.md", "r") as f:
#     long_description = f.read()



setup(name='zhaolinchao',  # 包名
      version='0.0.2',  # 版本号
      description='zhaolinchao:this is zlc',
      long_description="这里面有个mail模块：zhaolinchao",
      author='mike_talk',
      author_email='81471644@qq.com',
      url='',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.11',
          'Topic :: Software Development :: Libraries'
      ],
    )
