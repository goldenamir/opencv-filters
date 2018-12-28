from PIL import Image, ImageTk
import cv2
import time

from filters import clarendon, kelvin, moon, xpro2, make_cartoon, sketch_pencil_using_blending, sketch_pencil_using_edge_detection, invert, no_filter


default_filter_map = {
    'c': (clarendon, 'Clarendon'),
    'k': (kelvin, 'Kelvin'),
    'm': (moon, 'Moon'),
    'x': (xpro2, 'Xpro2'),
    'o': (make_cartoon, 'Cartoon'),
    'b': (sketch_pencil_using_blending, 'Sketch pencil using blending'),
    'e': (sketch_pencil_using_edge_detection, 'Sketch pencil using edge detection'),
    'i': (invert, 'Invert'),
    'n': (no_filter, 'No Filter')
}


class RootHandler:

    def __init__(self, panel):
        self.panel = panel
        self.curr_func = no_filter

    def bind_root(self, root, img_handler, init=True):
        for ch, (fn, name) in default_filter_map.items():
            print(f'Press {ch} - {name}')
            root.bind(f'<{ch}>', lambda e: fn(self.panel, img_handler, self, e, init))

        print(f'\nPress ESC to quit...\n')

    def update_func(self, ch):
        self.curr_func = default_filter_map[ch][0]

    def call_func(self, img_handler):
        self.curr_func(self.panel, img_handler)


class ImageHandler:

    def __init__(self, frame, filtered_frame, out_path):
        self.frame = frame
        self.filtered_frame = filtered_frame
        self.out_path = out_path

    def update_label(self, label, img, orig=False):
        if orig:
            self.frame = img
        else:
            self.filtered_frame = img
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = ImageTk.PhotoImage(img)
        label.configure(image=img)
        label.image = img

    def save_img(self, orig=False):
        ts = time.localtime(time.time())

        if orig:
            filename = f'orig-{time.strftime("%Y-%m-%d_%H-%M-%S", ts)}.jpg'
            p = self.out_path / filename
            cv2.imwrite(str(p), self.frame.copy())
        else:
            filename = f'filter-{time.strftime("%Y-%m-%d_%H-%M-%S", ts)}.jpg'
            p = self.out_path / filename
            cv2.imwrite(str(p), self.filtered_frame.copy())

        print(f'[INFO] saved {filename}')