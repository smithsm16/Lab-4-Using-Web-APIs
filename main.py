import requests

base_api_url = "https://opentdb.com/api.php"
categories_url = "https://opentdb.com/api_category.php"

def get_categories():
    result = requests.get(categories_url)
    if result.status_code == 200:
        #return list of categories
        return result.json().get('trivia_categories', [])
    #if request fails, return empty list
    return []