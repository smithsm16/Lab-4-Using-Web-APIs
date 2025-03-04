import requests

base_api_url = "https://opentdb.com/api.php"
categories_url = "https://opentdb.com/api_category.php"

#get list of categories from api
def get_categories():
    result = requests.get(categories_url)
    if result.status_code == 200:
        #return list of categories
        return result.json().get('trivia_categories', [])
    #if request fails, return empty list
    return []

#prompt user for desired amount of questions
def get_num_questions():
    while True:
        try: 
            #prompt user
            num_questions = int(input("How many questions would you like in your set (1-50): "))
            if num_questions > 0:
                #return desired number of questions
                return num_questions
            elif num_questions > 50:
                #number too high
                print("Please choose a number between 1 and 50.")
            else:
                #number too low
                print("Please enter a positive non-zero number.")
        except ValueError:
            #invalid input
            print("Invalid input, please enter a valid number!")

#prompt user for category
def get_category(categories):
    while True:
        print("Here are the available categories:")
        #display categories
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category['name']}")
        try:
            #prompt user
            category_choice = int(input("Enter the number of the category you'd like to choose: "))
            if 0 <= category_choice < len(categories):
                return categories[category_choice]['id']
            else:
                #invalid number
                print("Invalid choice, please try again.")
        except ValueError:
            #invalid input
            print("Invalid input, please select a number from the list!")


