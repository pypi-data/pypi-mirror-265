from typing import Optional, Union, List, Dict
import os
import re
import glob

import numpy as np

from quickstats import semistaticmethod
from quickstats.utils.path_utils import (resolve_paths, is_remote_path, remote_glob,
                                         remote_isdir, remote_dirlist, dirlist,
                                         local_file_exist, split_url)
from quickstats.utils.root_utils import is_corrupt
from quickstats.utils.common_utils import in_notebook
from quickstats.interface.xrootd import get_cachedir
from .TObject import TObject

class TFile(TObject):

    FILE_PATTERN = re.compile(r"^.+\.root(?:\.\d+)?$")

    def __init__(self, source:Union[str, "ROOT.TFile"],
                 **kwargs):
        super().__init__(source=source, **kwargs)

    def initialize(self, source:Union[str, "ROOT.TFile"]):
        self.obj = self._open(source)
        
    @staticmethod
    def is_corrupt(f:Union["ROOT.TFile", str]):
        return is_corrupt(f)

    @semistaticmethod
    def _is_valid_filename(self, filename:str):
        return self.FILE_PATTERN.match(filename) is not None
    
    @semistaticmethod
    def _requires_protocol(self, filename:str):
        return "://" in filename

    @semistaticmethod
    def _filter_valid_filenames(self, filenames:List[str]):
        filenames = [filename for filename in filenames if self._is_valid_filename(filename)]
        return filenames

    @semistaticmethod
    def _get_cache_path(self, path:str, cachedir:str="/tmp"):
        host, filename = split_url(path)
        filename = filename.lstrip('/.~')
        cache_path = os.path.join(cachedir, filename)
        return cache_path
    
    @semistaticmethod
    def _resolve_cached_remote_paths(self, paths:List[str],
                                     strict_format:Optional[bool]=True,
                                     cached_only:bool=False):
        import ROOT
        cachedir = get_cachedir()
        if cachedir is None:
            return list(paths)
        resolved_paths = []
        for path in paths:
            url = ROOT.TUrl(path)
            # skip local file
            if url.GetProtocol() == "file":
                resolved_paths.append(path)
                continue
            filename = url.GetFile().lstrip("/")
            cache_path = os.path.join(cachedir, filename)
            if os.path.exists(cache_path):
                if os.path.isdir(cache_path):
                    cache_paths = dirlist(cache_path)
                    if strict_format:
                        cache_paths = self._filter_valid_filenames(cache_paths)
                    if not cache_paths:
                        if not cached_only:
                            resolved_paths.append(path)
                        continue
                    resolved_paths.extend(cache_paths)
                else:
                    resolved_paths.append(cache_path)
            elif not cached_only:
                resolved_paths.append(path)
        return resolved_paths
                
    @semistaticmethod
    def list_files(self, paths:Union[List[str], str],
                   strict_format:Optional[bool]=True,
                   resolve_cache:bool=False,
                   expand_remote_files:bool=True,
                   raise_on_error:bool=True):
        remote_flag = True
        paths = resolve_paths(paths)
        filenames = []
        
        # expand directories if necessary
        for path in paths:
            if is_remote_path(path):
                if local_file_exist(path):
                    host, path = split_url(path)
                else:
                    if remote_flag:
                        self.stdout.info("Resolving remote files. Network traffic overhead might be expected.")
                        remote_flag = False
                    if expand_remote_files and remote_isdir(path):
                        filenames.extend(remote_dirlist(path))
                    else:
                        filenames.append(path)
                    continue
            if os.path.isdir(path):
                filenames.extend(dirlist(path))
            else:
                filenames.append(path)
        if strict_format:
            filenames = self._filter_valid_filenames(filenames)
        if not filenames:
            return []
        if resolve_cache:
            filenames = self._resolve_cached_remote_paths(filenames)
        import ROOT
        invalid_filenames = []
        valid_filenames = []
        for filename in filenames:
            if is_remote_path(filename):
                # delay the check of remote root file to when they are open
                valid_filenames.append(filename)
                continue
            try:
                rfile = ROOT.TFile(filename)
                if self.is_corrupt(rfile):
                    invalid_filenames.append(filename)
                else:
                    valid_filenames.append(filename)
            except:
                invalid_filenames.append(filename)
        if invalid_filenames:
            fmt_str = "\n".join(invalid_filenames)
            if raise_on_error:
                raise RuntimeError(f'Found empty/currupted file(s):\n{fmt_str}')
            else:
                self.stdout.warning(f'Found empty/currupted file(s):\n{fmt_str}')
        if not remote_flag:
            self.stdout.info("Finished resolving remote files.")
        return valid_filenames
    
    @staticmethod
    def _open(source:Union[str, "ROOT.TFile"]):
        # source is path to a root file
        if isinstance(source, str):
            import ROOT
            source = ROOT.TFile(source)
            
        if TFile.is_corrupt(source):
            raise RuntimeError(f'empty or currupted root file: "{source.GetName()}"')
            
        return source
        
    """
    def make_branches(self, branch_data):
        branches = {}
        return branches
    
    def fill_branches(self, treename:str, branch_data):
        if self.obj is None:
            raise RuntimeError("no active ROOT file instance defined")
        tree = self.obj.Get(treename)
        if not tree:
            raise RuntimeError(f"the ROOT file does not contain the tree named \"{treename}\"")
        n_entries = tree.GetEntriesFast()
        
        for i in range(n_entries):
            for branch in branches:
                
        tree.SetDirectory(self.obj)
        # save only the new version of the tree
        tree.GetCurrentFile().Write("", ROOT.TObject.kOverwrite)
    """
    
    def get_tree(self, name:str, strict:bool=True):
        tree = self.obj.Get(name)
        if not tree:
            if strict:
                raise RuntimeError(f'In TFile.Get: Tree "{name}" does not exist')
            return None
        return tree

    @semistaticmethod
    def fetch_remote_files(self, paths:Union[str, List[str]],
                          cache:bool=True,
                          cachedir:str="/tmp",
                          **kwargs):
        if isinstance(paths, str):
            paths = [paths]
        remote_paths = []
        for path in paths:
            if not is_remote_path(path):
                self.stdout.warning(f"Not a remote file: {path}. Skipped.")
                continue
            if local_file_exist(path):
                self.stdout.warning(f"Remote file {path} can be accessed locally. Skipped.")
                continue
            remote_paths.append(path)
        filenames = self.list_files(remote_paths, resolve_cache=cache,
                                    expand_remote_files=True)
        cached_files = [filename for filename in filenames if not is_remote_path(filename)]
        files_to_fetch = [filename for filename in filenames if is_remote_path(filename)]
        if cached_files:
            self.stdout.info(f'Cached remote file(s):\n' + '\n'.join(cached_files))
        from quickstats.interface.xrootd.utils import copy_files
        src, dst = [], []
        for file in files_to_fetch:
            src.append(file)
            dst.append(self._get_cache_path(file))
        if src:
            self.stdout.info(f'Fetching remote file(s):\n' + '\n'.join(src))
            self.stdout.info(f'Destination(s):\n' + '\n'.join(dst))
        copy_files(src, dst, force=not cache, **kwargs)

    def close(self):
        self.obj.Close()
        self.obj = None