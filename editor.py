from PyQt5.QtWidgets import *
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
from PIL.ImageQt import Image
from PIL.ImageFilter import BLUR, SHARPEN

app = QApplication([])

window = QWidget()
window.setWindowTitle("Easy Editor")
window.resize(700, 500)

btn_directory = QPushButton("Папка")
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Відзеркалити")
btn_sharpness = QPushButton("Різкість")
btn_black_white = QPushButton("Ч/Б")
btn_blur = QPushButton("Блюр")
btn_contrast = QPushButton("Контраст")

lbl_image = QLabel()
list_files = QListWidget()

col1 = QVBoxLayout()
col2 = QVBoxLayout()
row = QHBoxLayout()
row_btns = QHBoxLayout()

col1.addWidget(btn_directory)
col1.addWidget(list_files)
col2.addWidget(lbl_image, 95)

row_btns.addWidget(btn_left)
row_btns.addWidget(btn_right)
row_btns.addWidget(btn_sharpness)
row_btns.addWidget(btn_flip)
row_btns.addWidget(btn_black_white)
row_btns.addWidget(btn_blur)
row_btns.addWidget(btn_contrast)

col2.addLayout(row_btns)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

window.setLayout(row)

workdir = ""

window.show()

def filter(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def choose_work_directory():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def show_filenames_list():
    extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
    choose_work_directory()
    filenames = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lbl_image.hide()
        pixmapimage = QPixmap(path)
        w = lbl_image.width()
        h = lbl_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lbl_image.setPixmap(pixmapimage)
        lbl_image.show()

    def rotate_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def rotate_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.filter(BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_contrast(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

workimage = ImageProcessor()

def showChoosenImage():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)

list_files.currentRowChanged.connect(showChoosenImage)
btn_directory.clicked.connect(show_filenames_list)
btn_flip.clicked.connect(workimage.do_flip)
btn_black_white.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.rotate_left)
btn_right.clicked.connect(workimage.rotate_right)
btn_sharpness.clicked.connect(workimage.do_sharpen)
btn_blur.clicked.connect(workimage.do_blur)
btn_contrast.clicked.connect(workimage.do_contrast)

app.exec_()