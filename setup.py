from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='netradio',
	version='0.1.0',
	description='A very simple streaming audio player for the Raspberry Pi - early alpha',
	url='http://github.com/harrisclinton/netradio',
	author='Chris Harrington',
	author_email='chris.harrington.jp@gmail.com',
	license='GPLv3+',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: X11 Applications'
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: POSIX :: Linux',
		'Natural Language :: English',
		'Programming Language :: Python :: 2.7',
		'Topic :: Multimedia :: Sound/Audio :: Players'
	],
	keywords='streaming audio Gstreamer PyGame Raspberry Pi',
	include_package_data=True,
	packages=['netradio'],
	install_requires=['pygobject','pygame']
)
