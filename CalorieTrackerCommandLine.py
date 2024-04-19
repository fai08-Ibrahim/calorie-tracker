## Author: Fathy Ibrahim
## Date created: 07/04/2024
## Date last changed: 14/04/2024
## This program helps users track their daily calorie consumption and provides a basic calorie calculator
## for estimating maintenance, weight loss, or weight gain goals.
## Input: 'Food Item Database.csv', Output: Daily calorie consumption 
## and recommended calorie intake based on the user’s weight and diet goals.

import csv
from tabulate import tabulate

# Constants
sDATABASE_FILE_PATH = 'Food Item Database.csv'

listItems = []

sDietType = None


def main():
    """
    Main function to run the program.
    """
    print("Welcome!")
    while True:
        showMenu()
        handleInput()

def showMenu():
    """
    Displays the menu options.
    """
    print("""Daily Calorie Consumption Calculator:
A: Display list of food items with their calories
B: Calculate my daily calorie consumption
C: Input weight and set diet goals
D: Calculate my recommended calorie intake
X: Exit""")
    print("Enter A, B, C, D or X to proceed:", end="")

def handleInput():
    """
    Takes user input and performs corresponding actions.
    """
    sRes = input().upper()
    readItems()
    if sRes == 'A':
        printItems()
    elif sRes == 'B':
        calculateConsumption()
    elif sRes == 'C':
        setDietGoals()
    elif sRes == 'D':
        calculateRecommendedCalories(sDietType)
    elif sRes == "X":
        exitApp()
    else:
        print("\nInvalid entry.\nPlease enter A, B, C, D or X.")

def readItems():
    """
    Reads food items from the database file.
    """
    with open(sDATABASE_FILE_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            listItems.append([row["Food"], row["Grams"], row["Calories"], row["Category"]])

def printItems():
    """
    Displays the list of food items with their calories.
    """
    listHeaders = ["Food", "Grams", "Calories", "Category"]
    print(tabulate(listItems, headers=listHeaders, tablefmt="grid", stralign="center"))
    returnToMenu()

def calculateConsumption():
    """
    Calculates daily calorie consumption based on user input.
    """
    listConsumedCalories = []
    while True:
        sItemName = input("Enter the name of the food item you consumed: ").lower()
        iItemCalorie, iItemWeight = findItem(sItemName)

        if iItemCalorie is None:
            print("That is not a valid food item. Please try again.")
            continue

        iGramsConsumed = getValidInput("Enter how many grams you consumed: ", "That is not a valid number. Please try again.")
        listConsumedCalories.append((iItemCalorie / iItemWeight) * iGramsConsumed)

        if not continueAdding():
            displayCalculatedConsumption(listConsumedCalories)
            returnToMenu()
            return

def findItem(sItemName):
    """
    Finds the calorie and weight information for a given food item.
    Returns a tuple containing the calorie value and weight (or None if not found).
    """
    for listItem in listItems:
        if sItemName == listItem[0].lower():
            return int(listItem[2]), int(listItem[1])
    return None, None

def getValidInput(sPrompt, sErrorMessage):
    """
    Prompts the user for input and validates that the input is a valid number.
    Returns the input as an integer if valid, otherwise prompts again.
    """
    while True:
        sUserInput = input(sPrompt)
        if sUserInput.isnumeric():
            return int(sUserInput)
        print(sErrorMessage)

def continueAdding():
    """
    Prompts the user if they want to add another item.
    Returns True if the user wants to continue, False otherwise.
    """
    while True:
        sRepeat = input("Do you want to enter a new item? (Y/N): ").upper()
        if sRepeat == 'N':
            return False
        elif sRepeat == 'Y':
            return True
        print("Invalid Entry. Please Enter Y or N")

def displayCalculatedConsumption(listConsumedCalories):
    """
    Displays total calorie consumption.
    """
    fTotalCalories = sum(listConsumedCalories)
    print(f"Total calories consumed: {fTotalCalories:.2f}")
    returnToMenu()

def setDietGoals():
    """
    Sets user's diet goals.
    """
    while True:
        sDietType = input("What are your diet goals? (standard - S, weight gains - WG, weight loss - WL):").lower()
        if sDietType in ['standard', 's', 'weightgain', 'wg', 'weightloss', 'wl']:
            break
        else:
            print("Invalid input. Please enter 'S' for standard, 'WG' for weight gains, or 'WL' for weight loss.")
    returnToMenu()

def calculateRecommendedCalories(sDietType="s"):
    """
    Calculates recommended calorie intake based on user's weight and diet goals.
    """
    sGender = input("Are you male or female? (M/F):").lower()
    iAge = int(input("How old are you?: "))
    fHeight = float(input("How tall are you? (in cm): "))
    fWeight = float(input("What's your current weight? (in kg): "))
    sActivityLevel = input("Select your activity level:\n"
                            "1. Sedentary (little or no exercise)\n"
                            "2. Lightly active (light exercise/sports 1-3 days a week)\n"
                            "3. Moderately active (moderate exercise/sports 3-5 days a week)\n"
                            "4. Very active (hard exercise/sports 6-7 days a week)\n"
                            "5. Extra active (very hard exercise/sports & physical job or training twice a day)\n"
                            "Enter the number corresponding to your activity level: ")
    
    fBMR = calculateBMR(sGender, iAge, fHeight, fWeight)
    fTDEE = calculateTDEE(fBMR, sActivityLevel)
    if sDietType == "standard" or sDietType == "s":
        print("Your diet goals are set to standard.")
    elif sDietType == "weightgain" or sDietType == "wg":
        print("Your diet goals are set to weight gain.")
        fTDEE += 500  # Increase TDEE by 500 for weight gain
    elif sDietType == "weightloss" or sDietType == "wl":
        print("Your diet goals are set to weight loss.")
        fTDEE -= 500  # Decrease TDEE by 500 for weight loss
        
    print(f"\nYour Basal Metabolic Rate (BMR) is {fBMR: .2f} calories per day.")
    print(f"Your Total Daily Energy Expenditure (TDEE) is approximately {fTDEE: .2f} calories per day.")
    returnToMenu()

def calculateBMR(sGender, iAge, fHeight, fWeight):
    """
    Calculates Basal Metabolic Rate (BMR) based on user's gender, age, height, and weight.
    """
    if sGender == "m" or sGender == "male":
        fBMR = 88.362 + (13.397 * fWeight) + (4.799 * fHeight) - (5.677 * iAge)
    else:
        fBMR = 447.593 + (9.247 * fWeight) + (3.098 * fHeight) - (4.330 * iAge)
    return fBMR

def calculateTDEE(fBMR, activity_level):
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
    return fBMR * activity_factors.get(activity_level, 1.2)  # Default to sedentary if invalid input

def returnToMenu():
    """
    Asks the user if they want to return to the main menu or exit the application.
    """
    while True:
        res = input("Do you want to return to the main menu? (Y/N): ").upper()
        if res == 'Y':
            main()
            return
        elif res == 'N':
            exitApp()
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

def exitApp():
    """
    Exits the application.
    """
    print("You are leaving the app. Stay healthy!")
    exit()

# Call the main function to start the program
if __name__ == '__main__':
  main() 