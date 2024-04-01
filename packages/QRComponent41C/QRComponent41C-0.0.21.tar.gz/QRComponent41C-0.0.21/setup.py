from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='QRComponent41C',
    version='0.0.21',
    author='vissarion249',
    author_email='vissarion249@gmail.com',
    description='QRComponent41C is a Python library for working with QR codes in 1C:Enterprise 8.3.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Absolemus/QRfor1CComponent',
    packages=find_packages(),
    install_requires=['qrcode>=7.4.2', 'Pillow>=10.2.0'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='1C:Enterprise 8.3, QR code, qrcode, Pillow',
    project_urls={
        'GitHub': 'https://github.com/Absolemus/QRfor1CComponent'
    },
    python_requires='>=3.12'
)
