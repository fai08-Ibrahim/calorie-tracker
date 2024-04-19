## Author: Fathy Ibrahim
## Date created: 07/04/2024
## Date last changed: 14/04/2024
## This program uses a user-frienly GUI to help users
## track their daily calorie consumption and provides a basic calorie
## calculator for estimating maintenance, weight loss, or weight gain goals.
## Input: 'Food Item Database.csv', Output: Daily calorie consumption 
## and recommended calorie intake based on the user’s weight and diet goals.

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv

class CalorieTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stage 2 - Calorie Tracker")
        self.root.geometry("850x400")
        self.root.configure(bg='lightgray')

        # Read food items from CSV
        self.food_items = self.read_food_items()

        # Essential Variables used by the Calorie Calculator
        self.selected_diet = None
        self.sGender = None
        self.iAge = None
        self.fHeight = None
        self.fWeight = None
        self.iActivityLevel = None
        self.fBMR = None
        self.total_calories = None

        self.selections = {}
        
        # Menu
        self.menu_frame = tk.Frame(root, bg='lightgray')
        self.menu_frame.pack(pady=10)

        self.label_menu = tk.Label(self.menu_frame, text="Available Food Items:", font=("Arial", 12, "bold"), bg='lightgray')
        self.label_menu.grid(row=0, column=0, padx=5)

        # Create a scrollable listbox to display food items
        self.scrollbar = tk.Scrollbar(self.menu_frame, orient="vertical")
        self.food_listbox = tk.Listbox(self.menu_frame, yscrollcommand=self.scrollbar.set, bg='lightgray', selectmode="single", height=5)
        self.scrollbar.config(command=self.food_listbox.yview)
        self.food_listbox.grid(row=1, column=0, padx=5, pady=5)
        self.food_listbox.config(width=40, height=15)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        # Hide the listbox & scrollbar initially
        self.food_listbox.grid_remove()
        self.scrollbar.grid_remove()

        self.btn_display_items = tk.Button(self.menu_frame, text="Display Food Items", command=self.display_items, bg="#87CEFA")
        self.btn_display_items.grid(row=0, column=1, padx=5)
        
        self.btn_calc_consumption = tk.Button(self.menu_frame, text="Calculate Calorie Consumption", command=self.displayTotalCalories, bg="#87CEFA")
        self.btn_calc_consumption.grid(row=0, column=2, padx=5)
        
        self.btn_set_diet_goals = tk.Button(self.menu_frame, text="Set Diet Goals", command=self.set_diet_goals_popup, bg="#87CEFA")
        self.btn_set_diet_goals.grid(row=0, column=3, padx=5)
        
        self.btn_calc_recommended_calories = tk.Button(self.menu_frame, text="Calculate Recommended Calories", command=self.calc_recommended_calories, bg="#87CEFA", state="disabled")
        self.btn_calc_recommended_calories.grid(row=0, column=4, padx=5)
        
        self.btn_exit = tk.Button(self.menu_frame, text="Exit", command=self.root.quit, bg="#87CEFA")
        self.btn_exit.grid(row=0, column=5, padx=5)


    def read_food_items(self):
        food_items = []
        with open('Food Item Database.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, skipinitialspace=True)
            for row in reader:
                # From the database, I'm only displaying food items (on first column)
                food_items.append((row[0], row[1], row[2], row[3]))  
        return food_items
    
    def display_items(self):
        self.food_listbox.delete(0, tk.END)

        # Insert food items into the listbox
        for item in self.food_items:
            self.food_listbox.insert(tk.END, item[0] + ' - ' + item[3])

        self.food_listbox.grid()
        self.scrollbar.grid()

        # Enable selection of multiple items
        self.food_listbox.configure(selectmode="multiple")

        # Button to save selections
        save_button = tk.Button(self.menu_frame, text="Save Selections", command=self.save_selections)
        save_button.grid(row=2, column=0, padx=5, pady=5)
        # change the command to remove the listbox on 2nd click
        self.btn_display_items.config(command=lambda: self.hide_items(save_button))

    def hide_items(self, save_button):
        # Hide the listbox and scrollbar
        self.food_listbox.grid_remove()
        self.scrollbar.grid_remove()
        save_button.grid_remove()

        # Update the command of the "Display Food Items" button
        self.btn_display_items.config(command=self.display_items)

    def save_selections(self):
        # Get selected items and their indexes
        selected_indexes = self.food_listbox.curselection()
        selected_items = [self.food_items[index][0] for index in selected_indexes]

        # Prompt the user to input grams consumed for each selected item
        grams_consumed = {}
        for index, item in zip(selected_indexes, selected_items):
            grams = simpledialog.askfloat("Grams Consumed", f"How many grams of {item} did you consume?")
            if grams == None:
                grams = 0
            grams_consumed[index] = grams

        self.save_to_database(selected_indexes, grams_consumed)

    def save_to_database(self, selected_indexes, grams_consumed):
        # Add selected items and grams consumed to the dictionary
        for index, grams in zip(selected_indexes, grams_consumed):
            item_name = self.food_items[int(index)][0]
            self.selections[item_name] = grams
        self.calc_consumption(grams_consumed)

    def calc_consumption(self, grams_consumed):
        """Calculate total daily calories from saved selections."""
        self.total_calories = 0
        for index, grams in grams_consumed.items():
            foodItemStandardWeight = int(self.food_items[int(index)][2].replace(',', ''))
            foodItemCaloriesForStandardWeight = int(self.food_items[int(index)][1].replace(',', ''))
            grams_per_calorie = foodItemStandardWeight / foodItemCaloriesForStandardWeight
            calories_consumed = grams * grams_per_calorie
            self.total_calories += calories_consumed

    def displayTotalCalories(self):
        # Create a label to display the calculated total daily calories
        self.total_calories_label = tk.Label(self.menu_frame, text=f"Total Daily Calories: {self.total_calories:.2f}", bg="lightgray", font=("Arial", 10, "bold"))
        self.total_calories_label.grid(row=2, column=2, padx=5)

 
    def set_diet_goals_popup(self):
      # Create a new top-level window for the dialog box
      dialog_window = tk.Toplevel(self.root)
      dialog_window.title("Set Diet Goals")
      dialog_window.geometry("300x150") 

      prompt_label = tk.Label(dialog_window, text="Please select one of the three options below:")
      prompt_label.pack()

      # Create three check buttons for the diet goal options
      selected_diet = tk.StringVar()
      options = ["Standard", "Weight Gain", "Weight Loss"]
      for option in options:
          tk.Checkbutton(dialog_window, text=option, variable=selected_diet, onvalue=option, offvalue="").pack(anchor="w")

      # Add a button to confirm the selection
      confirm_button = tk.Button(dialog_window, text="OK", command=dialog_window.destroy)
      confirm_button.pack()

      dialog_window.wait_window()
      selected_diet = selected_diet.get()
      if selected_diet:
          self.selected_diet = selected_diet
          messagebox.showinfo("Diet Goals", f"Selected Diet Goals: {selected_diet}")
          self.toggle_calculate_button("normal")


    def toggle_calculate_button(self, state):
      self.btn_calc_recommended_calories.config(state=state)

    def calc_recommended_calories(self):
      # Create a new top-level window for the dialog box
      dialog_window = tk.Toplevel(self.root)
      dialog_window.title("Calculate Recommended Calories")
      dialog_window.geometry("430x250")

      # Labels and entry fields for user input
      tk.Label(dialog_window, text="Gender (M/F):").grid(row=0, column=0, sticky="w")
      self.gender_entry = tk.Entry(dialog_window)
      self.gender_entry.grid(row=0, column=1)

      tk.Label(dialog_window, text="Age:").grid(row=1, column=0, sticky="w")
      self.age_entry = tk.Entry(dialog_window)
      self.age_entry.grid(row=1, column=1)

      tk.Label(dialog_window, text="Height (in cm):").grid(row=2, column=0, sticky="w")
      self.height_entry = tk.Entry(dialog_window)
      self.height_entry.grid(row=2, column=1)

      tk.Label(dialog_window, text="Weight (in kg):").grid(row=3, column=0, sticky="w")
      self.weight_entry = tk.Entry(dialog_window)
      self.weight_entry.grid(row=3, column=1)

    # Activity level entry & Label explaining activity levels
      activity_description = "1: Sedentary, 2: Lightly active, 3: Moderately active, 4: Very active, 5: Extra active"
      tk.Label(dialog_window, text="Activity Level (1-5):").grid(row=4, column=0, sticky="w")
      self.activity_entry = tk.Entry(dialog_window)
      self.activity_entry.grid(row=4, column=1)
      activity_description_label = tk.Label(dialog_window, text=activity_description)
      activity_description_label.grid(row=5, column=0, columnspan=2, sticky="w")

      # Button to trigger the calculation
      calculate_button = tk.Button(dialog_window, text="Calculate", command=self.calculate_calories)
      calculate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

      # Function to close the dialog window
      def close_dialog():
          dialog_window.destroy()

      # Button to close the dialog window
      close_button = tk.Button(dialog_window, text="Close", command=close_dialog)
      close_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    
      # Function to calculate recommended calories
    def calculate_calories(self):
      self.sGender = self.gender_entry.get()
      self.iAge = int(self.age_entry.get())
      self.fHeight = float(self.height_entry.get())
      self.fWeight = float(self.weight_entry.get())
      self.iActivityLevel = int(self.activity_entry.get())
      self.fBMR = self.calculateBMR()
      self.displayRecommendedCalories()
      
      
    def calculateBMR(self):
        """
        Calculates Basal Metabolic Rate (BMR) based on user's gender, age, height, and weight.
        """
        if self.sGender.lower() == "m":
            self.fBMR = 88.362 + (13.397 * self.fWeight) + (4.799 * self.fHeight) - (5.677 * self.iAge)
        else:
            self.fBMR = 447.593 + (9.247 * self.fWeight) + (3.098 * self.fHeight) - (4.330 * self.iAge)
        return self.fBMR

    def calculateTDEE(self):
      """
      Calculates Total Daily Energy Expenditure (TDEE) based on BMR and activity level.
      """
      activity_factors = {
          "1": 1.2,  # Sedentary
          "2": 1.375,  # Lightly active
          "3": 1.55,  # Moderately active
          "4": 1.725,  # Very active
          "5": 1.9  # Extra active
        }
      return self.fBMR * activity_factors.get(str(self.iActivityLevel))


    def displayRecommendedCalories(self):
      """
      Display the recommended calorie intake on the root window.
      """
      tdee = self.calculateTDEE()
      # Create a new label to display the recommended calorie intake
      self.calories_label = tk.Label(self.menu_frame, text=f"Recommended Calories: {tdee:.2f}", bg="lightgray", font=("Arial", 10, "bold"))
      self.calories_label.grid(row=3, column=4, padx=5)


def main():
    root = tk.Tk()
    app = CalorieTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()