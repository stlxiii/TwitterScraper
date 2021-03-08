import os, time, datetime, pathlib


class _log(object):
    def __init__(self, name='logs', level=1):
        self.file = ''
        self.path = os.path.dirname(os.path.abspath(__file__))
        
        for i in range(level):
            self.path = pathlib.Path(self.path).parent
        self.path = os.path.join(self.path, name)
        os.makedirs(self.path, exist_ok=True)
        self.file = os.path.join(self.path, f'{str(int(time.time()))}.log')
        

    def debug(self, text):
        self.print(text, print_out=False)


    def output(self, text):
        self.print(text, print_out=True)


    def print(self, text, print_out=True,):
        if print_out:
            print(text)

        with open(self.file, 'a', encoding='utf-8') as f:
            if text == '':
                f.write ('')
            else:
                f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(text) + '\n')


    def save_file(self, name, content, compare_size=False):
        '''Save a file inside the log folder.  If compare_size is True, 
           the file will only be overwritten if the new content is larger
           than the one already written to disk.'''
        file = os.path.join(self.path, name)
        size = get_file_len(file) if compare_size else 0

        try:
            if len(content) > size:
                with open(file, 'w', encoding='utf8') as f:
                    f.write(content)
        except Exception as ex:
            self.debug(f'Error saving file {name} : {ex}')


def get_file_len(file):
    if os.path.exists(file) and os.path.isfile(file):
        with open(file, 'r', encoding='utf8') as f:
            return len(f.read())
    else:
        return 0