
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
    cursor.execute("SELECT version();")
    # Получить результат
    record = cursor.fetchone()
    print("Вы подключены к - ", record, "\n")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
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
        ttk.Button(frame, text = 'Сохранить', ).grid(row = 3, columnspan = 2, sticky = W + E)
        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        # таблица слов и значений
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'id', anchor = CENTER)
        self.tree.heading('#1', text = 'Вид матерьяла', anchor = CENTER)
    def on_exit(self):
        if messagebox.askyesno("Выйти", "Закрыть программу?"):
            self.wind.destroy()
    def run_query(self, query, parameters = ()):
        connection = psycopg2.connect(
                                  host="localhost",
                                  user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="0",
                                  port="5432",
                                  database="stroi")
    # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        result = cursor.execute(query, parameters)
        connection.commit()
        return result
    
if __name__ == '__main__':
    window = Tk()
    application = Dictionary(window)
    window.mainloop()