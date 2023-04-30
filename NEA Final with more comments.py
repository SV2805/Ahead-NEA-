#importing all necessary libraries
from tkinter import *
import os
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from matplotlib import pyplot as plt
import easygui
import json
from tkinter import messagebox
import time

class TimerApp:
    def __init__(self, master):
        # This class creates the timer app
        self.master = master
        self.master.title("Timer")
        self.master.geometry("300x100")
        
        # Label to display the timer
        self.time_label = tk.Label(self.master, text="00:00:00", font=("Arial", 30))
        self.time_label.pack()
        
        # Buttons to start, stop, and reset the timer
        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_button.pack(side="left", padx=10)
        
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_timer, state="disabled")
        self.reset_button.pack(side="left", padx=10)
        
        # Initialize timer variables
        self.timer_running = False
        self.start_time = None
        self.remaining_time = None
        
        # Bind Enter key to start_timer function
        self.master.bind("<Return>", self.start_timer)
    
    def start_timer(self, event=None):
        # Start the timer
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.reset_button.config(state="normal")
            
            # Get the remaining time from user input
            self.remaining_time = int(self.get_remaining_time())
            self.update_timer()
            
    def update_timer(self):
        # Update the timer label and check if timer has finished
        time_string = time.strftime("%H:%M:%S", time.gmtime(self.remaining_time))
        self.time_label.config(text=time_string)
        
        if self.timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.stop_timer()
            messagebox.showinfo("Timer End","Hey, Time is up.")
    
    def stop_timer(self):
        # Stop the timer
        if self.timer_running:
            self.timer_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def reset_timer(self):
        # Reset the timer
        self.stop_timer()
        self.time_label.config(text="00:00:00")
        self.reset_button.config(state="disabled")
        
    def get_remaining_time(self):
        # Ask the user to input a time in HH:MM:SS format and return the remaining time in seconds
        time_str = tk.simpledialog.askstring("Set Timer", "Enter time in HH:MM:SS format")
        if time_str:
            try:
                hours, minutes, seconds = map(int, time_str.split(":"))
                total_seconds = hours * 3600 + minutes * 60 + seconds
                return total_seconds
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please enter a valid time in HH:MM:SS format")

class NotepadApp:
    def __init__(self, master):
        # This class creates the notepad app
        self.master = master
        self.master.title("Notepad")
        self.master.geometry("300x250")

        # Text box to enter and display text
        self.text_box = tk.Text(self.master, height=12)
        self.text_box.pack(fill="both", expand=True)

        # Button to clear the text
        self.button_frame = tk.Frame(self.master)            
        self.button_frame.pack(side="bottom")
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_text)
        self.clear_button.pack(side="right", padx=5, pady=5)

    def clear_text(self):
      # Clearing the text box
        self.text_box.delete("1.0", "end")

class MainScreen:
    def __init__(self, master):
      # This class creates the main screen 
        self.master = master
        self.master.title("Main Screen")
        self.master.geometry("500x350")
    
    def open_timer(self):
      # Opening the timer page
        self.timer_window = tk.Toplevel(self.master)
        timer_app = TimerApp(self.timer_window)
    
    def open_notepad(self):
      # Opening the notepad page
        self.notepad_window = tk.Toplevel(self.master)
        notepad_app = NotepadApp(self.notepad_window)
# Designing window for registration
class ProgressTrackerApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.create_buttons(master)
        self.tests = [] #empty array to hold the test scores
      
#creation of the buttons needed and the coding to the buttons aswell, so bascially what each button will do when pressed
    def create_buttons(self,master):
      #this button (Add Test Score) is linked to one of the key features of this particular section which allows the user to add in their test score to display on the graph
        self.add_test = tk.Button(self)
        self.add_test["text"] = "Add Test Score"
        self.add_test["command"] = self.add_test_score
        self.add_test.pack(side="top")

      #this is the creation of the button (Show Graph) that will actually let the user view the graph and it is linked to the show_line_graph subroutine.
        self.show_graph = tk.Button(self)
        self.show_graph["text"] = "Show Graph"
        self.show_graph["command"] = self.show_line_graph
        self.show_graph.pack(side="top")

      #this is creation of the button (Close Graph) that closes the graph- key thing to remember is that this button only closes the rather the whole screen 
        self.close_graph = tk.Button(self)
        self.close_graph["text"] = "Close Graph"
        self.close_graph["command"] = self.close_line_graph
        self.close_graph.pack(side="top")
        
      #this is simply a quit button that closes the whole screen and exits out.
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=master.destroy)
        
        self.quit.pack(side="bottom")

