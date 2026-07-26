import os as _os
def flat_listdir(main_path):
    return _os.popen(fr'dir {main_path} /s /b').read().split('\n')
def sort_types(files):
    from collections import defaultdict
    from os import path
    result = defaultdict(list)
    for f in files:
        _, e = path.splitext(f)
        if e:
            result[e].append(f)
    return dict(result)
def make_if_not_exists(file_or_folder, type='file'):
    if not _os.path.exists(file_or_folder):
        if type.lower() == 'file':
            _os.mkdir(_os.path.dirname(file_or_folder))
            with open(file_or_folder, 'w') as f:
                pass
        else:
            _os.mkdir(file_or_folder)
