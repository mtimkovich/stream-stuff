import platform
import tkinter as tk
from threading import Thread
import signal

# Change these values as needed.
config = {
    'update_interval': 1,  # secs
    'file': 'test.txt',
    'font_face': 'Arial',
    'font_size': 40,
}

class TextApp(Thread):
    def run(self):
        self.root = tk.Tk()
        self.root.update()
        self.root.title('TextApp')
        self.set_transparency()

        self.sv = tk.StringVar()
        self.root.after(0, self.read_file(config['update_interval']))
        self.create_label()

        self.root.mainloop()

    def read_file(self, wait):
        """Updates text from the file every `wait` interval.

        Args:
            wait: Interval to update (seconds).

        Returns:
            A function that updates `self.sv` with the new contents of the file.
        """
        with open(config['file']) as f:
            content = f.read()

        def update_label():
            self.sv.set(content)
            ms_wait = wait * 1000
            self.root.after(ms_wait, self.read_file(wait))
        return update_label

    def set_transparency(self):
        """Makes the background transparent. Different for different OSes."""
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        if platform.system() == 'Windows':
            self.root.wm_attributes("-disabled", True)
            self.root.wm_attributes("-transparentcolor", "white")
        elif platform.system() == 'Linux':
            self.root.wm_attributes("-alpha", 0)

    def create_label(self):
        label = tk.Label(
            self.root,
            textvariable=self.sv,
            bg='white',
            font=(config['font_face'], config['font_size']),
        ).pack()

def sigint_handler(sig, frame):
    app.root.quit()
    app.root.update()

if __name__ == '__main__':
    app = TextApp()
    signal.signal(signal.SIGINT, sigint_handler)

    app.start()
