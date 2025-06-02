from distutils.core import setup

install_requires = [
    "beautifulsoup4[lxml]~=4.12",
    "openpyxl",
    "httpx[http2]",
    "dateutils",
    "anticaptchaofficial",
    "capsolver",
    "2captcha-python",
    "python-magic",
    "python-magic-bin; platform_system == 'Windows'"
]

setup(
    name='tweety-ns',
    packages=['tweety', 'tweety.types', 'tweety.events', 'tweety.captcha'],
    version='2.3.3',
    license='MIT',
    description='An easy Twitter Scraper',
    author='Tayyab Kharl',
    author_email='tayyabmahr@gmail.com',
    url='https://github.com/mahrtayyab/tweety',
    keywords=['TWITTER', 'TWITTER SCRAPE', 'SCRAPE TWEETS'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3'
    ],
)
