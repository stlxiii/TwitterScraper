import os, datetime, shutil
from pprint import pprint
from tinydb import Query, where, TinyDB


class _tiny_db(object):
    def __init__(self, file, clear=False):
        self.folder = os.path.dirname(file)
        self.file   = file

        #prepare path to database
        if not self.file.endswith('.json'): self.file += '.json'
        os.makedirs(self.folder, exist_ok=True)

        #delete the existing file if requested
        if clear:
            if os.path.exists(self.file):
                os.remove(self.file)

        #load database
        print('Loading database {}...'.format(self.file))
        self.db = TinyDB(self.file)

        #point different db functions from the class to the db object
        #so I don't have to do something silli like db.db.all()
        self.insert          = self.db.insert
        self.insert_multiple = self.db.insert_multiple
        self.update          = self.db.update
        self.purge           = self.db.purge
        self.remove          = self.db.remove
        self.search          = self.db.search
        self.all             = self.db.all
        

    def count(self):
        '''returns the number of rows in the database'''
        return len(self.db)


    def backup(self, backup_name='db_backup.json'):
        filename = self.folder + "/{}".format(backup_name.lower())
        if not filename.endswith('.json'): filename += '.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        print('Saving database backup ...')
        shutil.copy(self.file, filename)


    def get_all_ids(self):
        ids = []
        for i in self.all():
            ids.append(i['id'])
        return ids


    def merge(self, target, what=''):
        '''Loads the content of the target database into self, 
           except for rows with the same id value'''
        if what != '': what += ' '
        if target is None:
            print('Can''t merge this')
        else:
            if target.count() > 0:   
                print('Merging {} into {}.'.format(target.file, self.file))

                #load an index of the current ids
                db1_ids = self.get_all_ids()
                new = []

                #loop through the new database and only keep the new stuff
                target_n = target.count()
                done = 0
                start = datetime.datetime.now()
                print('{} / {} read'.format(done, target_n))
                for i in target.all():
                    print('{} / {} read'.format(done, target_n))
                    try:
                        if not i['id'] in db1_ids:
                            new.append(i)
                            db1_ids.append(i['id'])
                        done += 1
                    finally:
                        if (datetime.datetime.now() - start).seconds > 1:
                            start = datetime.datetime.now()
                            print('{} / {} checked'.format(done, target_n))

                print('Saving {} new {}'.format(len(new), what))
                #save the new stuff
                if len(new) > 0:
                    self.insert_multiple(new)
                print('Saved {} new {}into {}'.format(len(new), what, self.file))
        

    def wipe(self):
        self.db = None
        try:
            os.remove(self.file)
        except:
            pass