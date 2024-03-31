from setuptools import find_packages, setup

setup(
    name='czo',
    version='0.1.5',
    description='构建测试数据的工具包',
    long_description='伪造信息和随机数据',
    author='sfwwslm',
    author_email='sfwwslm@gmail.com',
    url='https://github.com/sfwwslm/czo.git',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=['setuptools>=69.2.0', 'wheel'],
    keywords='test faker rand',
    python_requires=">=3.10"
)
