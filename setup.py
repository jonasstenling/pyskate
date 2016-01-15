from distutils.core import setup
setup(
    name='pyskate',
    packages=['pyskate'],
    version='0.1.1',
    description='Netconf abstraction layer for Cisco IOS XE devices',
    author='Jonas Stenling',
    author_email='jonas@stenling.se',
    url='https://github.com/jonasstenling/pyskate',
    download_url='https://github.com/jonasstenling/pyskate/tarball/0.1',
    keywords=['netconf', 'Cisco', 'IOS', 'IOS XE', 'ncclient'],
    install_requires=['ncclient<=0.4.5', 'xmltodict<=0.9.2'],
    classifiers=[]
)
