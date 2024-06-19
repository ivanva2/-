
import psycopg2
from tkinter import ttk
from tkinter import messagebox, Menu, ttk, Label, Entry
from tkinter import *
import hashlib
from psycopg2 import Error
def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(parent.wind)
        self.window.title("Вход в систему")

        ttk.Label(self.window, text="Имя пользователя").grid(row=0)
        ttk.Label(self.window, text="Пароль").grid(row=1)

        self.username_entry = ttk.Entry(self.window)
        self.password_entry = ttk.Entry(self.window, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        ttk.Button(self.window, text="Войти",command=self.attempt_login ).grid(row=2, column=1)
        ttk.Button(self.window, text="Регистрация",command=self.register ).grid(row=3, column=1)
    
    def attempt_login(self):
        username = self.username_entry.get()
        password = hash_password(self.password_entry.get())
        connection = psycopg2.connect(
                                  host="localhost",
                                  user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="0",
                                  port="5432",
                                  database="stroi")
    # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=%s AND password_hash=%s', (username, password))
        if cursor.fetchone():
            self.window.destroy()  # Закрыть окно входа
            self.parent.wind.deiconify()  # Показать основное окно
        else:
            messagebox.showerror('Ошибка', 'Неверный логин или пароль')
        connection.close()

    def register(self):
        new_username = self.username_entry.get()
        new_password = hash_password(self.password_entry.get())
        if new_username and new_password:
            try:
                connection = psycopg2.connect(
                                  host="localhost",
                                  user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="0",
                                  port="5432",
                                  database="stroi")
                cursor = connection.cursor()
                cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (new_username, new_password))
                connection.commit()
                messagebox.showinfo('Успех', 'Регистрация прошла успешно')
            except psycopg2.IntegrityError:
                messagebox.showerror('Ошибка', 'Пользователь с таким именем уже существует')
            finally:
                connection.close()
        else:
            messagebox.showerror('Ошибка', 'Логин и пароль не могут быть пустыми')


