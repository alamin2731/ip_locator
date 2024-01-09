import tkinter as tk
from tkinter import scrolledtext
import requests
import threading
from tkinter import messagebox

def get_country_from_ip(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        iso_code = data.get('country', 'N/A')

        if iso_code != 'N/A':
            country_info = requests.get(f'https://restcountries.com/v3/alpha/{iso_code.lower()}')
            country_data = country_info.json()
            country_name = country_data[0]['name']['common']
            return country_name
        else:
            return 'N/A'
    except Exception as e:
        return 'N/A'

def process_ip_addresses():
    ip_addresses = ip_text.get("1.0", "end-1c").splitlines()
    result_text.delete(1.0, tk.END)  

    for ip in ip_addresses:
        country = get_country_from_ip(ip)
        result_text.insert(tk.END, f"{ip} : {country}\n")
        result_text.update_idletasks()  

def on_button_click():
    threading.Thread(target=process_ip_addresses).start()

def show_about():
    messagebox.showinfo("About", "IP Address to Country Lookup\n\nVersion 1.0\nDeveloped by Alamin")

window = tk.Tk()
window.title("IP Address to Country Lookup")
window.geometry("600x400")

menubar = tk.Menu(window)
window.config(menu=menubar)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)

help_menu.add_command(label="About", command=show_about)

# IP Address input
ip_label = tk.Label(window, text="Enter IP Addresses (one per line):")
ip_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

ip_text = scrolledtext.ScrolledText(window, width=30, height=8, wrap=tk.WORD)
ip_text.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="w")

# Button to perform the lookup
lookup_button = tk.Button(window, text="Lookup", command=on_button_click)
lookup_button.grid(row=0, column=2, pady=(10, 5), padx=10, sticky="w")

# Result display
result_label = tk.Label(window, text="Results:")
result_label.grid(row=1, column=0, pady=(10, 5), padx=10, sticky="w")

result_text = scrolledtext.ScrolledText(window, width=30, height=8, wrap=tk.WORD)
result_text.grid(row=1, column=1, pady=(10, 5), padx=10, sticky="w")

# Start the GUI
window.mainloop()
