import os
import sys
import fire
from pathlib import Path

def descendants(root_dirpath):
    ''' Return descendants file path list of `root_dirpath` ''' 
    fpaths = []
    it = os.walk(root_dirpath)
    for root,dirs,files in it:
        for path in map(lambda name: Path(root, name), files):
            fpaths.append(str(path))
    return fpaths

def move(src, dst, rep='_'):
    ''' 
    Move all files under <SRC> to <DST> recursively
    
    Rename files, and then move files to DST flat structure. 
      src/dir/to/file -> dst/dir_to_file
    
    step1. _ => '' (reps in srcname are removed)
    step2. / => _  (os.sep -> rep)
    
    So you can use rep as separator of some information.
    
    **CAUTION**
    It could be overwrite existing file.
    Be careful to move TOO MANY files in 1 DST directory.
    '''
    srcpaths = descendants(src)
    for srcpath in srcpaths:
        p = Path(srcpath)
        dstname = str(p.relative_to(p.parts[0]))
        dstpath = Path(
            dst, dstname.replace(rep, '').replace(os.sep, rep))
        print(srcpath, '=>', dstpath)
        
    ret = input('All files above will be moved. R U Sure? [y/n]')
    if ret == 'y':
        for srcpath in srcpaths:
            p = Path(srcpath)
            dstname = str(p.relative_to(p.parts[0]))
            dstpath = Path(
                dst, dstname.replace(rep, '').replace(os.sep, rep))
            p.rename(dstpath)
        print(f'Moved {len(srcpaths)} files successfuly.')
    else:
        print('Nothing happend.')

if __name__ == '__main__':
    fire.Fire(move)