class Dictionary:
    global a
    a=1
    def __init__(self, window):
        
        super().__init__()
        
        self.wind = window
        self.wind.withdraw()  # Скрыть основное окно
        self.wind.title('Строймагазин')
        main_menu = Menu()
        file_menu = Menu()
        self.login_window = LoginWindow(self)
        
        file_menu.add_command(label="Вид матерьяла",command = lambda: self.click_vid())
        file_menu.add_command(label="Матерьялы",command=lambda: self.click_mat())
        file_menu.add_separator()

        
        main_menu.add_cascade(label="таблицы", menu=file_menu)
        main_menu.add_cascade(label="новое",command = lambda: self.novoe())
        window.config(menu=main_menu)
        ttk.Button( text = 'поиск',command=self.poisk).grid(row = 5, column = 0, sticky = W + E)
        self.poiskk = Entry()
        self.poiskk.focus()
        self.poiskk.grid(row = 5, column = 1)

        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 6, column = 0, columnspan = 2, sticky = W + E)
        # таблица слов и значений
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 7, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'id', anchor = CENTER)
        self.tree.heading('#1', text = 'Вид матерьяла', anchor = CENTER)
        
        ttk.Button(text = 'Удалить', command = self.delete_word).grid(row = 8, column = 0, sticky = W + E)
        ttk.Button(text = 'Изменить',command=self.edit_word).grid(row = 8, column = 1, sticky = W + E)
        self.get_words()
    def show(self):
        ''' Показать основное окно после успешного входа '''
        self.update()
        self.deiconify()
    def click_mat(self):
        global a
        a = 2
        self.tree.destroy()
        self.tree = ttk.Treeview(height=10, columns=('размер', 'Характеристика', 'количество', 'Вид матерьяла'))
        self.tree.grid(row=7, column=0, columnspan=5)
        
        self.tree.heading('#0', text = 'id', anchor = CENTER)
        self.tree.heading('#1', text = 'размер', anchor = CENTER)
        self.tree.heading('#2', text = 'Характеристика', anchor = CENTER)
        self.tree.heading('#3', text = 'количество', anchor = CENTER)
        self.tree.heading('#4', text = 'Вид матерьяла', anchor = CENTER)
        window.update()
        window.update_idletasks()
        self.get_words()
        return a
    def click_vid(self):
        global a
        a = 1
        self.tree.destroy()
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 7, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'id', anchor = CENTER)
        self.tree.heading('#1', text = 'Вид матерьяла', anchor = CENTER)
        window.update()
        window.update_idletasks()
        self.get_words()
        return a

        

        
        
   
    def run_query(self, query,a, parameters = ()):
        connection = psycopg2.connect(
                                  host="localhost",
                                  user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="0",
                                  port="5432",
                                  database="stroi")
    # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        if a:
            record = cursor.fetchall()
        connection.commit()
        if a:
            return record 
    def get_words(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        global a
        if a==1:
            query = 'SELECT * FROM typesofmaterials;'
        if a==2:
            query = 'SELECT * FROM materials;'
        db_rows = self.run_query(query,TRUE)
        for row in db_rows:
            if a==1:
                self.tree.insert('', 0, text = row[0], values = row[1])
            if a==2:
                self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
     # валидация ввода
    def validation(self):
        return len(self.word.get()) != 0 and len(self.meaning.get()) != 0
    # добавление нового слова
    def add_word(self):
        if self.validation():
            global a
            if a==1:
                query = f""" INSERT INTO typesofmaterials (id, typeofmaterial) VALUES({self.word.get()},'{self.meaning.get()}')"""
            if a==2:
                query = f""" INSERT INTO materials (id, size, characteristic, quantity, material_id) VALUES({self.word.get()},'{self.meaning.get()}','{self.xarkt.get()}',{self.kol.get()},{self.vidd.get()})"""
            self.run_query(query,False)
            self.message['text'] = 'Вид матерьяла {} добавлено в таблицу'.format(self.meaning.get())
            self.word.delete(0, END)
            self.meaning.delete(0, END)
            if a==2:
                self.xarkt.delete(0, END)
                self.kol.delete(0, END)
                self.vidd.delete(0, END)

        else:
            self.message['text'] = 'введите слово и значение'
        self.get_words()
    #удаление
    def delete_word(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Выберите слово, которое нужно удалить'
            return
        self.message['text'] = ''
        typeofmaterial= self.tree.item(self.tree.selection())['text']
        global a
        if a==1:
            query = f'DELETE FROM typesofmaterials WHERE id = {typeofmaterial}'
        if a==2:
            query = f'DELETE FROM materials WHERE id = {typeofmaterial}'
        self.run_query(query,False, )
        self.message['text'] = 'Слово {} успешно удалено'.format(typeofmaterial)
        self.get_words()
    # рeдактирование слова и/или значения
    def edit_word(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Выберите строку для изменения'
            return
        
        global a
        if a==1:
            word = self.tree.item(self.tree.selection())['text']
            old_meaning = self.tree.item(self.tree.selection())['values'][0]
            self.edit_wind = Toplevel()
            self.edit_wind.title = 'Изменить значение'
            Label(self.edit_wind, text = 'Прежнее id:').grid(row = 0, column = 1)
            Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = word), state = 'readonly').grid(row = 0, column = 2)
        
            Label(self.edit_wind, text = 'Новое id:').grid(row = 1, column = 1)
            # предзаполнение поля
            new_word = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = word))
            new_word.grid(row = 1, column = 2)


            Label(self.edit_wind, text = 'Прежнее вид матерьяла:').grid(row = 2, column = 1)
            Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_meaning), state = 'readonly').grid(row = 2, column = 2)
 
            Label(self.edit_wind, text = 'Новое вид матерьяла:').grid(row = 3, column = 1)
            # предзаполнение поля
            new_meaning= Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_meaning))
            new_meaning.grid(row = 3, column = 2)

            Button(self.edit_wind, text = 'Изменить', command = lambda: self.edit_records(new_word.get(), word, new_meaning.get(), old_meaning)).grid(row = 4, column = 2, sticky = W)
            self.edit_wind.mainloop()
        if a==2:
            # Прежние значения
            selected_item = self.tree.selection()[0]  # Предполагается, что выбран один элемент
            word = self.tree.item(selected_item)['text']
            old_values = self.tree.item(selected_item)['values']
        
            self.edit_wind = Toplevel()
            self.edit_wind.title('Изменить значения')
            Label(self.edit_wind, text='Прежнее id:').grid(row=0, column=1)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=word), state='readonly').grid(row=0, column=2)
        
            Label(self.edit_wind, text='Прежний размер:').grid(row=1, column=1)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_values[0]), state='readonly').grid(row=1, column=2)
        
            Label(self.edit_wind, text='Прежняя характеристика:').grid(row=2, column=1)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_values[1]), state='readonly').grid(row=2, column=2)
        
            Label(self.edit_wind, text='Прежнее количество:').grid(row=3, column=1)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_values[2]), state='readonly').grid(row=3, column=2)
        
            Label(self.edit_wind, text='Прежний вид матерьяла:').grid(row=4, column=1)
            Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_values[3]), state='readonly').grid(row=4, column=2)

            # Новые значения
            Label(self.edit_wind, text='Новое id:').grid(row=0, column=3)
            new_id = Entry(self.edit_wind)
            new_id.grid(row=0, column=4)

            Label(self.edit_wind, text='Новый размер:').grid(row=1, column=3)
            new_size = Entry(self.edit_wind)
            new_size.grid(row=1, column=4)

            Label(self.edit_wind, text='Новая характеристика:').grid(row=2, column=3)
            new_characteristic = Entry(self.edit_wind)
            new_characteristic.grid(row=2, column=4)

            Label(self.edit_wind, text='Новое количество:').grid(row=3, column=3)
            new_quantity = Entry(self.edit_wind)
            new_quantity.grid(row=3, column=4)

            Label(self.edit_wind, text='Новый вид матерьяла:').grid(row=4, column=3)
            new_material_type = Entry(self.edit_wind)
            new_material_type.grid(row=4, column=4)

            Button(self.edit_wind, text='Изменить', command=lambda: self.edit_records1(new_id.get(), word, new_size.get(), old_values[0], new_characteristic.get(), old_values[1], new_quantity.get(), old_values[2], new_material_type.get(), old_values[3])).grid(row=5, column=2, sticky=W)
            self.edit_wind.mainloop()
    #новое
    def novoe(self):
        self.message['text'] = ''
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Добавить новое значение'
        global a
        if a==1:

            frame = LabelFrame(self.edit_wind, text = 'Введите новый вид матерьяла')
            frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
            Label(frame, text = 'id: ').grid(row = 1, column = 0)
            self.word = Entry(frame)
            self.word.focus()
            self.word.grid(row = 1, column = 1)
            Label(frame, text = 'Вид матерьяла: ').grid(row = 2, column = 0)
            self.meaning = Entry(frame)
            self.meaning.grid(row = 2, column = 1)
            ttk.Button(frame, text = 'Сохранить', command = self.add_word).grid(row = 3, columnspan = 2, sticky = W + E)
        if a==2:
            frame = LabelFrame(self.edit_wind, text = 'Введите новый вид матерьяла')
            frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
            Label(frame, text = 'id: ').grid(row = 1, column = 0)
            self.word = Entry(frame)
            self.word.focus()
            self.word.grid(row = 1, column = 1)
            Label(frame, text = 'размер: ').grid(row = 2, column = 0)
            self.meaning = Entry(frame)
            self.meaning.grid(row = 2, column = 1)
            Label(frame, text = 'Характеристика: ').grid(row = 3, column = 0)
            self.xarkt = Entry(frame)
            self.xarkt.grid(row = 3, column = 1)
            Label(frame, text = 'количество: ').grid(row = 4, column = 0)
            self.kol = Entry(frame)
            self.kol.grid(row = 4, column = 1)
            Label(frame, text = 'Вид матерьяла: ').grid(row = 5, column = 0)
            self.vidd = Entry(frame)
            self.vidd.grid(row = 5, column = 1)
            ttk.Button(frame, text = 'Сохранить', command = self.add_word).grid(row = 6, columnspan = 2, sticky = W + E)
    # внесение изменений в базу
    def edit_records(self, new_word, word, new_meaning, old_meaning):
      
        query = f"""UPDATE typesofmaterials SET id = {new_word}, typeofmaterial = '{new_meaning}'WHERE id = {word} AND typeofmaterial = '{old_meaning}'"""
        self.run_query(query,False)
        self.edit_wind.destroy()
        self.message['text'] = 'слово {} успешно изменено'.format(word)
        self.get_words()
    def poisk(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        x=self.poiskk.get()
        global a 
        if x.isdigit():
            if a==1:
                query=f"""SELECT * FROM typesofmaterials WHERE id = {self.poiskk.get()}  """
            if a==2:
                query=f"""SELECT * FROM materials WHERE id = {self.poiskk.get()} or quantity = {self.poiskk.get()} or material_id ={self.poiskk.get()}"""
        else:
            if a==1:
                query=f"""SELECT * FROM typesofmaterials WHERE  typeofmaterial = '{self.poiskk.get()}' """
            if a==2:
                query=f"""SELECT * FROM materials WHERE  size  = '{self.poiskk.get()}' or characteristic= '{self.poiskk.get()}'"""
        db_rows = self.run_query(query,TRUE)
        for row in db_rows:
            if a==1:
                self.tree.insert('', 0, text = row[0], values = row[1])
            if a==2:
                self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
    def edit_records1(self, new_id, old_id, new_size, old_size, new_characteristic, old_characteristic, new_quantity, old_quantity, new_material_type, old_material_type):
        
        query = f"""UPDATE  materials SET id = {new_id}, size = '{new_size}', characteristic='{new_characteristic}',quantity ={new_quantity}, material_id ={new_material_type} WHERE id = {old_id}"""
        self.run_query(query,False)
        self.edit_wind.destroy()
        self.message['text'] = 'мательял {} успешно изменен'.format(new_characteristic)
        self.get_words()
    

        
if __name__ == '__main__':
    window = Tk()
    application = Dictionary(window)
    window.mainloop()