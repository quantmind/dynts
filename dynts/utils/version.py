import datetime
import os
import subprocess

symbol = {'alpha': 'a', 'beta': 'b'}


def get_version(version, filename=None):
    assert len(version) == 5
    assert version[3] in ('alpha', 'beta', 'rc', 'final')
    main = '.'.join(map(str, version[:3]))
    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        git_changeset = get_git_changeset(filename)
        if git_changeset:
            sub = '.dev%s' % git_changeset
    if version[3] != 'final' and not sub:
        sub = '%s%s' % (symbol.get(version[3], version[3]), version[4])
    return main + sub


def sh(command, cwd=None):
    return subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            cwd=cwd,
                            universal_newlines=True).communicate()[0]


def get_git_changeset(filename=None):
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    dirname = os.path.dirname(filename or __file__)
    git_show = sh('git show --pretty=format:%ct --quiet HEAD',
                  cwd=dirname)
    timestamp = git_show.partition('\n')[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')
