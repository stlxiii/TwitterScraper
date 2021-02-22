import os, pathlib
from configparser import ConfigParser


class _config(object):
    def __init__(self, file='config.ini', parentdir=True):
        self.cp:ConfigParser = ConfigParser()
        self.file_path       = os.path.join(pathlib.Path(__file__).parent.absolute())
        if parentdir:          self.file_path  = pathlib.Path(self.file_path).parent
        self.file_path       = os.path.join(self.file_path, file)

        self.cp.read(self.file_path)
        self.save()


    def add_section(self, section):
        if not self.cp.has_section(section):
            self.cp.add_section(section)


    def get_key(self, section, key):
        try:
            return self.cp.get(section, key)
        
        except: 
            return None


    def save_key(self, section, key, value):
        self.add_section(section)
        self.cp.set(section, key, value)
        self.save()


    def save(self):
        with open(self.file_path, 'w', encoding="utf-8") as f:
            self.cp.write(f)