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



window.close()
