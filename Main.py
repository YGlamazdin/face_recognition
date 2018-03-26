from tkinter import *
import baza.db_fases as db
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import cv2
import PersonWindows
import CameraWindow
import WorkWindow as ww
import SortWindow
import FaceAlgo

# https://konkurs.sochisirius.ru/#directions

person=0
selected_persone =False
max_in_page  = 35
page_win_person_main=0
present = True

filter = ""
list_persons=[]
# def set_page(i):
#     text_file = open("p.txt", "w")
#     text_file.write("%s" % i)
#     print("save", i)
#     text_file.close()
#
# def read_page():
#     with open('p.txt', 'r') as myfile:
#         data = myfile.read().replace('\n', '')
#         print("read file", data)
#         return (int(data))


def callback_search(sv):
    global filter
    print(sv.get())
    filter = sv.get()
    refresh_main_window()
    #отображаем в списке только те персоны, которрые есть ф фильтре

    return True

def delbuff():
    FaceAlgo.del_buff()

def delEmptyFaces():
    print("удаляем пустые персоны")
    FaceAlgo.delEmptyFaces()
    refresh_main_window()

def del_selected(self):
    cs=listbox.curselection()
    print(cs)
    if cs:
        listbox.delete(cs[0])
    refresh_main_window()

def OnSelect(event):
    global person, selected_persone, page_win_person_main, present
    #page_win_person_main = 0
    print("select person")

    #print("click")
    # selections = listbox.curselection()  # tuple of digit-string(s), aTupleOfSTRINGs, where digit-string(s) range from { 0, 1, .., N-1 }
    # selections = [int(x) + 1 for x in selections]  # transform string(s) to shifted int(s), make 'em { 1, 2, .., N }
    if listbox.curselection():
        #set_page(0)
        present = False
        page_win_person_main=0
        print(listbox.curselection()[0])
        print(present)

        person = list_persons[listbox.curselection()[0]]
        #person=all_person[listbox.curselection()[0] ]
        # PersonWindows.WindowsPerson(person)
        selected_persone=True
        refesh_persone()


def OnSelect2(event):
    global person, selected_persone, page_win_person_main
    page_win_person_main = 0
    print("click")
    # selections = listbox.curselection()  # tuple of digit-string(s), aTupleOfSTRINGs, where digit-string(s) range from { 0, 1, .., N-1 }
    # selections = [int(x) + 1 for x in selections]  # transform string(s) to shifted int(s), make 'em { 1, 2, .., N }
    if listbox.curselection():
        print(listbox.curselection()[0])

        person = list_persons[listbox.curselection()[0]]
        #person=all_person[listbox.curselection()[0] ]
        PersonWindows.WindowsPerson(person)
        selected_persone=True
        refesh_persone()

def del_person():
    db.del_persone(all_person[listbox.curselection()[0] ])
    refresh_main_window()

def OpenCameraWindow():
    CameraWindow.WindowsCamera(cv2.VideoCapture(0), False)

def OpenCameraWindowFile():
    fileName = askopenfilename(filetypes = (("All files", "*.*")
                                                     , ("move", "*.mov;*.mpg;*.avi;*.mp4")))
    if len(fileName)>0:
        CameraWindow.WindowsCamera(cv2.VideoCapture(fileName), False)
    else:
        print("Файл не выбран")

# def WorkWindows():
#     print("Запускаем служебное окно")
#     WorkWindow.WindowsWork()

def SortWindows():
    print("Запускаем сортировку персон")
    SortWindow.WindowsSort()


def create_person():
    print("создаем новую персону в базе данных")
    db.add_person()
    refresh_main_window()
    return

def savePerson():
    global e_name, e_second_name, persone
#    print ("save", e_name.get(), e_second_name.get())
    person.name = e_name.get()
    #person.second_name = e_second_name.get()

    person.save()
    #persone.get(name=e_name.get(), second_name=e_second_name.get(), birthday=date(2007, 1, 10), is_relative=True)

    return


