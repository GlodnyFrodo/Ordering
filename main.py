import PySimpleGUI as sg

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


window.close()
