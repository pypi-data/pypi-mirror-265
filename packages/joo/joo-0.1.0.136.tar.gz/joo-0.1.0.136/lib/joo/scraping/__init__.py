"""
    This file is part of joo library.
    :copyright: Copyright 1993-2024 Wooloo Studio.  All rights reserved.
    :license: MIT, check LICENSE for details.
"""
import os
import time
import json
import chardet
import hashlib
from abc import ABC, abstractclassmethod
from bs4 import BeautifulSoup
import joo.sysutil as sysutil
from joo import ManagedObject
from joo.sysutil import FileSystemDataStore
from joo.logging import LoggerHelper

class Cache(ABC):
    @abstractclassmethod
    def set(self, key, value, text_format=False): pass

    @abstractclassmethod
    def remove(self, key): pass

    @abstractclassmethod
    def get(self, key, valid_period=0, text_format=False): pass

    @abstractclassmethod
    def clear(self, valid_period=0): pass

    @classmethod
    def make_key(cls, resource_id):
        return hashlib.md5(resource_id.encode(encoding="utf-8")).hexdigest()

class FileSystemCache(Cache, FileSystemDataStore):
    def __init__(self, root_folderpath=None):
        FileSystemDataStore.__init__(root_folderpath)

    def _get_filepath(self, key):
        return self.get_path(key, True)

    def set(self, key, value, text_format=False):
        fpath = self._get_filepath(key)
        if value is None:
            sysutil.delete_file(fpath)
        else:
            if text_format:
                sysutil.save_file_contents(fpath, value)
            else:
                sysutil.save_file_bytes(fpath, value)

    def remove(self, key):
        fpath = self._get_filepath(key)
        sysutil.delete_file(fpath)

    def get(self, key, valid_period=0, text_format=False):
        fpath = self._get_filepath(key)
        if not sysutil.file_exists(fpath): return None
        if valid_period > 0:
            if (time.time() - os.path.getctime(fpath)) > valid_period: return None
        if text_format:
            return sysutil.load_file_contents(fpath)
        else:
            return sysutil.load_file_bytes(fpath)

    def clear(self, valid_period=0):
        fpaths = sysutil.list_files(self.root_folderpath)
        t_now = time.time()
        if fpaths is None: return
        if valid_period > 0:
            for fpath in fpaths:
                if (t_now - os.path.getctime(fpath)) > valid_period:
                    sysutil.delete_file(fpath)
        else:
            for fpath in fpaths:
                sysutil.delete_file(fpath)

class Session(ABC, ManagedObject, LoggerHelper):
    def __init__(self):
        ManagedObject.__init__(self)
        LoggerHelper.__init__(self)

        # control
        self._handle = None

    def __del__(self):
        self.close()
        ManagedObject.__del__(self)

    @abstractclassmethod
    def open(self, **kwargs): return None

    @abstractclassmethod
    def close(self): pass

    @abstractclassmethod
    def _get_page(self, url, cache, format, **kwargs): return None

    def get_page(self, url, cache=None, format="soup", **kwargs):
        if format == "html":
            return self._get_page(url, cache, "html", **kwargs)
        elif format == "soup":
            try:
                html = self.get_page(url, cache, "html", **kwargs)
                if html is None: return None
                return BeautifulSoup(html, "html.parser")
            except Exception as ex:
                self.exception(ex)
                return None
        else:
            return self._get_page(url, cache, format, **kwargs)

    @property
    def handle(self):
        return self.open()

    @classmethod
    def wait(cls, secs=1.0):
        time.sleep(secs)

    @classmethod
    def bytes_str(cls, content_bytes, encoding=None):
        try:
            if content_bytes is None: return ""
            if encoding:
                if encoding == "ISO-8859-1": encoding = None
            if encoding is None: encoding = chardet.detect(content_bytes)["encoding"]
            if encoding == "GB2312": encoding = "GBK"
            content_str = str(content_bytes, encoding, errors='replace')
        except:
            content_str = str(content_bytes, errors='replace')
        return content_str
    
    @classmethod
    def json_loads(cls, text):
        try:
            return json.loads(text)
        except:
            return None