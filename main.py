import PySimpleGUI as sg
from datetime import datetime
import json

def save_order(name, surname, dob, product_table, filename):
    headings = ["Nazwa", "Ilosc", "Cena"]
    products = [dict(zip(headings, product)) for product in product_table]
    order = {
        'imie': name,
        'nazwisko': surname,
        'data_urodzenia': dob,
        'produkty': products
    }
    with open(filename, 'w') as f:
        json.dump(order, f)

product_table = []

sg.theme('DarkGreen4')
layout = [
    [sg.Text('Imię:'), sg.Input(key='-NAME-')],
    [sg.Text('Nazwisko:'), sg.Input(key='-SURNAME-')],
    [sg.Text('Data urodzenia:'), sg.Input(key='-DOB-')],
    [sg.Button('Dodaj produkt', key='-ADD-'), sg.Button('Zmień produkt', key='-EDIT-'),
     sg.Button('Usuń produkt', key='-REMOVE-')],
    [sg.Text('Zamówione produkty')],
    [sg.Table(values=[], headings=['Nazwa produktu', 'Ilość', 'Cena szt'], key='-TABLE-')],
    [sg.Button('Zapisz zamówienie', key='-SAVE-')]
]

window = sg.Window('Zamówienie', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == '-ADD-':
        add_layout = [
            [sg.Text('Nazwa:'), sg.InputText()],
            [sg.Text('Ilość:'), sg.InputText(key='-QUANTITY-')],
            [sg.Text('Cena produktu:'), sg.InputText(key='-PRICE-')],
            [sg.Button('Dodaj'), sg.Button('Anuluj')]
        ]
        add_window = sg.Window('Dodaj produkt', add_layout)

        while True:
            add_event, add_values = add_window.read()

            if add_event == sg.WINDOW_CLOSED or add_event == 'Anuluj':
                add_window.close()
                break
            try:
                price = float(add_values['-PRICE-'])
                quantity = int(add_values['-QUANTITY-'])
            except ValueError:
                sg.popup('Podane dane są nieprawidłowe!', title='Błąd', keep_on_top=True)
                continue

            if add_event == 'Dodaj':
                product_table.append([add_values[0], quantity, price])
                window['-TABLE-'].update(values=product_table)
                add_window.close()

    if event == '-REMOVE-' and product_table != []:

        try:
            selected_row = values['-TABLE-'][0]
            del product_table[selected_row]
            window['-TABLE-'].update(values=product_table)
            del selected_row
        except IndexError:
            continue

    if event == '-EDIT-':
        try:
            selected_product = values['-TABLE-'][0]

            if selected_product is not None:
                row_values = product_table[int(selected_product)]

                edit_layout = [
                    [sg.Text('Nazwa:'), sg.InputText(row_values[0], key='-NAME-')],
                    [sg.Text('Cena:'), sg.InputText(row_values[1], key='-PRICE-')],
                    [sg.Text('Ilość:'), sg.InputText(row_values[2], key='-QUANTITY-')],
                    [sg.Button('Zapisz zmiany'), sg.Button('Anuluj')]
                ]

                edit_window = sg.Window('Edycja produktu', edit_layout)

                while True:
                    edit_event, edit_values = edit_window.read()

                    if edit_event == sg.WIN_CLOSED or edit_event == 'Anuluj':
                        break
                    if edit_event == 'Zapisz zmiany':
                        product_table[int(selected_product)] = [edit_values['-NAME-'], edit_values['-PRICE-'],
                                                                edit_values['-QUANTITY-']]
                        window['-TABLE-'].update(values=product_table)
                        edit_window.close()
        except IndexError:
            continue

    if event == '-SAVE-' and product_table != []:

        filename = sg.popup_get_file('Wybierz plik do zapisu komentarzy', save_as=True,
                                     file_types=(('JSON files', '*.json'),))

        if not filename.endswith('.json'):
            filename += '.json'

        name = values['-NAME-']
        surname = values['-SURNAME-']
        dob = values['-DOB-']

        if all(char.isalpha() or char in ['-', ' '] for char in name) and \
                all(char.isalpha() or char in ['-', ' '] for char in surname) and \
                not (surname.startswith(('-', ' ')) or name.endswith(('-', ' ')) or surname.endswith(('-', ' '))
                     or name.startswith(('-', ' '))) and name and surname:
            try:
                date = datetime.strptime(dob, '%Y-%m-%d')
                if date.year < 1900 or date.year > 2007:
                    sg.popup('Rok urodzenia musi być pomiędzy 1900 a 2007!')
                else:
                    save_order(name, surname, dob, product_table, filename)
                    sg.popup('Zamówienie zostało zapisane do pliku json', title='Zamówienie zapisano', keep_on_top=True)

            except ValueError:
                sg.popup('Niepoprawny format daty!')
        else:
            sg.popup('Pola imię i nazwisko nie mogą być puste i mogą zawierać tylko litery, spacje i "-"')

window.close()
