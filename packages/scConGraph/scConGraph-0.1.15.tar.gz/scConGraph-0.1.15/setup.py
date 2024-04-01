from setuptools import setup, find_packages
import setuptools

setup(
    name='scConGraph',
    version='0.1.15',
    description="A scalable cross-time Context Graph model for reconstructing tumor cell dynamic responses from single-cell perturbation transcriptomics.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown", 
    include_package_data=True,
    author='Xinqi Li',
    author_email='lxq19@mails.tsinghua.edu.cn',
    license='MIT License',
    url='https://github.com/Li-Xinqi/scConGraph.git',
    packages=find_packages(include=['scConGraph', 'scConGraph.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7',
    install_requires=['network','matplotlib','numpy','pandas','seaborn','scipy','scanpy', 'community'],
)