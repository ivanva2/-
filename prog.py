
import psycopg2
from tkinter import ttk
from tkinter import *
from psycopg2 import Error


try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(
                                  host="localhost",
                                  user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="0",
                                  port="5432",
                                  database="stroi")

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Распечатать сведения о PostgreSQL
    print("Информация о сервере PostgreSQL")
    print(connection.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    
    cursor.execute("SELECT * FROM typesofmaterials;")
    # Получить результат
    record = cursor.fetchone()
    print("Вы подключены к - ", record, "\n")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
#finally:
   # if connection:
       # cursor.close()
       # connection.close()
       # print("Соединение с PostgreSQL закрыто")
class Dictionary:
    def __init__(self, window):

        self.wind = window
        self.wind.title('Строймагазин')

        
        frame = LabelFrame(self.wind, text = 'Введите новый вид матерьяла')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        Label(frame, text = 'id: ').grid(row = 1, column = 0)
        self.word = Entry(frame)
        self.word.focus()
        self.word.grid(row = 1, column = 1)
        Label(frame, text = 'Вид матерьяла: ').grid(row = 2, column = 0)
        self.meaning = Entry(frame)
        self.meaning.grid(row = 2, column = 1)
        ttk.Button(frame, text = 'Сохранить', command = self.add_word).grid(row = 3, columnspan = 2, sticky = W + E)
        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        # таблица слов и значений
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'id', anchor = CENTER)
        self.tree.heading('#1', text = 'Вид матерьяла', anchor = CENTER)
        ttk.Button(text = 'Удалить', command = self.delete_word).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Изменить',command=self.edit_word).grid(row = 5, column = 1, sticky = W + E)
        self.get_words()
        
   
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
        query = 'SELECT * FROM typesofmaterials;'
        db_rows = self.run_query(query,TRUE)
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = row[1])
     # валидация ввода
    def validation(self):
        return len(self.word.get()) != 0 and len(self.meaning.get()) != 0
    # добавление нового слова
    def add_word(self):
        if self.validation():
            query = f""" INSERT INTO typesofmaterials (id, typeofmaterial) VALUES({self.word.get()},'{self.meaning.get()}')"""
            self.run_query(query,False)
            self.message['text'] = 'Вид матерьяла {} добавлено в таблицу'.format(self.meaning.get())
            self.word.delete(0, END)
            self.meaning.delete(0, END)
        else:
            self.message['text'] = 'введите слово и значение'
        self.get_words()
    def delete_word(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Выберите слово, которое нужно удалить'
            return
        self.message['text'] = ''
        typeofmaterial= self.tree.item(self.tree.selection())['text']
        query = f'DELETE FROM typesofmaterials WHERE id = {typeofmaterial}'
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
    # внесение изменений в базу
    def edit_records(self, new_word, word, new_meaning, old_meaning):
        query = f"""UPDATE typesofmaterials SET id = {new_word}, typeofmaterial = '{new_meaning}'WHERE id = {word} AND typeofmaterial = '{old_meaning}'"""
        
        self.run_query(query,False)
        self.edit_wind.destroy()
        self.message['text'] = 'слово {} успешно изменено'.format(word)
        self.get_words()
    
    
if __name__ == '__main__':
    window = Tk()
    application = Dictionary(window)
    window.mainloop()