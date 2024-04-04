import os
import sys
import glob

from typing import List, Union
from pathlib import Path

if sys.version_info[0] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

from .string_utils import split_str

FILESYSTEM_TO = {}

def split_url(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    path = parsed_uri.path
    if path.startswith("//"):
        path = path[1:]
    return domain, path

def is_remote_path(path:str):
    return "://" in path

def is_xrootd_path(path:str):
    return "root://" in path

def remote_glob(path:str):
    # can only glob xrootd path
    if not is_xrootd_path(path):
        return path
    import XRootD.client.glob_funcs as glob
    return glob.glob(path)

def get_filesystem(host:str):
    if host in FILESYSTEM_TO:
        return FILESYSTEM_TO[host]
    from XRootD.client import FileSystem
    FILESYSTEM_TO[host] = FileSystem(host)
    return get_filesystem(host)

def remote_isdir(dirname:str, timeout:int=0):
    # can only list xrootd dir
    if not is_xrootd_path(dirname):
        return None
    from XRootD.client import FileSystem
    host, path = split_url(dirname)
    query = get_filesystem(host)
    if not query:
        raise RuntimeError("Cannot prepare xrootd query")
    status, dirlist = query.dirlist(path, timeout=timeout)
    return not status.error
    #return len(remote_glob(os.path.join(dirname, "*"))) > 0

def remote_dirlist(dirname:str):
    # can only list xrootd dir
    if not is_xrootd_path(dirname):
        return []
    return remote_glob(os.path.join(dirname, "*"))

def dirlist(dirname:str):
    return glob.glob(os.path.join(dirname, "*"))

def local_file_exist(path:str):
    if os.path.exists(path):
        return True
    if is_xrootd_path(path):
        host, path = split_url(path)
        return local_file_exist(path)
    return False

def remote_file_exist(path:str, timeout:int=0):
    # can not stat non-xrootd file for now
    if not is_xrootd_path(path):
        return None
    from XRootD.client import FileSystem
    host, path = split_url(path)
    query = get_filesystem(host)
    if not query:
        raise RuntimeError("Cannot prepare xrootd query")
    status, _ = query.stat(path, timeout=timeout)
    return not status.error
    
def resolve_paths(paths:Union[str, List[str]],
                  sep:str=","):
    if isinstance(paths, str):
        paths = split_str(paths, sep=sep, strip=True, remove_empty=True)
        return resolve_paths(paths, sep=sep)
    resolved_paths = []
    for path in paths:
        if "*" in path:
            if is_remote_path(path):
                glob_paths = remote_glob(path)
            else:
                glob_paths = glob.glob(path)
            resolved_paths.extend(glob_paths)
        else:
            resolved_paths.append(path)
    return resolved_paths

