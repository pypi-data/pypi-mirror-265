from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

'''
# 学习了这篇文章：https://zhuanlan.zhihu.com/p/276461821
# 总结一下就是先写个 setup.py 文件，然后按照下面步骤操作：
# python3 setup.py register
# python3 setup.py sdist upload
'''
# 更新了打包步骤：https://blog.csdn.net/xcntime/article/details/115189401
# python3 setup.py sdist
# twine check dist/*
# twine upload dist/*
setup(
    name='resounds',
    version='0.0.1',
    author='may.xiaoya.zhang',
    author_email='may.xiaoya.zhang@gmail.com',
    url='https://pypi.org/user/May.xiaoya.zhang/',
    description='工程化自修改prompt',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
