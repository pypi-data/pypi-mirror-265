from distutils.core import setup
from setuptools import find_packages

# with open("README.md", "r") as f:
#     long_description = f.read()



setup(name='zhaolinchao',  # 包名
      version='0.0.6',  # 版本号
      description='林超，这个是你的专属区域',
      long_description="项目说明：\r\n这里面有个mail模块：zhaolinchao",
      author='mike_talk',
      author_email='81471644@qq.com',
      license="Apache License, Version 2.0",
      url="http://0510666.xyz",
      python_requires='>=3.6',  # 指定支持的 Python 版本
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            'Programming Language :: Python :: 3.11',
      ],

      include_package_data=True,  # 一般不需要
      packages=find_packages(),
      # install_requires=install_requires,
      entry_points={
            'console_scripts': [
                  'test = test.help:main'
            ]
      }
    )
