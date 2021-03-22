import configparser
import os
import tkinter as tk
from threading import Thread
import signal

class TextApp(Thread):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        self.root = tk.Tk()
        self.root.update()
        self.root.title('TextApp')

        self.sv = tk.StringVar()
        interval = int(self.config['update_interval'])
        self.root.after(0, self.read_file(interval))
        self.create_label()

        self.root.mainloop()

    def read_file(self, wait):
        """Updates text from the file every `wait` interval.

        Args:
            wait: Interval to update (seconds).

        Returns:
            A function that updates `self.sv` with the new contents of the file.
        """
        try:
            with open(self.config['file']) as f:
                content = f.read()
        except IOError:
            content = 'Could not read file.'

        def update_label():
            self.sv.set(content)
            ms_wait = wait * 1000
            self.root.after(ms_wait, self.read_file(wait))
        return update_label

    def create_label(self):
        label = tk.Label(
            self.root,
            textvariable=self.sv,
            fg=self.config['fg'],
            bg=self.config['bg'],
            font=(self.config['font_face'], self.config['font_size']),
        ).pack()

def sigint_handler(sig, frame):
    app.root.quit()
    app.root.update()

if __name__ == '__main__':
    cwd = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    os.chdir(cwd)

    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['textapp']

    app = TextApp(config)
    signal.signal(signal.SIGINT, sigint_handler)

    app.start()