def refesh_persone():
    global all_person, person, selected_persone, max_in_page, listbox_faces, frame5,frame6, page_win_person_main, panel, present
    #page_win_person_main = read_page()
    if present == False:
        panel.destroy()
    if selected_persone:
        e_name.grid(row=0, column=1, padx=20)
        l_name.grid(row=0, column=0, padx=20)
        but_save.grid(row=0, column=2, padx=20)

        print("page_win_person", page_win_person_main)
        e_name.delete(0, END)
        e_name.insert(END, person.name)


        but_step1 = Button(frame5, text='<<', command=lambda i=-1: page_change(i)).grid(row=5, column=0,
                                                                                        sticky=(N, W, E, S))
        but_step2 = Button(frame5, text='>>', command=lambda i=1: page_change(i)).grid(row=6, column=0, sticky=(N, W, E, S))
        but_cut = Button(frame5, text='Вырезать', command=onCut).grid(row=2, column=0, sticky=(N, W, E, S))
        but_paste = Button(frame5, text='Вставить', command=onPaste).grid(row=1, column=0,
                                                                                          sticky=(N, W, E, S))

        row_c = 0
        col_c = 0
        c = 0
        listbox_faces.delete(0, END)

        list = frame6.grid_slaves()
        for l in list:
            l.destroy()

        count_faces = 0
        for face in person.face:
            # print(page_win_person*max_in_page, page_win_person*max_in_page+max_in_page)

            if count_faces >= page_win_person_main * max_in_page and count_faces < page_win_person_main * max_in_page + max_in_page:
                try:
                    listbox_faces.insert(END, face)
                    frame = cv2.imread(face.image_path)
                    height, width = frame.shape[:-1]
                    if height > 0 and width > 0:
                        frame = cv2.resize(frame, (115, 115), interpolation=cv2.INTER_CUBIC)
                        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                        img = Image.fromarray(cv2image)
                        # imgtk = ImageTk.PhotoImage(image=img)

                        # img = ImageTk.PhotoImage(Image.open(face.image_path))
                        img = ImageTk.PhotoImage(image=img)

                        #print(face.image_path, c)
                        # panel = Label(t, image=img)

                        # panel = Label(t, text = face.image_path)

                        panel = Button(frame6, image=img, command=lambda i=c: onClick(i))
                        # panel = Button(t, image=img, text=c)
                        # panel.bind('<Button-1>', push_image)

                        panel.image = img
                        panel.grid(row=row_c, column=col_c, sticky=(N, W, E, S))
                        col_c += 1
                        if col_c > 6:
                            col_c = 0
                            row_c += 1
                        c += 1
                except:
                    print("ошибка вывода картинки", face.image_path)
                    db.del_face(face)
            count_faces += 1

        listbox_faces.grid(row=0, column=0, padx=10, pady=10)

def onCut():
    global listbox_faces, max_in_page, person, frame5,frame6
    #values = [listbox_faces.get(idx) for idx in listbox_faces.curselection()]
    #page_win_person_main = read_page()
    answer, person_buf = db.search_person("bufer")
    if answer:

        # for face in person.face:
        #     print(face)
        list_faces = []
        for n in listbox_faces.curselection():
            #print(int(page_win_person*max_in_page +n))
            print (page_win_person_main)
            print(int(n), (int(page_win_person_main * max_in_page + n)))
            #num = (int(page_win_person * max_in_page + n))
            list_faces.append( person.face[int(page_win_person_main*max_in_page +n)])
            #list_faces.append(person.face[int(n)])

            print(n)
        for f in list_faces:
            db.set_face(person_buf, f)

    refesh_persone()

def onPaste():
    global listbox_faces, person
    # переносим из bufer в выбранный профиль
    answer, person_buf = db.search_person("bufer")
    if answer:
        for f in person_buf.face:
            db.set_face(person, f)
    refesh_persone()

def onClick(index):
        global listbox_faces, max_in_page, page_win_person_main, frame5,frame6
        #page_win_person_main = read_page()

        #print("page_win_person", page_win_person_main)
        #values = [listbox_faces.get(idx) for idx in listbox_faces.curselection()]
        print("This is Button: " + str(index))
        #index = index + page_win_person*max_in_page
        #print("Face: " + str(index))
        flag= 0
        for i in listbox_faces.curselection():
            if i == index:
                flag=1

        if flag==1:
            print ("clear")
            listbox_faces.selection_clear(index, END)
        else:
            listbox_faces.selection_set(index)

        #print("page_win_person-", page_win_person_main)


def page_change(index):
    global person, max_in_page, page_win_person_main
    #page_win_person_main = read_page()
    page_win_person_main+=int(index)
    if page_win_person_main<=0:
        page_win_person_main=0
    if page_win_person_main>=len(person.face)/max_in_page:
        page_win_person_main = int(len(person.face)/max_in_page)

    #set_page(page_win_person_main)
    print("change page", page_win_person_main)

    refesh_persone()
    print("change page2", page_win_person_main)



def refresh_main_window():
    global all_person, person, selected_persone, filter, search_pole, frame1, frame5

    listbox.delete(0,END)
    all_person = db.select_all_person()

    search_pole = Entry(frame1, textvariable=sv)
    search_pole.grid(row=0, column=0, padx=10, pady=10)

    list_persons.clear()
    # добавляем в лист бокс данные
    for p in all_person:
        #listbox.insert(END, str(p.name+" "+p.second_name) )
        #для поиска с разным регистром приводим все в нижний
        index = p.name.lower().find(filter.lower())
        #print(index)
        if index>-1:
            list_persons.append(p)
            listbox.insert(END, str( str(len(p.face))+ " "+p.name ) )

    listbox.grid(row=1, column=0, padx=10, pady=10)


    refesh_persone()
    return

