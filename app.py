import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
import os
import struct
import copy
import math

import loans


loans_list = []

def nada():
    return None


def save_as():
    global loans_list
    file_path = filedialog.asksaveasfilename(defaultextension=".lpfs", filetypes=[("Loan Planner Files", "*.lpfs")])
    if file_path:
        try:
            with open(file_path, 'wb') as file:
                file.write(struct.pack("B", len(loans_list)))

                for loan in loans_list:
                   file.write(struct.pack("ffHHfH??", loan.principal_init, loan.rate, loan.term, loan.frequency, loan.start_year, loan.defered, loan.compounding, loan.roll_in))
                loans_list.clear()
        except Exception as e:
            print(f"An error has occured: {e}")


def openf():
    global loans_list
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Loan Planner Files", "*.lpfs")])
    if file_path:
        try:
            with open(file_path, "rb") as file:
                loans_list.clear()
                num_loans = struct.unpack("B", file.read(1))[0]
                for i in range(num_loans):
                    data = struct.unpack("ffHHfH??", file.read(20))
                    loans_list.append(loans.loans(data[0], data[1], data[2], data[6], data[3], data[4], data[5], data[7]))
        except Exception as e:
            print(f"An error has occured: {e}")
        for loan in loans_list:
            loan.accrue_lifetime()


