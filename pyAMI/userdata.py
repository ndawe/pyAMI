import os
import shutil


DATA_ROOT = os.getenv('PYAMI_CONFIG_DIR', os.path.expanduser('~/.pyami'))
if not os.path.exists(DATA_ROOT):
    os.mkdir(DATA_ROOT)
elif not os.path.isdir(DATA_ROOT):
    raise RuntimeError("A file at %s already exists."
                       "Unable to create user data" % DATA_ROOT)

# only allow user access
os.chmod(DATA_ROOT, 0700)


def reset(interactive=True):

    if interactive:
        print "This will remove everything under %s" % DATA_ROOT
        option = raw_input("Proceed? (Y/[n]): ")
        if option != 'Y':
            return
    shutil.rmtree(DATA_ROOT)
