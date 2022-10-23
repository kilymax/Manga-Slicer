from email.mime import image
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox

import os
import shutil
import tkinter
from PIL import Image, ImageTk

class Main(tkinter.Tk):
    # ???
    def __init__(self):
        super().__init__()
        self.button1 = tkinter.Button(self, text='Выбрать\nизображение', width=16, height=2, font='Verdana 16', command=self.open_file)
        self.button1.place(x=20, y=20)
        self.label_end = Label(self, text="", bg = '#03362f', fg='white', font='Verdana 12')
        self.label_end.place(x=20, y=110)

    # функция с основным функционалом
    def open_file(self):

        # выбор и открытие изображения
        image_path = fd.askopenfilename()
        #print(image_path)
        self.image = Image.open(image_path)
        self.label_end.config(text='')
        self.counter = 0
        self.res_dir_count = 1

        # Создание новой result папки
        while self.res_dir_count < 100:
            if os.path.exists(os.path.join(os.path.split(image_path)[0], f'result{self.res_dir_count}')):
                #shutil.rmtree(os.path.join(os.path.split(image_path)[0], f'result{self.res_dir_count}'))
                self.res_dir_count += 1
            else:
                self.result_path = os.path.join(os.path.split(image_path)[0], f'result{self.res_dir_count}')
                os.mkdir(f'{self.result_path}')
                break
            

        # создание бегунка для регулировки масштаба
        self.scale_label = Label(text="Масштаб изображения:", bg = '#03362f', fg='white', font='Verdana 12')
        self.scale_label.place(x=30, y=125)
        self.scale = Scale(orient=HORIZONTAL, from_=0.1, to=2, length=215, resolution=0.1, highlightthickness=0, bg='#03362f', fg='white', font='Verdana 12', variable=canvas_scale, command=self.visualization)
        self.scale.set(1)
        self.scale.place(x=20, y=145)

        # кнопка обрезания
        self.button2 = tkinter.Button(self, text='Обрезать', width=16, height=2, font='Verdana 16', command=self.image_slice)
        self.button2.place(x=20, y=220)

        # метка для проверки выбраной области
        self.label_check = Label(self, text="", bg = '#03362f', font='Verdana 12')
        self.label_check.place(x=30, y=295)

        # кнопка сохранения и выхода из программы
        self.button3 = tkinter.Button(self, text='Завершить\nнарезку', width=16, height=2, font='Verdana 16', command=self.end_slicing)
        self.button3.place(x=20, y=350)

        self.visualization(canvas_scale.get())
        self.first_time = True

    def visualization(self, cs):
        # удаление предыдущих виджетов
        if self.first_time:
            self.slice_scale.destroy()
            self.canvas.destroy()

        # создание миниатюры для визуализации 
        self.true_size = self.image.size
        half_size = (round(self.true_size[0]/2 * float(cs)), round(self.true_size[1]/2 * float(cs)))
        image_miniature = self.image.resize((half_size[0], half_size[1]))

        # создание полотна с изображением
        self.canvas = tkinter.Canvas(height=half_size[1], width=half_size[0])
        self.canvas.place(x=290, y=19)
        self.photo = ImageTk.PhotoImage(image_miniature)
        self.canvas.create_image(round(half_size[0]/2)+2, round(half_size[1]/2)+2, image=self.photo)
        self.slice_line = self.canvas.create_line(0, 0, 0, 0)

        # создание бегунка для калибровки линии среза
        self.slice_scale = Scale(orient=VERTICAL, from_=0, to=half_size[1], showvalue=0, length=half_size[1]+32, highlightthickness=0, bg='#03362f', fg='white', font='Verdana 12', variable=slice_px, command=self.slice_aim)
        self.slice_scale.place(x=260, y=0)

    # функция визуализации линии среза
    def slice_aim(self, slice_px):
        self.label_check.config(text='', fg='red')
        self.canvas.delete(self.slice_line)
        self.slice_line = self.canvas.create_line(0, int(slice_px), 720, int(slice_px), width=1, fill='red')
    
    # функция обрезания и сохранения
    def image_slice(self):
        if slice_px.get()>0:
            #print('Обрезается: ', self.image.size, int(slice_px.get())*2, float(canvas_scale.get()))
            left = 0
            right = self.image.size[0]
            upper = 0
            lower = round(int(slice_px.get())*2 / canvas_scale.get())-4
            piece = self.image.crop((left, upper, right, lower))
            piece.save(self.result_path + f'/{self.counter+1}.png')
            self.image = self.image.crop((left, lower, right, self.image.size[1]))
            self.counter += 1
            self.visualization(canvas_scale.get())
            self.slice_aim(slice_px.get())
        else:
            self.label_check.config(text='Выберите место среза!', fg='red')
    
    def end_slicing(self):
        self.image.save(self.result_path + f'/{self.counter+1}.png')
        self.slice_scale.destroy()
        self.canvas.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.scale_label.destroy()
        self.scale.destroy()
        self.label_check.destroy()
        self.label_end.config(text='Изображения сохранены!', fg='white')
        answer = messagebox.askyesno(title="Успешно!", 
                            message=f"Результат сохранен в папке result в указанной директории.\n\nВсего нарезано изображений: {self.counter+1}\n\nОткрыть папку с результатами?")
        if answer:
            os.startfile(self.result_path)

file_dir = os.path.split(__file__)[0] + '\\'
if __name__ == "__main__":
    main = Main()
    main.geometry('720x720')
    main.title('MangaSlicer')
    main['bg'] = '#03362f'
    slice_px = IntVar()
    canvas_scale = DoubleVar()
    main.first_time = False


    main.mainloop()

# pyinstaller -F -w -i 'ico.png' originals\orig_slicer.py