root = Tk()
root.title('Распознавание лиц. Проектная работа ЦРР')
root.geometry('1220x735+10+10') # ширина=500, высота=400, x=300, y=200
root.resizable(True, True) # размер окна может быть изменён только по горизонтали
root.iconbitmap(default="../face_recognition/img/cdr.ico")

frame1 = Frame(root)
frame1.grid(row=0, column=0,  sticky=(N))

frame2 = Frame(root)
frame2.grid(row=0, column=1,  sticky=(N))

frame3 = Frame(frame2)
frame3.grid(row=0, column=0,  sticky=(N, W))

frame4 = Frame(frame2)
frame4.grid(row=1, column=0,  sticky=( W))

frame5 = Frame(frame4)
frame5.grid(row=0, column=0,  sticky=(N, W))

frame6 = Frame(frame4)
frame6.grid(row=0, column=1,  sticky=(N))

print(present)

# frame1.pack()
e_name = Entry(frame3)
l_name = Label(frame3, text="Имя")

but_save = Button(frame3, text="Сохранить", command=savePerson)



sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback_search(sv))

search_pole = Entry(frame1, textvariable=sv)
search_pole.grid(row=0, column=0, padx=10, pady=10)

listbox = Listbox( frame1,  height=42, width=33 ,  bg = 'white' )
listbox.config( selectmode = SINGLE )   # see above EXTENDED
listbox.bind("<<ListboxSelect>>", OnSelect)
listbox.bind('<Button-3>', OnSelect2)



# e_name.grid(row=0, column=1, padx=20)
# l_name.grid(row=0, column=0, padx=20)
# but_save.grid(row=0, column=2, padx=20)



listbox_faces = Listbox(frame5, bg='white', height=33)
listbox_faces.config(selectmode=MULTIPLE)



#listbox_faces.grid(row=0, column=0,  padx=10, pady=10)

#     but_step1 = Button(frame5, text='<<', command=lambda i=-1: page_change(i)).grid(row=5, column=0, sticky=(N, W, E, S))
#     but_step2 = Button(frame5, text='>>', command=lambda i=1: page_change(i)).grid(row=6, column=0, sticky=(N, W, E, S))
#     but_cut = Button(frame5, text='Вырезать', command=onCut).grid(row=2, column=0, sticky=(N, W, E, S))
#     but_paste = Button(frame5, text='Вставить', command=onPaste).grid(row=1, column=0,
#                                                                                       sticky=(N, W, E, S))
# #but_del = Button(frame5, text='Удалить', command=lambda i=person: onDel(i)).grid(row=3, column=0, sticky=(N, W, E, S))

img = ImageTk.PhotoImage(Image.open('../face_recognition/img/present.png'))

panel = Label(frame6, image = img, width= 980, height= 675)
panel.pack(side = "bottom", fill = "both", expand = "yes")


refresh_main_window()

listbox.grid(row=1, column=0, padx=10, pady=10)

m = Menu(root)  # создается объект Меню на главном окне
root.config(menu=m)  # окно конфигурируется с указанием меню для него

fm = Menu(m)  # создается пункт меню с размещением на основном меню (m)
m.add_cascade(label="Захват изображение", menu=fm)  # пункту располагается на основном меню (m)
fm.add_command(label="Захват с камеры", command = OpenCameraWindow)  # формируется список команд пункта меню
# fm.add_command(label="New", command=new_win)
fm.add_command(label="Захват с файла ", command = OpenCameraWindowFile)
# fm.add_command(label="Exit", command=close_win)

hm = Menu(m)  # второй пункт меню
m.add_cascade(label="Работа", menu=hm)
#hm.add_command(label="Отладочные функции",  command=WorkWindows)
#hm.add_command(label="Сортировка",  command=SortWindows)
hm.add_command(label="Обновить список", command=refresh_main_window)
sfm = Menu(fm)
hm.add_cascade(label="Сортировка",menu=sfm)
sfm.add_command(label="Сортировка", command=SortWindows)
sfm.add_command(label="Сравнить лицо", command=ww.compare_person)
sfm.add_command(label="Разнести лица по персонам", command=ww.make_all_person)
#hm.add_command(label="About", command=about)

hm = Menu(m)  # второй пункт меню
m.add_cascade(label="Персона", menu=hm)
hm.add_command(label="Добавить персону", command=create_person)
ofm = Menu(fm)
hm.add_cascade(label="Удаления",menu=ofm)
ofm.add_command(label="Удалить пустые персоны", command=FaceAlgo.delEmptyFaces)
ofm.add_command(label="Удалить все персоны", command=ww.del_all_person)
ofm.add_command(label="Удалить выбранную персону", command=del_person)
ofm.add_command(label="Удалить пустые персоны",  command=delEmptyFaces)
ofm.add_command(label="Удалить буфер", command=delbuff)


#hm.add_command(label="About", command=about)


root.mainloop()
