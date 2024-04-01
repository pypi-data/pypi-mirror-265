from setuptools import setup

description = '''\
`fsbi` renames font files in a compact, well alphabetically ordered way rather than the usual long and disordered notation.

`fsbi -r` restores the original notation.

# Help

	usage: fsbi [-lrw] [file] ...
	
	positional arguments:
	  file  file or dir [*]
	
	options:
	  -l    list [default]
	  -r    restore
	  -w    write

# Compact

	fsbi

	Barlow-Bold.ttf -> Barlow-57.ttf
	Barlow-BoldItalic.ttf -> Barlow-57i.ttf
	BarlowCondensed-ExtraLight.ttf -> Barlow-32.ttf
	BarlowCondensed-ExtraLightItalic.ttf -> Barlow-32i.ttf

# Restore

	fsbi -r

	Barlow-32.ttf -> BarlowCondensed-ExtraLight.ttf
	Barlow-32i.ttf -> BarlowCondensed-ExtraLightItalic.ttf
	Barlow-57.ttf -> Barlow-Bold.ttf
	Barlow-57i.ttf -> Barlow-BoldItalic.ttf

# Python

	import fsbi
	fsbi.compact(font)
	fsbi.expand(font)
	fsbi.rename(files, list=False, restore=False, write=False)

# Values

| | Stretch | Weight
| :-: | :-: | :-:
| 0 | | Hairline
| 1 | UltraCondensed | Thin
| 2 | ExtraCondensed | ExtraLight
| 3 | Condensed | Light
| 4 | SemiCondensed | Regular
| 5 | Normal | Medium
| 6 | SemiExtended | SemiBold
| 7 | Extended | Bold
| 8 | ExtraExtended | ExtraBold
| 9 | UltraExtended | Black'''

setup(
	name = 'fsbi',
	version = '0.2',
	description = 'Font Stretch Bold Italic',
	long_description = description,
	long_description_content_type = 'text/markdown',
	license = 'MIT',
	url = 'http://phyl.io/?page=fsbi.html',
	author = 'Philippe Kappel',
	author_email = 'philippe.kappel@gmail.com',
	keywords = 'font',
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: System Administrators',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: System :: Console Fonts',
		'Topic :: Text Processing :: Fonts',
		'Topic :: Utilities'],
	packages = ['fsbi'],
	entry_points = {'console_scripts': ['fsbi = fsbi:main']}
)