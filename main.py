import requests
import random
import html

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
            if 0 < num_questions <= 50:
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
            if 0 < category_choice <= len(categories):
                return categories[category_choice - 1]['id']
            else:
                #invalid number
                print(f"Invalid choice, please enter a number between 1 and {len(categories)}.")
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
        question_type = input("Choose a question type: 'multiple' for multiple choice, 'boolean' for true/false, or 'mixed' for a mix of both: ").lower()
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
    
#display question numbers
def display_question_numbers(questions):
    print("\nHere are the question numbers:")
    #only display number to add some random fun
    for i, question in enumerate(questions, 1):
        print(i)

#prompt user for desired question
def get_question(num_questions):
    while True:
        try:
            #prompt user
            question_choice = int(input(f"Which question from (1-{num_questions}) would you like to answer? "))
            #valid input
            if 0 < question_choice <= num_questions:
                return question_choice - 1
            #invalid number
            else: print(f"Please select a valid question number between 1 and {num_questions}.")
        #error
        except ValueError:
            print("Invalid input, please enter a valid number!")

#display question
def display_question(question_data):
    #parse through api response and fix html in question
    question = html.unescape(question_data["question"])
    answers = question_data["incorrect_answers"] + [question_data["correct_answer"]]
    #fix html in answers
    answers = [html.unescape(answer) for answer in answers]
    #randomize answers
    random.shuffle(answers)
    #print question
    print(f"\nQuestion: {question}")
    #print answer choices
    for i, answer in enumerate(answers, 1):
        print(f"{i}. {answer}")
    return answers, question_data["correct_answer"]

#prompt user for answer
def get_answer(answers):
    while True:
        try:
            #prompt user
            answer_choice = int(input(f"Chose an answer (1-{len(answers)}): ")) - 1
            #valid input
            if 0 <= answer_choice < len(answers):
                return answer_choice
            #invalid choice
            else:
                print(f"Please select a valid answer between 1 and {len(answers)}.")
        #error
        except ValueError:
            print("Invalid input, please select a valid number!")

#display feedback
def display_feedback(user_answer, correct_answer, answers):
    #if correct
    if answers[user_answer] == correct_answer:
        print("Correct! Nice job!!")
    #if incorrect
    else:
        print(f"Incorrect, nice try! The correct answer was: {correct_answer}")

#prompt user if they would like to continue
def continue_game():
    while True:
        #prompt user
        choice = input("Would you like to Continue with another question from this set, generate a New set, or Exit the game? (Enter 'C' 'N' or 'E') ").lower()
        #valid input
        if choice in ['c', 'n', 'e']:
            return choice
        #invalid input
        else:
            print("Invalid choice. Please select either 'C', 'N', or 'E'.")

#main function
def main():
    print("Welcome to my Trivia Game!")
    #retrieve categories
    categories = get_categories()
    if not categories:
        print("Unable to retrieve categories, please try again later.")
        return
    #get category
    category = get_category(categories)
    #get desired number of questions
    num_questions = get_num_questions()
    #get difficulty
    difficulty = get_difficulty()
    #get question type
    question_type = get_question_type()
    #GET request for trivia questions
    trivia_data = get_trivia_questions(num_questions, category, difficulty, question_type)
    if trivia_data and trivia_data["response_code"] == 0:
        questions = trivia_data["results"]
        while True:
            #display question numbers
            display_question_numbers(questions)
            #prompt user for what question they would like to chose
            question_choice = get_question(num_questions)
            #display question
            answers, correct_answer = display_question(questions[question_choice])
            #prompt for answer
            user_answer = get_answer(answers)
            #display feedback
            display_feedback(user_answer, correct_answer, answers)
            #prompt user if they would like to continue
            continue_choice = continue_game()
            if continue_choice == 'c':
                #continue to chose different question in set
                continue
            elif continue_choice == 'n':
                #generate a new set (restart program)
                main()
            elif continue_choice == 'e':
                #exit
                print("Thanks for playing!")
                break
    else:
        print("Failed to retrieve questions, please try again later!")

main()
