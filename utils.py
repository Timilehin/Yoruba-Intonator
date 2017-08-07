import os
import urllib2
from itertools import chain

flatten = lambda lst: list(chain.from_iterable(lst))
setify = lambda row: set(list(row))

def load_or_run(runner, loader, *fpaths):
	if all(os.path.exists(fpath) for fpath in fpaths):
		if len(fpaths) > 1:
			return tuple(loader(fpath) for fpath in fpaths) 
		return loader(fpaths[0])
	else:
		return runner(*fpaths)


def download_file_unicode(path):
	resp = urllib2.urlopen(path)
	encoding = resp.headers.getparam('charset')
	return unicode(resp.read(), encoding)