#subroutine that adds the user's test scores to the graph   
    def add_test_score(self):
      #instantiating a variable test_score this is the actaul number that will be added to the graph. Used simpledialog to create simple dialog boxes to take user input. 
        test_score = simpledialog.askinteger("Input", "Enter test score in percentage:")
      # this in short determines the x-axis value for each test score added as it determines what number test this is by checking the length of the array and increasing it by one to accommodate for the new test score being added 
        test_number = len(self.tests) + 1
        self.tests.append((test_number, test_score)) 
      #this part above simply matches the test number(x-axis value) to the score inputted by the user(y-axis value) to plot them according later  

#subroutine for presenting the graph to the user 
    def show_line_graph(self):
        x = [x for x, y in self.tests] 
        y = [y for x, y in self.tests]
      #takes the x and y values to plot on the graph from tests array 
        plt.plot(x, y, '-r')
        plt.xlabel('Test Number')
        plt.ylabel('Percentage')
        plt.title('Progress Tracker')
      #simply plots the the x and y value against each other and makes the line coloured red and adds labels to the axis as well as a graph title 
        plt.show()

#subroutine to close the graph 
    def close_line_graph(self):
        plt.close()

class HomePage:
  def home_page(self,tab1):

#timetable function was added later was getting bugs in other places so decided to leave it here R
      def timetable_show():
          root =tk.Tk()
          root.title("Timetable Program")
          days = ["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
          for i in range(8):
            label = tk.Label(root, text=days[i], padx=10, pady=5, font=("Arial", 10, "bold"))
            label.grid(row=0, column=i)

      # Create the time slots
          times = ["7am", "8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm", "12am"]
          for i in range(len(times)):
            label = tk.Label(root, text=times[i], padx=10, pady=5, font=("Arial", 10))
            label.grid(row=i+1, column=0)

    # Create the entry fields
          for i in range(1, len(times)+1):
                         for j in range(1, len(days)):
                            entry = tk.Entry(root, font=("Arial", 10), width=15)
                            entry.grid(row=i, column=j, padx=5, pady=2)
          root.mainloop()
      
      self.menu_var = tk.StringVar(tab1)
      self.menu_var.set("Select a subject")
      self.menu = tk.OptionMenu(tab1, self.menu_var, "Computer Science", "Maths", "Physics", "Timetable", command=self.show_page)
      self.menu.pack()
      def get_progress_tracker():
        progress_win = tk.Tk()
        obj = ProgressTrackerApp()
        progress_win.mainloop()
      # create buttons
      self.flashcards_button = tk.Button(tab1, text="Flashcards")
      self.progress_button = tk.Button(tab1, text="Progress Tracker",command=get_progress_tracker)
      def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

      def display_decks():
         clear_frame(tab1)
         self.get_display_decks(tab1)

      # create pages
      self.cs_page = tk.Frame(tab1, width=500, height=250, bg="dodger blue")
      self.maths_page = tk.Frame(tab1, width=500, height=250, bg="dodger blue")
      self.physics_page = tk.Frame(tab1, width=500, height=250, bg="dodger blue")
      self.timetable_page = tk.Frame(tab1, width=500, height=250, bg="dodger blue")
      def go_to_progress_tracker():
        pro_win = tk.Tk()
        obj = ProgressTrackerApp(pro_win)
        pro_win.mainloop()
      # add labels to pages
      tk.Label(self.cs_page, text="Computer Science Page", bg ="dodgerblue", padx=0, pady=0).pack()
      tk.Label(self.maths_page, text="Maths Page", bg ="dodgerblue", padx=0, pady=0).pack()
      tk.Label(self.physics_page, text="Physics Page", bg ="dodgerblue", padx=0, pady=0).pack()
      tk.Label(self.timetable_page, text="Timetable Page", bg ="dodgerblue", padx=0, pady=0).pack()
      
      # add buttons to pages
      tk.Label(self.cs_page, text="", bg ="dodgerblue").pack()
      tk.Button(self.cs_page, text="CS:Flashcards", command=display_decks, padx=5, pady=5, width=25, height=2).pack()
      tk.Label(self.cs_page, text="", bg ="dodgerblue").pack()
      tk.Label(self.cs_page, text="", bg ="dodgerblue").pack()
      tk.Button(self.cs_page, text="CS:Progress Tracker", command=go_to_progress_tracker, padx=5, pady=5, width=25, height=2).pack()
      
      tk.Label(self.maths_page, text="", bg ="dodgerblue").pack()      
      tk.Button(self.maths_page, text="MA:Flashcards", command=display_decks, padx=5, pady=5,width=25, height=2).pack()
      tk.Label(self.maths_page, text="", bg ="dodgerblue").pack()
      tk.Label(self.maths_page, text="", bg ="dodgerblue").pack()
      tk.Button(self.maths_page, text="MA:Progress Tracker", command=go_to_progress_tracker, padx=5, pady=5, width=25, height=2).pack()
      
      tk.Label(self.physics_page, text="", bg ="dodgerblue").pack()       
      tk.Button(self.physics_page, text="PH:Flashcards",command=display_decks, padx=5, pady=5, width=25, height=2).pack()
      tk.Label(self.physics_page, text="", bg ="dodgerblue").pack()
      tk.Label(self.physics_page, text="", bg ="dodgerblue").pack()
      tk.Button(self.physics_page, text="PH:Progress Tracker",command=go_to_progress_tracker, padx=5, pady=5, width=25, height=2).pack()

      tk.Button(self.timetable_page, text="Timetable", command=timetable_show, padx=5, pady=5, width=25, height=2).pack()


      #---------------------x-----------------
      self.timer_,self.notepad_ = self.notepad_and_timer(tab1)

      def back():
        for widget in tab1.winfo_children():
          widget.destroy()
        self.home_page(tab1)

      tk.Button(tab1, text="Back", command=back, padx=5, pady=5,width=10, font=("",10,"bold")).place(x=190,y=275)
      tk.Button(tab1, text="Timer", command=self.timer_, padx=5, pady=5,width=10, font=("",10,"bold")).place(x=290,y=275)
      tk.Button(tab1, text="Notepad", command=self.notepad_, padx=5, pady=5,width=10, font=("",10,"bold")).place(x=390,y=275)

  def __init__(self, master):
    self.master = master
    master.title("Home Page")
    master.geometry("500x300")
    master.configure(bg ="dodgerblue")
    self.root_deck_path = os.path.join(os.path.dirname(__file__),"Decks")
    notebook = ttk.Notebook(master)
    notebook.pack(fill='both', expand=True)

    # Create the first tab
    style= ttk.Style()
    style.configure('TFrame', background='dodgerblue')
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text='Home')
    label1 = ttk.Label(tab1, text='Home',background='dodgerblue',font=("",14,"bold"))
    label1.pack(padx=10, pady=10)
    self.home_page(tab1)

  def notepad_and_timer(self,frame):
      # Create an instance of the MainScreen class
      timer_notepad = MainScreen(self.master)
      # Get the timer and notepad from the MainScreen instance
      timer = timer_notepad.open_timer
      notepad = timer_notepad.open_notepad
      # Return the timer and notepad
      return timer,notepad
  
  def show_page(self, selected):
      # Hide all pages
      self.cs_page.pack_forget()
      self.maths_page.pack_forget()
      self.physics_page.pack_forget()
      self.timetable_page.pack_forget()
        
      # Show the selected page
      if selected == "Computer Science":
          self.cs_page.pack()
      elif selected == "Maths":
          self.maths_page.pack()
      elif selected == "Physics":
          self.physics_page.pack()
      else:
          self.timetable_page.pack()
  
  def get_selected_menu(self):
      # Set the window size
      self.master.geometry("800x350")
      # Print and return the selected menu
      print(self.menu_var.get())
      return self.menu_var.get()
  
  def get_flashcard(self):
      # Create a list of input labels
      input_list  = ["Question:", "Answer:"]
      # Open a dialog box to get the flashcard input
      flashcard = easygui.multenterbox("Enter a question and answer for flashcard","FlashCard",input_list)
      # If the user entered values, return them
      if flashcard != None:
          return flashcard
      # Otherwise, return None
      # ans = easygui.enterbox("Enter answer for flashcard")
  
  def create_deck(self):
      # Create a list of options
      options = ["Physics", "Maths","Computer Science"]
      # Get the selected deck from the menu variable
      selected_deck = self.menu_var.get()
      # Open a dialog box to get the deck name
      deck_name = easygui.enterbox("Enter deck name: ")
      # Set the new deck variable to the selected deck
      self.new_deck = selected_deck
      # Add the .json extension to the deck name
      deck_name = deck_name+".json"
      # Create the folder and file paths
      folder_path = os.path.join(self.root_deck_path,selected_deck)
      file_path = os.path.join(folder_path,deck_name)
  
      # If the file does not exist, create it
      if os.path.exists(file_path) == False:
          with open(file_path,'w') as wf:
              wf.write("")
          print(self.new_deck,deck_name)
          # Create the first flashcard for the deck
          self.create_flashcard(selected_deck,deck_name,'first')
      # Otherwise, show an error message
      else:
          messagebox.showinfo("Already Exist!","Deck already exist.")
  