def add_loan():
    global loans_list
    window = tk.Tk()
    window.title("Loan Creator")

    #The Header of the Window 
    header = tk.Text(window, height=1, width=20)
    header.insert("1.0", "Loan Creator")
    header.tag_configure("center", justify="center")
    header.tag_add("center", "1.0", "end")
    header.configure(state=tk.DISABLED)
    header.pack()

    #Create all rows in form for easier formatting
    row1 = tk.Frame(window)
    row2 = tk.Frame(window)
    row3 = tk.Frame(window)
    row4 = tk.Frame(window)
    row5 = tk.Frame(window)

    row1.pack(pady=(20, 10))
    row2.pack(pady=10)
    row3.pack(pady=10)
    row4.pack(pady=10)
    row5.pack(pady=10)

    #First Row of Form
    p_label = tk.Label(row1, text="Enter the principal:")
    principal = tk.Entry(row1)

    r_label = tk.Label(row1, text="Enter rate decimal(10% => .1):")
    rate = tk.Entry(row1)

    p_label.pack(side="left", padx=(10, 0))
    principal.pack(side="left", padx=(0, 5))
    r_label.pack(side="left", padx=(5, 0))
    rate.pack(side="left", padx=(0, 10))

    #Second Row of Form
    t_label = tk.Label(row2, text="Enter the term in years:")
    term = tk.Entry(row2)

    c_label = tk.Label(row2, text="Compounding or Simple:")
    c_options = ["Compounding", "Simple"]
    c_output = tk.StringVar(window)
    c_output.set(c_options[0])
    c_menu = tk.OptionMenu(row2, c_output, *c_options)

    t_label.pack(side="left", padx=(10, 0))
    term.pack(side="left", padx=(0, 5))
    c_label.pack(side="left", padx=(5, 0))
    c_menu.pack(side="left", padx=(0, 10))
    
    #Third Row of Form
    roll_label = tk.Label(row3, text="If simple interest, roll in?:")
    roll_options = ["No", "Yes"]
    roll_output = tk.StringVar(window)
    roll_output.set(roll_options[0])
    roll_menu = tk.OptionMenu(row3, roll_output, *roll_options)
    
    f_label = tk.Label(row3, text="Enter how many times a year interest accrues:")
    frequency = tk.Entry(row3)

    roll_label.pack(side="left", padx=(10, 0))
    roll_menu.pack(side="left", padx=(0, 5))
    f_label.pack(side="left", padx=(5, 0))
    frequency.pack(side="left", padx=(0, 10))

    #4th Row of Form
    y_label = tk.Label(row4, text="Enter start year:")    
    year = tk.Entry(row4)
    m_label = tk.Label(row4, text="Select start month:")
    m_options = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    m_output = tk.StringVar(window)
    m_output.set(m_options[0])
    m_menu = tk.OptionMenu(row4, m_output, *m_options)

    y_label.pack(side="left", padx=(10, 0))
    year.pack(side="left", padx=(0, 5))
    m_label.pack(side="left", padx=(5, 0))
    m_menu.pack(side="left", padx=(0, 10))

    #Final Row of Form
    d_label = tk.Label(row5, text="For how many months will this loan be defered?:")
    deferment = tk.Entry(row5)

    d_label.pack(side="left", padx=(10, 0))
    deferment.pack(side="left", padx=(0, 10))


    #method for creating loan from user input
    def create_loan():
        if len(loans_list) < 14:
            _principal = float(principal.get())
            _rate = float(rate.get())
            _term = int(term.get())
            _compounding = c_output.get()
            if _compounding == "Compounding":
                _compounding = True
            else:
                _compounding = False
            
            _frequency = int(frequency.get())
            month_dict = {"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "July": 6, "Aug": 7, "Sept": 8, "Oct": 9, "Nov": 10, "Dec": 11}
            _start_year = float(year.get()) + (month_dict[m_output.get()] / 12)

            _defered = int(deferment.get())
            _roll = roll_output.get()
            if _roll == "No":
                _roll = False
            else:
                _roll = True

            loan = loans.loans(_principal, _rate, _term, _compounding, _frequency, _start_year, _defered, _roll)
            loan.accrue_lifetime()
            loans_list.append(loan)

            window.destroy()
        else:
            warning = tk.Tk()
            warning.title("Too Many Loans")

            def acknowledge_too_many():
                warning.destroy()
                window.destroy()

            warn = tk.Label(warning, text="You have created too many loans. This software can only handle 14 total loans. Remove one before adding a new one.")

            acknowledgement = tk.Button(warning, text="Acknowledge", command=acknowledge_too_many)


    #submit button
    submit = tk.Button(window, text="Create Loan", command=create_loan)
    submit.pack(pady=10)

    window.mainloop()


def manage_loans():
    global loans_list
    remove_list = []
    def remove_loan(ind):
        if remove_list.count(ind) > 0:
            remove_list.remove(ind)
            buttons[ind]["text"] = "Remove"
        else:
            remove_list.append(ind)
            buttons[ind]["text"] = "Removed"
    
    def finish():
        for i in sorted(remove_list, reverse=True):
            loans_list.pop(i)
        remove_list.clear()
        window2.destroy()


    window2 = tk.Tk()
    window2.title("Loan Manager")

    #creates header of the page
    header = tk.Label(window2, text="Loan Manager")
    header.pack(pady=10)

    #create frame for the table
    table = tk.Frame(window2)
    table.pack()


    row_num = 0
    buttons = []
    for loan in loans_list:
        
        if loan.roll_in:
            roll = "Roll In"
        else:
            roll = "No Roll In"
        
        if loan.compounding:
            comp = "Compounding"
        else:
            comp = "Simple"

        if row_num < 6:
            dash = "Solid"
        else:
            dash = "Dashed"
        
        colors = ["Blue", "Green", "Red", "Cyan", "Magenta", "Yellow", "Black"]
        color = tk.Label(table, text=colors[row_num % 7])
        dashed = tk.Label(table, text=dash)
        l1 = tk.Label(table, text=loan.start_year)
        l2 = tk.Label(table, text=comp)
        l3 = tk.Label(table, text=loan.rate)
        l4 = tk.Label(table, text=loan.term)
        l5 = tk.Label(table, text=loan.frequency)
        l6 = tk.Label(table, text=loan.start_year)
        l7 = tk.Label(table, text=loan.defered)
        l8 = tk.Label(table, text=roll)

        remove = tk.Button(table, text="Remove", command=lambda current_row=row_num: remove_loan(current_row))
        
        color.grid(row=row_num, column=0)
        dashed.grid(row=row_num, column=1)
        l1.grid(row=row_num, column=2)
        l2.grid(row=row_num, column=3)
        l3.grid(row=row_num, column=4)
        l4.grid(row=row_num, column=5)
        l5.grid(row=row_num, column=6)
        l6.grid(row=row_num, column=7)
        l7.grid(row=row_num, column=8)
        l8.grid(row=row_num, column=9)
        remove.grid(row=row_num, column=10)

        buttons.append(remove)
        row_num += 1

    
    finish_b = tk.Button(window2, text="Finish", command=finish)
    finish_b.pack(pady=20)
    window2.mainloop()


def instructions():
    window = tk.Tk()
    window.title("Instructions")

    header = tk.Label(window, text="Instructions")

    par1 = tk.Label(window, text="To dd loans, navigate to  Edit>Add Loan. Enter the principal as a number only value. Enter the rate as a decimal. Enter the term as a whole number of years. Select either compounding or simple interest. If you selected simple interest and the interest will roll into the principal after the deferment period, select yes, otherwise, select no. Enter a whole number of how many times a year you will pay down your interest. Enter the start year and select the start month. Enter a whole number of months that the loan will be defered.")


def principals():
    global loans_list
    window = tk.Tk()
    window.title("Principals")

    header = tk.Label(window, text="Principals Over Time")
    header.pack()

    max_year = 0
    min_year = 4000
    for loan in loans_list:
        if loan.start_year < min_year:
            min_year = loan.start_year
        if max(loan.interest_ot.keys()) > max_year:
            max_year = max(loan.interest_ot.keys())


    fig, ax = plt.subplots()

    lines = ["b-", "g-", "r-", "c-", "m-", "y-", "k-", "b--", "g--", "r--", "c--", "m--", "y--", "k--"]
    ln = 0
    for loan in loans_list:
        x1=[]
        y1=[]
        for key in loan.principal_ot:
            x1.append(key)
            y1.append(loan.principal_ot[key]) 
        ax.plot(x1, y1, lines[ln], linewidth=2.0)
        ln += 1

    ax.set(xlim=(math.trunc(min_year), max_year + 1), xticks=np.arange(math.trunc(min_year), max_year, 2))
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    window.mainloop()


def interests():
    global loans_list
    window = tk.Tk()
    window.title("Interests")

    header = tk.Label(window, text="Interests Over Time")
    header.pack()

    max_year = 0
    min_year = 4000
    for loan in loans_list:
        if loan.start_year < min_year:
            min_year = loan.start_year
        if max(loan.interest_ot.keys()) > max_year:
            max_year = max(loan.interest_ot.keys())

    ticks = np.arange(min_year, max_year, 1)

    fig, ax = plt.subplots()

    lines = ["b-", "g-", "r-", "c-", "m-", "y-", "k-", "b--", "g--", "r--", "c--", "m--", "y--", "k--"]
    ln = 0
    for loan in loans_list:
        x1=[]
        y1=[]
        for key in loan.interest_ot:
            x1.append(key)
            y1.append(loan.interest_ot[key]) 
        ax.plot(x1, y1, lines[ln], linewidth=2.0)
        ln += 1

    ax.set(xlim=(math.trunc(min_year), max_year + 1), xticks=np.arange(math.trunc(min_year), max_year, 2))
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    window.mainloop()


#Create main window
root = tk.Tk()
root.title("Loan Planner")

#Add menu bar to access other pages
menubar = tk.Menu(root)

#Define File menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=nada)
filemenu.add_command(label="Open", command=openf)
filemenu.add_command(label="Save", command=nada)
filemenu.add_command(label="Save As", command=save_as)
filemenu.add_command(label="Close", command=nada)

#Define edit menu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Add Loan", command=add_loan)
editmenu.add_command(label="Manage Loans", command=manage_loans)

#Define Help Menu
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Instructions", command=instructions)


#Define View menu
viewmenu = tk.Menu(menubar, tearoff=0)
viewmenu.add_command(label="Principals", command=principals)
viewmenu.add_command(label="Interests", command=interests)

#add menus to menu bar as cascade elements
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="Help", menu=helpmenu)
menubar.add_cascade(label="View", menu=viewmenu)


root.config(menu=menubar)
root.mainloop()