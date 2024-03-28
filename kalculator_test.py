import unittest
import sqlite3
from tkinter import Tk
from tkinter import Entry
from tkinter import Button
from tkinter import Toplevel
from tkinter import Label
from tkinter import messagebox
from unittest.mock import patch
import kalkulator


class TestCalculatorApp(unittest.TestCase):
    @classmethod
    #Testing untuk menguji directory
    def setUpClass(cls):
        cls.root = Tk()
        cls.app = kalkulator

    #Testing untuk terminate Program
    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    #Testing untuk input data
    def setUp(self):
        self.entry = Entry(self.root)
        self.result_label = Label(self.root)
        self.history_button = Button(self.root)

    #Testing untuk perhitungan
    def test_calculate(self):
        with patch.object(messagebox, 'showerror') as mock_error:
            self.app.calculate()
            mock_error.assert_called_once()

        with patch.object(self.app, 'save_to_history'):
            self.entry.insert(0, "2+2")
            self.app.calculate()
            self.assertEqual(self.result_label.cget("text"), "Hasil: 4")

    #Testing untuk menghapus history Database
    def test_save_to_history(self):
        conn = sqlite3.connect('calculator_history.db')
        c = conn.cursor()
        c.execute("DELETE FROM history")
        conn.commit()
        conn.close()

        #Test untuk masukkan data ke Database
        self.app.save_to_history("2+2", 4)
        conn = sqlite3.connect('calculator_history.db')
        c = conn.cursor()
        c.execute("SELECT * FROM history")
        result = c.fetchone()
        conn.close()
        self.assertEqual(result, ("2+2", 4))

    #Test untuk menampilkan history
    def test_show_history(self):
        with patch.object(messagebox, 'showinfo') as mock_info:
            self.app.show_history()
            mock_info.assert_called_once_with("Info", "Histori kosong")

        with patch.object(Toplevel, 'title') as mock_title:
            self.app.show_history()
            mock_title.assert_called_once_with("History")

    #Test untuk menampilkan data history yang dihapus dan ditambahkan
    def test_insert_history_result(self):
        with patch.object(Entry, 'delete') as mock_delete:
            with patch.object(Entry, 'insert') as mock_insert:
                self.app.insert_history_result(4)
                mock_delete.assert_called_once_with(0, self.app.tk.END)
                mock_insert.assert_called_once_with(self.app.tk.END, "4")

    #Test untuk menguji tombol Clear
    def test_clear_entry(self):
        with patch.object(Entry, 'delete') as mock_delete:
            self.app.clear_entry()
            mock_delete.assert_called_once_with(0, self.app.tk.END)

    #Test untuk memastikan semua tombol berfungsi
    def test_button_clicks(self):
        with patch.object(Entry, 'insert') as mock_insert:
            buttons = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '+', '%', '=', 'C']
            for button in buttons:
                self.app.on_button_click(button)
            self.assertEqual(mock_insert.call_count, len(buttons))


if __name__ == '__main__':
    unittest.main()
