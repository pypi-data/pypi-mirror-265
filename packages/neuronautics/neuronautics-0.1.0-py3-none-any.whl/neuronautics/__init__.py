import subprocess
___version___="0.1.0.1.0"

import os

branch = (subprocess
          .run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
               stdout=subprocess.PIPE, text=True)
          .stdout.strip())

branch = os.environ.get('BRANCH_NAME')
major, minor, patch, rc, dev = ___version___.split('.')
if branch in ('master', 'main'):
    __version__ = f'{major}.{minor}.{patch}'
elif branch in ('staging', ):
    __version__ = f'{major}.{minor}.{patch}rc{rc}'
else:
    __version__ = f'{major}.{minor}.{patch}dev{dev}'
