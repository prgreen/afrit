import os
import sys
import hashlib
import urllib2
from optparse import OptionParser
from fnmatch import fnmatch

def list_files(d):
    fileList = []
    for root, subFolders, files in os.walk(d):
        for file in files:
            fileList.append(os.path.join(root, file))
    fileList = [f.replace('\\', '/') for f in fileList]
    for i, _ in enumerate(fileList):
        if fileList[i].startswith('./'):
            fileList[i]=fileList[i][2:]
    if 'afrit' in fileList:
        fileList.remove('afrit')
    if 'afrit_ignore' in fileList:
        fileList.remove('afrit_ignore')
    return fileList

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def file_hash(f):
    m = hashlib.md5()
    m.update(open(f).read())
    return m.hexdigest()

def download_file(f):
    return urllib2.urlopen(URL+f).read()


parser = OptionParser()
parser.add_option('-u', '--url', dest='url', help='URL of remote server')
(options, args) = parser.parse_args()
URL = options.url
#TODO option to remove local files? 

if __name__ == '__main__':
    djinn = r"""
          .-=-.
         /  ! )\
      __ \__/__/
     / _<( ^.^ )
    / /   \ c /O
    \ \_.-./=\.-._     _
     `-._  `~`    `-,./_<
         `\' \'\`'----'
       *   \  . \          *
            `-~~~\   .
       .      `-._`-._   *
             *    `~~~-       *
                        *
                   *         .
    """
    # list everything and write to file afrit
    afrit = open('afrit', 'w+')
    L = list_files('.')
    # TODO ignore files in afrit_ignore
    try:
        ignore_file = open('afrit_ignore')
        ignore_file_lines = ignore_file.read().split('\n')
        ignore_patterns = [line for line in ignore_file_lines if line != '']
        #print ignore_patterns
        for p in ignore_patterns:
            for f in list(L):
                if fnmatch(f, p):
                    L.remove(f)
        ignore_file.close()
    except Exception, err:
        pass
    # http://docs.python.org/2/library/fnmatch.html#fnmatch.fnmatch
    local_afrit = {}
    for f in L:
        t = (f, file_hash(f))
        afrit.write("%s|%s\n" % t)
        local_afrit[t[0]] = t[1]
    afrit.close()

    if URL:
        # retrieve remote afrit
        remote_afrit = download_file('afrit')
        lines = remote_afrit.split('\n')
        remote_files = [tuple(L.split('|')) for L in lines if L != '']
        remote_files_dict = {}
        for k,v in remote_files:
            remote_files_dict[k] = v
        if 'afrit.py' in remote_files_dict:
              if 'afrit.py' in local_afrit and local_afrit['afrit.py'] != remote_files_dict['afrit.py']:
                    w = open('afrit.py', 'w+')
                    w.write(download_file('afrit.py'))
                    w.close()
                    #os.execl(sys.executable, *([sys.executable]+sys.argv))
                    print djinn
                    print 'Patcher was updated, please launch again'
                    sys.exit()
        # retrieve remote files and replace local files with them
        for f,m in remote_files:
            if not (f in local_afrit and local_afrit[f] == m):
                ensure_dir('./' + f)
                w = open(f, 'w+')
                w.write(download_file(f)) #TODO progression bar
                w.close()
                if file_hash(f) != m:
                    print 'DOWNLOAD ' + f + ' OK/hashKO'
                else:
                    print 'DOWNLOAD ' + f + ' OK'
