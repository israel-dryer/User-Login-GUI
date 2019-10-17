'''
    A user login GUI adapted for PySimpleGUI (original tkinter)
    Adapted by:     Israel Dryer, israel.dryer@gmail.com
    Modified:       2019-10-17
    Original Author I_Know_Python
    Original Video  https://www.youtube.com/watch?v=lcBoYduaUy0&feature=youtu.be+

    This codebase uses 24% fewer characters than the original tkinter implementation

'''
import PySimpleGUI as sg 
from sqlite3 import connect

# ---- APPLICATION GUI LAYOUT ---------------------------------------------- #
main_layout = [
    [sg.Text('What do you want to do?')],
    [sg.Button('login', size=(8,1)), sg.Button('sign-up', size=(8,1))]]

login_layout = [
    [sg.Text('username'), sg.Input(key='username')],
    [sg.Text('password'), sg.Input(password_char='*', key='password')],
    [sg.Button('login', bind_return_key=True)]]

signup_layout = [
    [sg.Text('username'), sg.Input(key='username')],
    [sg.Text('email'), sg.Input(key='email')],
    [sg.Text('password'), sg.Input(password_char='*', key='password')],
    [sg.Button('sign-up', bind_return_key=True)]]

main_window = sg.Window('Main Menu', main_layout, element_justification='center')
login_window = sg.Window('Login', login_layout, element_justification='right')
signup_window = sg.Window('Create Account', signup_layout, element_justification='right')

# ---- APPLICATION FUNCTIONS ------------------------------------------------#
def create_db():
    ''' create database if one does not already exist '''
    with connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)")    


def login(values):
    ''' obtain user credentials and validate against database '''
    with connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test WHERE username = ? AND password = ?", (values['username'], values['password']))        
        check = len(cursor.fetchall())
        # login if credentials are found, otherwise alert user
    if check == 1:
        sg.popup('You are now logged in.')
    else:
        sg.popup_error('Invalid username or password')


def signup(values):
    ''' create user accounts based on supplied parameters, if account does not already exist '''
    with connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test WHERE username = ?", (values['username'],))
        check = len(cursor.fetchall())
        # add to database if not existing, otherwise alert user
        print(check)
        if check == 0:
            cursor.execute("INSERT INTO test VALUES(NULL, ?, ?, ?)", (values['username'], values['email'], values['password']))
            sg.popup('Username {} has been created'.format(values['username']))
        else:
            sg.popup_error('Username {} already exists'.format(values['username']))

# ---- MAIN EVENT LOOP ----------------------------------------------------- #
create_db()

while True:
    event, values = main_window.read()
    if event in (None, 'Cancel'):
        break
    if event == 'login':
        main_window.close()
        log_event, log_values = login_window.read()
        if log_event == 'login':
            login(log_values)
            break
    if event == 'sign-up':
        main_window.close()
        sign_event, sign_values = signup_window.read()
        if sign_event == 'sign-up':
            signup(sign_values)
            break