def select_deck(self,frame):
    # display decks in dropdown
    folder_name = self.get_selected_menu()
    folder_path = os.path.join(self.root_deck_path,folder_name)

    # check if the root deck path exists, create it if it doesn't
    if os.path.exists(self.root_deck_path) == False:
        os.mkdir(self.root_deck_path)

    # check if the folder path exists, create it if it doesn't
    if os.path.exists(folder_path) == False:
        os.mkdir(folder_path)

    # get list of all decks in the folder
    all_decks = [i.split(".")[0] for i in os.listdir(folder_path)]

    # if no decks are found, set a default 'Add decks' option
    if all_decks == []:
        all_decks = ['Add decks']

    # create a string variable to store the selected deck name
    deck_var = tk.StringVar()

    # create a dropdown menu to display all decks
    combobox = ttk.Combobox(frame, textvariable=deck_var, width=50,state= "readonly")
    combobox['values']=all_decks
    deck_var.set(all_decks[0])
    combobox.pack()

    # return the selected deck variable
    return deck_var


def get_display_decks(self,frame):
    # clear the frame before displaying anything new
    for widget in frame.winfo_children():
        widget.destroy()

    # function to call to clear the frame and display the deck list again
    def get_display_v2():
        for widget in frame.winfo_children():
            widget.destroy()
        self.get_display_decks(frame)

    # function to go back to the home page
    def back():
        for widget in frame.winfo_children():
            widget.destroy()
        self.home_page(frame)

    # get the selected folder name
    folder_name = self.get_selected_menu()

    # display the header and the dropdown for selecting a deck
    ahead_label = tk.Label(frame,text='Ahead',font=("",16,"bold"),background='dodgerblue').place(x=20,y=10)
    front_text = f"{folder_name}: Flashcards\n"
    front_label = tk.Label(frame,text=front_text,font=("",16,"bold"),background='dodgerblue').pack()
    tk.Label(frame,text="Select Deck\n",font=("",11,"bold"),background='dodgerblue').pack()
    deck_name = self.select_deck(frame)

    # function to create a new flashcard
    def cr_fls():
        self.create_flashcard(folder_name,deck_name,None)

    # initialize variables for question and answer
    self.qs,self.ans = "",""

    # function to show the selected deck
    def show_deck():
        frame = tk.Tk()
        frame.geometry("600x300")
        frame.resizable(0,0)
        frame.configure(background='dodgerblue')

        # get the folder and deck names to display in the header
        folder_name = self.get_selected_menu()
        ahead_label = tk.Label(frame,text='Ahead\n',font=("",16,"bold"),background="dodgerblue").place(x=20,y=10)
        front_text = f"{folder_name}: Flashcards \n{deck_name.get()}"
        front_label = tk.Label(frame,text=front_text,font=("",16,"bold"),background="dodgerblue").pack()

        # create a frame for the text widget
        _frame = tk.Frame(frame)
        _frame.pack()
        
        # Create a Text widget and add it to the Frame
        text_widget = tk.Text(_frame,width=50,height=12)
        text_widget.pack()
        
        # Initialize variables
        previous_fls = []
        self.constant_vals = []
        
        # Construct the path to the deck's JSON file
        deck_path = os.path.join(os.path.join(self.root_deck_path,folder_name),deck_name.get())+'.json'
        
        # Load the data from the deck's JSON file
        with open(deck_path,'r') as rf:
            data = rf.read()
            self.load_data = json.loads(data)
            first_card = list(self.load_data[0].keys())[0]
        
            # Insert the first flash card's question into the Text widget
            text_widget.insert(tk.END, first_card)
        
        # Define a function to display the next flash card in the deck
        def next_():
            try:
                flash_card = list(self.load_data[0].items())
                self.qs,self.ans = flash_card[0][0],flash_card[0][1]
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, self.qs)
        
                # Add the current flash card to the list of previously displayed flash cards
                if self.load_data[0] not in previous_fls:
                    previous_fls.append(self.load_data[0])
        
                # Add the current flash card to the list of constant flash cards (i.e., those that will always be in the deck)
                if self.load_data[0] not in self.constant_vals:
                    self.constant_vals.append(self.load_data[0])
        
                # Remove the current flash card from the deck
                self.load_data.remove(self.load_data[0])
            except IndexError:
                # If there are no more cards in the deck, reset the deck to its original state (i.e., with only the constant cards)
                self.load_data = self.constant_vals
                pass
        
        # Define a function to flip the current flash card (i.e., display its answer)
        def flip():
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, self.ans)
        
        # Define a function to display the previous flash card in the deck
        def previous():
            try:
                # Get the previous flash card (i.e., the most recently displayed one)
                flash_card = list(previous_fls[-1].items())
                self.qs,self.ans = flash_card[0][0],flash_card[0][1]
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, self.qs)
        
                # Remove the most recently displayed flash card from the list of previous flash cards
                previous_fls.remove(previous_fls[-1])
            except IndexError:
                # If there are no previous flash cards (i.e., the current card is the first one), display a message box
                messagebox.showinfo('First Flashcard',"The card you are seeing is the first card of this deck")
      
      #creating the buttons needed for the flashcards feature 
        pre = tk.Button(frame,text='Previous',width=12,command=previous,font=("",10,"bold")).place(x=20,y=260)
        flip_ = tk.Button(frame,text='Flip',width=12,command=flip,font=("",10,"bold")).place(x=130,y=260)
        next__ = tk.Button(frame,text='Next',width=12,command=next_,font=("",10,"bold")).place(x=240,y=260)
        tk.Button(frame,text='Timer',width=12,command=self.timer_,font=("",10,"bold")).place(x=350,y=260)
        tk.Button(frame,text='Notepad',width=12,command=self.notepad_,font=("",10,"bold")).place(x=460,y=260)
        frame.mainloop()

    # timer_notepad = MainScreen(self.master)
    # timer = timer_notepad.open_timer
    # notepad = timer_notepad.open_notepad
    # tk.Button(frame, text="Timer", command=timer, padx=5, pady=5,width=10, font=("",10,"bold")).place(x=290,y=230)
    # tk.Button(frame, text="Notepad", command=notepad, padx=5, pady=5,width=10, font=("",10,"bold")).place(x=190,y=230)

  #creating the buttons to manipulate the flashcards/decks 
    create_deck = tk.Button(frame,text='Create Deck',width=30,command=self.create_deck,font=("",10,"bold")).place(x=140,y=180)
    tk.Button(frame,text='Timer',width=30,command=self.timer_,font=("",10,"bold")).place(x=140,y=140)
    tk.Button(frame,text='Notepad',width=30,command=self.notepad_,font=("",10,"bold")).place(x=430,y=140)
    create_fsc = tk.Button(frame,text='Create Flashcard',width=30,command=cr_fls,font=("",10,"bold")).place(x=430,y=180)
    edit_deck = tk.Button(frame,text='Edit Deck',width=30,command=self.edit_dec,font=("",10,"bold")).place(x=140,y=220)
    edit_fsc = tk.Button(frame,text='Edit Flashcard',width=30,command=self.edit_fsc,font=("",10,"bold")).place(x=430,y=220)
    refresh_btn = tk.Button(frame,text='Refresh',width=30,command=get_display_v2,font=("",10,"bold")).place(x=430,y=260)
    show_deck_ = tk.Button(frame,text='Show Flashcard',width=30,command=show_deck,font=("",10,"bold")).place(x=140,y=260)
    back_to_home = tk.Button(frame,text='Back To Home',width=30,command=back,font=("",10,"bold")).place(x=285,y=300)

  def create_flashcard(self,deck_var,file,_event):
    # Function to create a new flashcard and save it in the selected deck

    # Get the question and answer for the new flashcard
    fc = self.get_flashcard()

    if deck_var!=None:
      # Create a dictionary to store the flashcard
      flashcard = {}
      ques = fc[0]
      ans = fc[1]
      flashcard[ques] = ans

      folder_path = os.path.join(self.root_deck_path,deck_var)

      # If the file name is not given, prompt the user to enter one
      if type(file) != str:
        file = file.get()+".json"
      else:
        file = file+".json"

      # Replace double file extension with single file extension
      if '.json.json' in file:
         file = file.replace(".json.json",".json")

      # Create the path to the deck file
      deck_path = folder_path+"\\"+file

      # If the event is 'first', create a new deck file and add the flashcard
      if _event =='first':
        with open(deck_path,'a') as wf:
            dumps_data = json.dumps([flashcard],indent=2)
            wf.write(dumps_data)
            wf.close()

      # If the event is not 'first', open the deck file, add the new flashcard, and save the file
      if _event != 'first':
        with open(deck_path,'r') as rf:
          data = rf.read()
          load_list = json.loads(data)
          load_list.append(flashcard)

        with open(deck_path,'w') as wf2:
          dump_data = json.dumps(load_list)
          wf2.write(dump_data)

  def edit_fsc(self):
    # Function to edit the answer of a flashcard in a deck

    # Get the folder and deck names and path to the deck file
    folder_name = self.menu_var.get()
    values = ["Subject:","Deck"]
    deck_name = easygui.enterbox("Enter deck name")
    deck_name = deck_name+".json"
    folder_path = os.path.join(self.root_deck_path,folder_name)
    deck_path = os.path.join(folder_path,deck_name)

    # Prompt the user to select the flashcard question to edit and enter a new answer
    with open(deck_path,'r') as rf:
      data = rf.read()
      load_data = json.loads(data)
      all_qs = [list(i.keys())[0] for i in load_data]
      selected_qs = easygui.buttonbox("Select a flashcard question you \nwant to edit its answer:", choices=all_qs)
      new_ans = easygui.enterbox("Enter new answer")

      # Modify the flashcard in the deck with the new answer
      modified_deck_list = []
      for i in load_data:
        if selected_qs in i.keys():
            key = list(i.keys())[0]
            i[key] = new_ans
        modified_deck_list.append(i)
      
      # Save the modified deck file
      with open(deck_path,'w') as wf:
         dump_data = json.dumps(modified_deck_list)
         wf.write(dump_data)

  def edit_dec(self):
    # Function to edit multiple flashcards in a deck

    # Call edit_fsc function to edit a flashcard in the deck
    self.edit_fsc()

    # Prompt the user if they want to edit more flashcards in the deck
    ask_more = messagebox.askyesno("Edit","Would you like to edit more flashcards in the deck?")
    if ask_more=='yes':
       self.edit_fsc()
    else:
       messagebox.showinfo("Greetings!","Thank you")

 
