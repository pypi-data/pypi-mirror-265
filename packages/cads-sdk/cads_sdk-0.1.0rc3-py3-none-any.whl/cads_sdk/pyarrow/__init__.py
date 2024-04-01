from .pyarrow_add_on import PyArrow
import pyarrow as pa

# config host and port for hdfs
hdfs = PyArrow().hdfs


"""
Extention function
"""

def ls(path, detail=False):
    if "file:" in path:
        import os
        return os.listdir(path.replace('file:', ''))
    else:
        return pa.HadoopFileSystem().ls(path, detail=detail)


def mkdir(path):
    return pa.HadoopFileSystem().mkdir(path)


def cat(path):
    return pa.HadoopFileSystem().cat(path)


def exists(path):
    if "file:" in path:
        import os
        return os.path.exists(path.replace('file:', ''))
    else:
        return pa.HadoopFileSystem().exists(path)


def info(path):
    return pa.HadoopFileSystem().info(path)


def open(path, mode='rb'):
    return pa.HadoopFileSystem().open(path, mode=mode)
