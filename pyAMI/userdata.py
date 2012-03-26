import os


DATA_ROOT = os.path.expanduser('~/.pyami')
if not os.path.exists(DATA_ROOT):
    os.mkdir(DATA_ROOT)
elif not os.path.isdir(DATA_ROOT):
    raise RuntimeError("A file at ~/.pyami already exists."
                       "Unable to create user data")

# only allow user access
os.chmod(DATA_ROOT, 0700)
