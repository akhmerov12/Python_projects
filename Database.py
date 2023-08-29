from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.metrics import sp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from psycopg2 import sql
import pyAesCrypt
import os
import cryptography
from cryptography.fernet import Fernet

from kivy.uix.tabbedpanel import TabbedPanel
from config import host, user, password, db_name

import psycopg2
import re

class MainApp(MDApp):
    def build(self):
        self.screen = Screen()
        self.add_button = Button(text="Открыть", font_size=13, size_hint=[.15, 0.05],
                                 pos_hint={'center_x': 0.1, 'center_y': 0.17}, on_press=self.add_table)
        self.add_button1 = Button(text="Расшифровать", font_size=13, size_hint=[.15, 0.05],
                                pos_hint={'center_x': 0.1, 'center_y': 0.1}, on_press=self.decrypt_all_rows_in_database)
        self.textInput1 = TextInput(multiline = True, font_size=13, size_hint=[.15, 0.05],
                                    hint_text= "Имя таблицы", pos_hint={'center_x': 0.3, 'center_y': 0.17})
        self.textInput2 = TextInput(multiline=True, font_size=13, size_hint=[.15, 0.05],
                                    hint_text="Введите пароль", pos_hint={'center_x': 0.3, 'center_y': 0.1})
        self.screen.add_widget(self.textInput1)
        self.screen.add_widget(self.add_button)
        self.screen.add_widget(self.add_button1)
        self.screen.add_widget(self.textInput2)
        return self.screen

    def load_key(self):
        """
        Loads the key from the current directory named `key.key`
        """
        return open("key.key", "rb").read()


    def decrypt_all_rows_in_database(self, args):
        if self.textInput2.text == 'q1w2e3r4':
            key = self.load_key()
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
            )
            cur = conn.cursor()
            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
            tables = cur.fetchall()

            for table in tables:
                cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier((table[0]))))
                rows = cur.fetchall()
                for row in rows:
                    f = Fernet(key)
                    encrypted = f.decrypt(row[1]).decode()
                    cur.execute(f"UPDATE {table[0]} SET comments='{encrypted}' WHERE number={row[0]}")
                    conn.commit()

            cur.close()
            conn.close()

    def add_table(self, args):
            name = self.textInput1.text
            print(type(name))
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
            )
            table_name = name
            cur = conn.cursor()
            cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            rows = cur.fetchall()
            for i in range(len(rows)):
                rows[i] = list(rows[i])
            for row in rows:
                row[1] = re.sub("^\s+|\n|\r|\s+$", '', row[1])
            self.lastNumber = rows[len(rows) - 1][0] + 2
            print(self.lastNumber)
            table = MDDataTable(
                pos_hint = {'center_x': 0.5, 'center_y': 0.5},
                size_hint =(0.9, 0.6),
                check = True,
                use_pagination = True,
                column_data = [
                    ("Number", dp(70)),
                    ("Comment", sp(670), sp(100)),
                ],
                row_data=rows
            )

            table.bind(on_check_press=self.checked)



            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_palette = 'BlueGray'
            self.textInput = TextInput(multiline=True, size_hint=[.3, 0.14], pos_hint={'center_x': 0.74, 'center_y': 0.12})
            self.screen.add_widget(self.textInput)

            self.button = Button(text="Add comment", font_size=13, size_hint=[.15, 0.05], pos_hint={'center_x': 0.5, 'center_y': 0.17}, on_press = self.add_comment)


            self.screen.add_widget(self.button)

            self.screen.add_widget(table)
            conn.close()
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
            )
            cur = conn.cursor()
            cur.execute(sql.SQL("SELECT MAX(number) FROM {}").format(sql.Identifier(table_name)))
            max_number1 = cur.fetchall()
            max_number2 = list(max_number1[0])
            self.max_number = max_number2[0] + 1
    def checked(self, instance_table, current_row):
        temp = current_row
        name = self.textInput1.text
        table_name = name
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        cur = conn.cursor()
        n = temp[0]
        print(type(temp[0]))
        cur.execute(sql.SQL("DELETE FROM {} WHERE number = (%s)").format(sql.Identifier(table_name)), (n,))
        conn.commit()
        conn.close()

    def add_comment(self, args):
        name = self.textInput1.text
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )
        cur = conn.cursor()
        cur.execute(sql.SQL("INSERT INTO {} (number, comments) VALUES (%s, %s)").format(sql.Identifier(name)), (self.max_number, self.textInput.text,))
        conn.commit()
        conn.close()


MainApp().run()