def register():
    #creating the screen for registering 
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("500x250")
    register_screen.configure(bg ="dodgerblue")

    #creating the variables 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    #creating user input boxes for the username and password and labelling them so the user knows what box is which 
    Label(register_screen, text="Please enter details below", bg = "dodgerblue").pack()
    Label(register_screen, text="", bg = "dodgerblue").pack()
    username_label = Label(register_screen, text="Username*", bg = "dodgerblue")
    username_label.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_label = Label(register_screen, text="Password*", bg = "dodgerblue")
    password_label.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="", bg = "dodgerblue").pack()

    #when button is clicked to register it runs register_user function
    Button(register_screen, text="Register", width=10, height=1,command = register_user).pack()  
# Designing window for login 
 
def login():

    #creating the separate login screen for the user 
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("500x250")
    login_screen.configure(bg ="dodgerblue")
    Label(login_screen, text="Please enter details below to login", bg = "dodgerblue").pack()
    Label(login_screen, text="", bg = "dodgerblue").pack()

    #creating the variables 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry

    #creating boxes for the user input and labelling it clearly to let the user know what box to enter the details in
    Label(login_screen, text="Username ",  bg = "dodgerblue").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()

    #also adding chosen colour to the screen
    Label(login_screen, text="", bg = "dodgerblue").pack()
    Label(login_screen, text="Password ",  bg = "dodgerblue").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="" , bg = "dodgerblue").pack()

    #creating the button for the user to submit their input leading to the login check 
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
# Implementing event on register button
 
