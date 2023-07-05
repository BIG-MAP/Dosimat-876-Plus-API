# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 13:44:42 2023

@author: bandesha
"""
import serial
import tkinter as tk

# Serielle Verbindung zum Dosimeter herstellen
ser = None

# Liste der verfügbaren Methoden
methods = ["0,5ml-XDOS", "1ml-XDOS", "2ml-XDOS", "5ml-XDOS", "10ml-XDOS"] #muss gleichen einduetigen namen im Dosiamten haben

# Funktion zum Öffnen der seriellen Verbindung
def open_serial():
    global ser
    try:
        ser = serial.Serial(
            port='COM11',
            baudrate=19200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=True, # Software-Handshake aktivieren
            rtscts=False,
            dsrdtr=False
        )
        print("Serielle Verbindung erfolgreich geöffnet.")
    except serial.SerialException as e:
        print(f"Fehler beim Öffnen der seriellen Verbindung: {str(e)}")

# Funktion zum Schließen der seriellen Verbindung
def close_serial():
    global ser
    if ser is not None and ser.is_open:
        ser.close()
        print("Serielle Verbindung geschlossen.")
        


# Funktion zum Abrufen der verfügbaren Methoden auf dem Dosimeter
def get_available_methods():
    global methods
    methods = []  # Leere Liste für Methoden
    for method in methods:
        command = f"$L({method})\r\n"  # Befehl zum Laden der Methode
        ser.write(command.encode())
        response = ser.readline().decode().strip()  # Antwort vom Dosimeter lesen
        if response == "OK":
            methods.append(method)  # Methode zur Liste hinzufügen

# Funktion zum Anzeigen der Methoden auf der GUI
def show_methods():
    method_listbox.delete(0, tk.END)  # Vorhandene Einträge in der Listbox löschen
    for method in methods:
        method_listbox.insert(tk.END, method)  # Methoden zur Listbox hinzufügen

# Funktion zum Laden der ausgewählten Methode
def load_method():
    selected_method = method_listbox.get(tk.ACTIVE)  # Ausgewählte Methode aus der Listbox lesen
    command = f"$L({selected_method})\r\n"  # Befehl zum Laden der ausgewählten Methode
    ser.write(command.encode())  # Befehl über die serielle Verbindung senden
    
# Funktionen für die Befehle des Dosimeters
def start_dosing():
    command = "$G\r\n"  # Befehl zum Starten/Weiterführen des Dosierprozesses
    ser.write(command.encode())  # Befehl über die serielle Verbindung senden

def stop_dosing():
    command = "$S\r\n"  # Befehl zum Stoppen des Dosierprozesses
    ser.write(command.encode())  # Befehl über die serielle Verbindung senden

def hold_method():
    command = "$H\r\n"  # Befehl zum Anhalten der laufenden Methode
    ser.write(command.encode())  # Befehl über die serielle Verbindung senden

def scan_status():
    command = "$D\r\n"  # Befehl zum Abfragen des Instrumentstatus
    ser.write(command.encode())  # Befehl über die serielle Verbindung senden

def confirm_message():
    command = "$A(OK)\r\n"  # Befehl zur Bestätigung einer Nachricht auf dem Instrument
    ser.write(command.encode())  # Befehl über die serielle Verbindung senden

# Funktion beim Schließen des Fensters
def on_window_close():
    close_serial()  # Serielle Verbindung schließen
    root.destroy()  # GUI-Fenster schließen

# GUI erstellen
def create_gui():
    global root, method_listbox, response_listbox  # Zugriff auf die globale Variable
    root = tk.Tk()

    method_label = tk.Label(root, text="Methoden:")
    method_label.pack()

    method_listbox = tk.Listbox(root)
    method_listbox.pack()

    refresh_button = tk.Button(root, text="Methoden aktualisieren", command=show_methods)
    refresh_button.pack()
    
    load_button = tk.Button(root, text="Methode in Dosimeter laden", command=load_method)
    load_button.pack()
    
    response_label = tk.Label(root, text="Manuell Dosing:")
    response_label.pack()

    start_button = tk.Button(root, text="Start Dosing", command=start_dosing)
    start_button.pack()

    stop_button = tk.Button(root, text="Stop Dosing", command=stop_dosing)
    stop_button.pack()

    hold_button = tk.Button(root, text="Hold Method", command=hold_method)
    hold_button.pack()

    response_listbox = tk.Listbox(root)
    response_listbox.pack()

    scan_button = tk.Button(root, text="Scan Status", command=scan_status)
    scan_button.pack()

    confirm_button = tk.Button(root, text="Confirm Message", command=confirm_message)
    confirm_button.pack()
    
    quit_button = tk.Button(root, text="Quit", command=on_window_close)
    quit_button.pack()

    root.protocol("WM_DELETE_WINDOW", lambda: on_window_close())  # Funktion beim Schließen des Fensters aufrufen

    root.mainloop()

# Hauptfunktion zum Ausführen des Codes
def main():
    open_serial()  # Serielle Verbindung öffnen
    create_gui()

# Hauptprogramm starten
if __name__ == "__main__":
    main()
