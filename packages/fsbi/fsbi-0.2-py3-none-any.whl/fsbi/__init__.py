import argparse, glob, os, os.path, re

__all__ = ['compact','expand','rename']

def compact(font):
	d,f,x,s,b,i,t = compact.e(font).groups()
	return f"{d or ''}{f}-{5+compact.x[x]*compact.s[s]}{compact.b[b]}{compact.i[i]}.{t}"

compact.e = re.compile(r'(.*[/\\])?(.+?)(?:(Semi|Extra|Ultra)?(Condensed|Extended))?-'
	r'(Hairline|Thin|ExtraLight|Light|Regular|Medium|SemiBold|Bold|ExtraBold|Black|Heavy)?'
	r'(Italic|Oblique)?\.(otf|ttf|woff2)', re.M).fullmatch
compact.x = {'Semi':1, None:2, 'Extra':3, 'Ultra':4}
compact.s = {'Condensed':-1, None:0, 'Extended':1}
compact.b = {'Hairline':0, 'Thin':1, 'ExtraLight':2, 'Light':3, None:4, 'Regular':4,
	'Medium':5, 'SemiBold':6, 'Bold':7, 'ExtraBold':8, 'Black':9, 'Heavy':9}
compact.i = {None:'', 'Italic':'i', 'Oblique':'o'}

def expand(font):
	d,f,s,b,i,t = expand.e(font).groups()
	s,b = int(s)-5, int(b)
	return f'''{d or ''}{f}{expand.x[abs(s)]}{'Condensed' if s<0 else 'Extended' if s>0
		else ''}-{'' if b==4 and i else expand.b[b]}{expand.i[i]}.{t}'''

expand.e = re.compile(r'^(.*[/\\])?(.+?)-(\d)(\d)([io]?)\.(otf|ttf|woff2)', re.M).fullmatch
expand.x = ['', 'Semi', '', 'Extra', 'Ultra']
expand.b = ['Hairline', 'Thin', 'ExtraLight', 'Light', 'Regular',
	'Medium', 'SemiBold', 'Bold', 'ExtraBold', 'Black']
expand.i = {'':'', 'i':'Italic', 'o':'Oblique'}

def fsbi(files, list=False, restore=False, write=False):
	r,x = [], expand if restore else compact
	for f in sum([glob.glob(f'{f}/*' if os.path.isdir(f) else f) for f in files], []):
		try:
			r.append((f, (n:=x(f)) ))
			if list: print(f'{f} -> {n}')
			if write: os.rename(f,n)
		except:
			pass
	return r

def main():
	a = argparse.ArgumentParser(usage='fsbi [-lrw] [file] ...', add_help=False)
	a.add_argument('file', nargs='*', default=['*'], help='file or dir [*]')
	a.add_argument('-h', action='help', help=argparse.SUPPRESS)
	a.add_argument('-l', action='store_true', help='list [default]')
	a.add_argument('-r', action='store_true', help='restore')
	a.add_argument('-w', action='store_true', help='write')
	a = a.parse_args()
	fsbi(a.file, a.l or not a.w, a.r, a.w)

if __name__ == '__main__':
	main()