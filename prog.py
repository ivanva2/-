
import psycopg2
from tkinter import ttk
from tkinter import messagebox, Menu, ttk, Label, Entry
from tkinter import *
import hashlib
from psycopg2 import Error
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Materials(Base):
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True)
    size = Column(String(50), nullable=False)
    characteristic = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    material_id = Column(Integer, ForeignKey('typesofmaterials.id'))

    # Явное указание условия соединения
    typesofmaterials = relationship("TypesOfMaterials", back_populates="materials",
                                    primaryjoin="Materials.material_id==TypesOfMaterials.id")

    def __repr__(self):
        return f"<Materials(size='{self.size}', characteristic='{self.characteristic}', quantity={self.quantity}, material_id={self.material_id})>"

class TypesOfMaterials(Base):
    __tablename__ = 'typesofmaterials'
    
    id = Column(Integer, primary_key=True)
    typeofmaterial = Column(String(50), nullable=False)

    # Определение отношения для обратной ссылки
    materials = relationship("Materials", order_by=Materials.id, back_populates="typesofmaterials")

    def __repr__(self):
        return f"<typesofmaterials(typeofmaterial='{self.typeofmaterial}')>"



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
    a=1
    b=2
    def __init__(self, window):
        super().__init__()
        self.session = Session()
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

        Dictionary.a = 2
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
       
        Dictionary.a = 1
        self.tree.destroy()
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 7, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'id', anchor = CENTER)
        self.tree.heading('#1', text = 'Вид матерьяла', anchor = CENTER)
        window.update()
        window.update_idletasks()
        self.get_words()
        return a

        

        
    def run_query1(self, orm_class, parameters={}):
        # Предполагается, что parameters - это словарь для фильтрации
        result = self.session.query(orm_class).filter_by(**parameters).all()
        return result    
    

        
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
        if Dictionary.b==1:
            if Dictionary.a==1:
                query = 'SELECT * FROM typesofmaterials;'
            if Dictionary.a==2:
                query = 'SELECT * FROM materials;'
            db_rows = self.run_query(query,TRUE)
            for row in db_rows:
                if Dictionary.a==1:
                    self.tree.insert('', 0, text = row[0], values = row[1])
                if Dictionary.a==2:
                    self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
        if Dictionary.b==2:
            if Dictionary.a == 1:
                db_rows = self.run_query1(TypesOfMaterials)
                for row in db_rows:
                    self.tree.insert('', 0, text=row.id, values=(row.typeofmaterial,))
            elif Dictionary.a == 2:
                db_rows = self.run_query1(Materials)
                for row in db_rows:
                    self.tree.insert('', 0, text=row.id, values=(row.size, row.characteristic, row.quantity, row.material_id ))
    
     # валидация ввода
    def validation(self):
        return len(self.word.get()) != 0 and len(self.meaning.get()) != 0
    # добавление нового слова
    def add_word(self):
        if self.validation():
            if Dictionary.b==1:
                if Dictionary.a==1:
                    query = f""" INSERT INTO typesofmaterials (id, typeofmaterial) VALUES({self.word.get()},'{self.meaning.get()}')"""
                if Dictionary.a==2:
                    query = f""" INSERT INTO materials (id, size, characteristic, quantity, material_id) VALUES({self.word.get()},'{self.meaning.get()}','{self.xarkt.get()}',{self.kol.get()},{self.vidd.get()})"""
                self.run_query(query,False)
                self.message['text'] = 'Вид матерьяла {} добавлено в таблицу'.format(self.meaning.get())
            if Dictionary.b==2:
                session = Session()
                if Dictionary.a == 2:
                    # Добавление нового материала
                    new_material = Materials(
                    id=self.word.get(),
                    size=self.meaning.get(),
                    characteristic=self.xarkt.get(),
                    quantity=self.kol.get(),
                    material_id=self.vidd.get()
                    )
                    session.add(new_material)
                else:
                    # Добавление нового типа материала
                    new_type_of_material = TypesOfMaterials(
                    id=self.word.get(),
                    typeofmaterial=self.meaning.get()
                    )
                    session.add(new_type_of_material)
                session.commit()
                session.close()
            self.word.delete(0, END)
            self.meaning.delete(0, END)
            if Dictionary.a==2:
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
        if Dictionary.b==1:
            if Dictionary.a==1:
                query = f'DELETE FROM typesofmaterials WHERE id = {typeofmaterial}'
            if Dictionary.a==2:
                query = f'DELETE FROM materials WHERE id = {typeofmaterial}'
            self.run_query(query,False, )
        elif Dictionary.b==2:
            session = Session()
            if Dictionary.a == 1:
                # Поиск и удаление типа материала по id
                type_of_material_to_delete = session.query(TypesOfMaterials).filter_by(id=typeofmaterial).first()
                if type_of_material_to_delete:
                    session.delete(type_of_material_to_delete)
            elif Dictionary.a == 2:
                # Поиск и удаление материала по id
                material_to_delete = session.query(Materials).filter_by(id=typeofmaterial).first()
                if material_to_delete:
                    session.delete(material_to_delete)

            # Подтверждение изменений
            session.commit()

            # Закрытие сессии
            session.close()
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
        

        if Dictionary.a==1:
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
        if Dictionary.a==2:
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

        if Dictionary.a==1:

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
        if Dictionary.a==2:
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
        if Dictionary.b==1:
            query = f"""UPDATE typesofmaterials SET id = {new_word}, typeofmaterial = '{new_meaning}'WHERE id = {word} AND typeofmaterial = '{old_meaning}'"""
            self.run_query(query,False)
            
        elif Dictionary.b==2:      
            session = Session()
            new_word_id = new_word  
            new_typeofmaterial = new_meaning  
            # Получение старых значений
            old_word_id = word  
            old_typeofmaterial = old_meaning  
            # Поиск объекта по старым значениям
            type_of_material_to_update = session.query(TypesOfMaterials).filter_by(id=old_word_id, typeofmaterial=old_typeofmaterial).first()

            if type_of_material_to_update:
    # Обновление атрибутов объекта
                type_of_material_to_update.id = new_word_id
                type_of_material_to_update.typeofmaterial = new_typeofmaterial

    # Подтверждение изменений
                session.commit()
                session.close()
        self.edit_wind.destroy()
        self.message['text'] = 'слово {} успешно изменено'.format(word)
        self.get_words()
    def poisk(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        x=self.poiskk.get()
        if Dictionary.b==1:
            if x.isdigit():
                if Dictionary.a==1:
                    query=f"""SELECT * FROM typesofmaterials WHERE id = {self.poiskk.get()}  """
                if Dictionary.a==2:
                    query=f"""SELECT * FROM materials WHERE id = {self.poiskk.get()} or quantity = {self.poiskk.get()} or material_id ={self.poiskk.get()}"""
            else:
                if Dictionary.a==1:
                    query=f"""SELECT * FROM typesofmaterials WHERE  typeofmaterial = '{self.poiskk.get()}' """
                if Dictionary.a==2:
                    query=f"""SELECT * FROM materials WHERE  size  = '{self.poiskk.get()}' or characteristic= '{self.poiskk.get()}'"""
            db_rows = self.run_query(query,TRUE)
            for row in db_rows:
                if Dictionary.a==1:
                    self.tree.insert('', 0, text = row[0], values = row[1])
                if Dictionary.a==2:
                    self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
        if Dictionary.b==2:
            session = Session()
            if x.isdigit():
            # Поиск по id
                if Dictionary.a == 1:
                    results = session.query(TypesOfMaterials).filter_by(id=int(self.poiskk.get())).all()
                elif Dictionary.a == 2:
                    id_value = int(self.poiskk.get())
                    results = session.query(Materials).filter((Materials.id == id_value) | 
                                                        (Materials.quantity == id_value) | 
                                                        (Materials.material_id == id_value)).all()
            else:
    # Поиск по текстовому полю
                if Dictionary.a == 1:
                    results = session.query(TypesOfMaterials).filter_by(typeofmaterial=self.poiskk.get()).all()
                elif Dictionary.a == 2:
                    search_value = self.poiskk.get()
                    results = session.query(Materials).filter((Materials.size == search_value) | 
                                                 (Materials.characteristic == search_value)).all()

# Вставка результатов в дерево
            for row in results:
                if Dictionary.a == 1:
                    self.tree.insert('', 0, text=row.id, values=row.typeofmaterial)
                elif Dictionary.a == 2:
                    self.tree.insert('', 0, text=row.id, values=(row.size, row.characteristic, row.quantity, row.material_id))

# Закрытие сессии
            session.close()
    def edit_records1(self, new_id, old_id, new_size, old_size, new_characteristic, old_characteristic, new_quantity, old_quantity, new_material_type, old_material_type):
        if Dictionary.b==1:
            query = f"""UPDATE  materials SET id = {new_id}, size = '{new_size}', characteristic='{new_characteristic}',quantity ={new_quantity}, material_id ={new_material_type} WHERE id = {old_id}"""
            self.run_query(query,False)
        elif Dictionary.b==2:
            session = Session()


            old_id_value = old_id  
            new_id_value = new_id  
            new_size_value = new_size  


            material_to_update = session.query(Material).filter_by(id=old_id_value).first()

            if material_to_update:
                # Обновление атрибутов объекта
                material_to_update.id = new_id_value
                material_to_update.size = new_size_value
                material_to_update.characteristic = new_characteristic
                material_to_update.quantity = new_quantity
                material_to_update.material_id = new_material_type

    # Подтверждение изменений
            session.commit()

            # Закрытие сессии
            session.close()
        self.edit_wind.destroy()
        self.message['text'] = 'мательял {} успешно изменен'.format(new_characteristic)
        self.get_words()
    

        
if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:0@localhost:5432/stroi')
    Session = sessionmaker(bind=engine)
    window = Tk()
    application = Dictionary(window)
    window.mainloop()