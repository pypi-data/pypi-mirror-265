from setuptools import setup
with open("spd_stats/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='spd_stats',
    version='0.1.0',
    description='Statistical Probability Distributions Package',
    packages=['spd_stats'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    author = 'Pradeep Sahani',
    author_email = 'sahanipradeep5529@gmail.com',
    zip_safe=False
)