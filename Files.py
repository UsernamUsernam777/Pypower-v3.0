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
