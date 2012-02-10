import os


DATA_ROOT = os.path.expanduser('~/.atlasmeta')
if not os.path.exists(DATA_ROOT):
    os.mkdir(DATA_ROOT)
elif not os.path.isdir(DATA_ROOT):
    raise RuntimeError("A file at ~/.atlasmeta already exists."
                       "Unable to create user data")