def register_user():
    username_info = username.get()
    password_info = password.get()
    #added check for unique usernames 
    if username_info in os.listdir():
      username_used()
      return()
    else:
      #added if statement to make sure there is something inputted into both fields
      if username_info == "":
        empty_username()
      
      elif password_info== "":
        empty_password()
    
      else:
        #creating a file to write down registering details of the user
        file = open(username_info, "w")
        file.write(username_info + "\n")
        file.write(password_info)
        file.close()
     
        username_entry.delete(0, END)
        password_entry.delete(0, END)
      
        #letting the user know thye have been registered 
        Label(register_screen, text="Registration Success", fg="green",bg = "dodgerblue", font=("calibri", 11)).pack()

#implementing uniqueness check 

def username_used():
  #destroying register screen 
  register_screen.destroy()
  #creating popup window for the error 
  global username_used_screen
  username_used_screen = Toplevel(main_screen)
  username_used_screen.configure(bg = "dodgerblue")
  username_used_screen.title("Error")
  username_used_screen.geometry("350x100")
  Label(username_used_screen, text="Username already in use, please choose a new one.", bg = "dodgerblue").pack()
  #added OK button to close the popup 
  Button(username_used_screen, text="OK", command=delete_username_used_screen).pack()
  
def delete_username_used_screen():
  username_used_screen.destroy()
  
