import setuptools

setuptools.setup(
  name="hySpider",
  version="0.0.1",
  author="zhyclouds",
  author_email="310123665@qq.com",
  description="a spider demo",
  url="https://github.com/zhyclouds",
  packages=setuptools.find_packages(),
  install_requires=['requests', 'lxml'],
  python_requires='>=3.6',
  license="Apache 2.0",
  classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3 :: Only",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
)