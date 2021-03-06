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

        with open(self.file, 'a') as f:
            if text == '':
                f.write ('')
            else:
                f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(text) + '\n')