#Implementing presence check for username 

def empty_username():
  global empty_username_screen
  empty_username_screen = Toplevel(register_screen)
  empty_username_screen.configure(bg = "dodgerblue")
  empty_username_screen.title("Error")
  empty_username_screen.geometry("250x100")
  Label(empty_username_screen, text="Please enter an username.", bg = "dodgerblue").pack()
  Button(empty_username_screen, text="OK", command=delete_empty_username_screen).pack()

def delete_empty_username_screen():
    empty_username_screen.destroy()

#Implementing presence check for username 
def empty_password():
  global empty_password_screen
  empty_password_screen = Toplevel(register_screen)
  empty_password_screen.configure(bg ="dodgerblue")
  empty_password_screen.title("Error")
  empty_password_screen.geometry("250x100")
  Label(empty_password_screen, text="Please enter a password.", bg = "dodgerblue").pack()
  Button(empty_password_screen, text="OK", 
command=delete_empty_password_screen).pack()

def delete_empty_password_screen():
  empty_password_screen.destroy()
# Implementing event on login button 
 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
 
    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
 
        else:
            password_not_recognised()
 
    else:
        user_not_found()
 
# Designing popup for login success
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(main_screen)
    login_success_screen.title("Success")
    login_success_screen.configure(bg ="dodgerblue")
    login_success_screen.geometry("250x150")
    Label(login_success_screen, text="Login Success", bg = "dodgerblue").pack()

    def go_to_home():
       main_screen.destroy()
       home_win = Tk()
       obj = HomePage(home_win)
       home_win.mainloop()
    Button(login_success_screen, text="Homepage", command=go_to_home).pack()
 
# Designing popup for login invalid password
 
def password_not_recognised():
  #creating screen for popup to notify wrong password
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.configure(bg ="dodgerblue")
    password_not_recog_screen.geometry("250x150")
    Label(password_not_recog_screen, text="Invalid Password ", bg = "dodgerblue").pack()
  #ok button to close the notification 
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.configure(bg ="dodgerblue")
    user_not_found_screen.geometry("250x150")
    Label(user_not_found_screen, text="User Not Found", bg = "dodgerblue").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success():
    login_success_screen.destroy()
 
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy() 
 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    #creating the size I want for the screen and the screen itself 
    main_screen = Tk()
    main_screen.geometry("500x250")
    main_screen.title("AHEAD")
    #choosing what text to say + adding colours to the background
    Label(text="Welcome to Ahead", bg= "dodgerblue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="", bg= "dodgerblue").pack() 
    #creating the login and registering buttons 
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="", bg= "dodgerblue").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
    main_screen.configure(bg ="dodgerblue")
    main_screen.mainloop()
 
main_account_screen()