from typing import List
from XRootD.client import CopyProcess

#https://xrootd.slac.stanford.edu/doc/python/xrootd-python-0.1.0/modules/client/copyprocess.html
def copy_files(src:List[str], dst:List[str], force:bool=False, **kwargs):
    copy_process = CopyProcess()
    for src_i, dst_i in zip(src, dst):
        copy_process.add_job(src_i, dst_i, force=force, **kwargs)
    copy_process.prepare()
    copy_process.run()