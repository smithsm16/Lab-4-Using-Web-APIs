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

#prompt user for difficulty_level
def get_difficulty():
    while True:
        #prompt user
        difficulty = input("Chose a difficulty (easy, medium, or hard): ").lower()
        #valid input
        if difficulty in ['easy', 'medium', 'hard']:
            return difficulty
        #invalid input
        else:
            print("Invalid difficulty. Please enter either 'easy' 'medium' or 'hard'.")

#prompt user for question type
def get_question_type():
    while True:
        #prompt user
        question_type = input("Choose a question type: 'multiple' for multiple choice,\n 'boolean' for true/false, or 'mixed' for a mix of both: ").lower()
        if question_type == 'mixed':
            #api default, return nothing
            return None
        elif question_type in ['multiple', 'boolean']:
            #return type
            return [question_type]
        else:
            #invalid input
            print("Invalid input, please enter 'multiple', 'boolean', or 'mixed'.")

#GET request to OpenTDB API based on user input
def get_trivia_questions(amount, category, difficulty, question_type):
    #parameters
    params = {
        "amount": amount,
        "category": category,
        "difficulty": difficulty
    }
    #add type if user specifies between mixed or boolean
    if question_type:
        params["type"] = question_type[0]
    #api request
    response = requests.get(base_api_url, params=params)
    #return questions
    if response.status_code == 200:
        return response.json()
    else:
        #error message
        print("Error retrieving questions.")
        return None
