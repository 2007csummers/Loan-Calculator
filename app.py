import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

import loans

loans_list = []

def nada():
    return None

def add_loan():
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


    #submit button
    submit = tk.Button(window, text="Create Loan", command=create_loan)
    submit.pack(pady=10)

    window.mainloop()

def manage_loans():

    remove_list = []
    def remove_loan(index):
        if index in remove_list:
            remove_list.remove(index)
            remove.config(text="Remove")
        else:
            remove_list.append(index)
            remove.config(text="Removed")
    
    def finish():
        for ind in remove_list:
            loans_list.pop(ind)
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
    for loan in loans_list:
        
        l1 = tk.Label(table, text=loan.start_year)
        
        if loan.compounding:
            comp = "Compounding"
        else:
            comp = "Simple"
        l2 = tk.Label(table, text=comp)
        l3 = tk.Label(table, text=loan.rate)

        remove = tk.Button(table, text="Remove", command=lambda:remove_loan(row_num))
        
        l1.grid(row=row_num, column=0)
        l2.grid(row=row_num, column=1)
        l3.grid(row=row_num, column=2)
        remove.grid(row=row_num, column=3)

    
    finish_b = tk.Button(window2, text="Finish", command=finish)
    finish_b.pack(pady=20)
    window2.mainloop()


#Create main window
root = tk.Tk()
root.title("Loan Planner")

#Add menu bar to access other pages
menubar = tk.Menu(root)

#Define File menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=nada)
filemenu.add_command(label="Open", command=nada)
filemenu.add_command(label="Save", command=nada)
filemenu.add_command(label="Save As", command=nada)
filemenu.add_command(label="Close", command=nada)

#Define edit menu
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Add Loan", command=add_loan)
editmenu.add_command(label="Manage Loans", command=manage_loans)

#Define Help Menu
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Instructions", command=nada)


#Define View menu
viewmenu = tk.Menu(menubar, tearoff=0)
viewmenu.add_command(label="Principals", command=nada)
viewmenu.add_command(label="Interests", command=nada)
viewmenu.add_command(label="totals", command=nada)

#add menus to menu bar as cascade elements
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="Help", menu=helpmenu)
menubar.add_cascade(label="View", menu=viewmenu)


root.config(menu=menubar)
root.mainloop()