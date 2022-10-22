from distutils.core import setup

setup(
    name='tweety-ns',
    packages=['tweety', 'tweety.types'],
    version='0.5.1',
    license='MIT',
    description='An easy Twitter Scraper',
    author='Tayyab Kharl',
    author_email='tayyabmahr@gmail.com',
    url='https://github.com/mahrtayyab/tweety',
    keywords=['TWITTER', 'TWITTER SCRAPE', 'SCRAPE TWEETS'],
    install_requires=[
        'beautifulsoup4',
        'openpyxl',
        'requests',
        'dateutils'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
