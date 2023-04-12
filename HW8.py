# Your name: Lucas Szentgyorgyi
# Your student id: 85320192
# Your email: szentgl@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()
    cat_dict = {}
    cur.execute('SELECT * FROM categories')
    for row in cur:
        cat_dict[row[0]] = row[1]

    build_dict = {}
    cur.execute('SELECT * FROM buildings')
    for row in cur:
        build_dict[row[0]] = row[1]

    cur.execute('SELECT * FROM restaurants')
    temp_dict = {}
    for row in cur:
        temp_dict[row[1]] = {}
        temp_dict[row[1]]['category'] = cat_dict[row[2]]
        temp_dict[row[1]]['building'] = build_dict[row[3]]
        temp_dict[row[1]]['rating'] = row[4]
    return temp_dict
        
# load_rest_data('South_U_Restaurants.db')

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()
    cat_dict = {}
    cur.execute('SELECT * FROM categories')
    for row in cur:
        cat_dict[row[0]] = row[1]
    
    temp_dict = {}
    cur.execute('SELECT * FROM restaurants')
    for row in cur:
        if cat_dict[row[2]] not in temp_dict:
            temp_dict[cat_dict[row[2]]] = 1
        else:
            temp_dict[cat_dict[row[2]]] += 1

    plt.bar(temp_dict.keys(), temp_dict.values())
    plt.show()

    return temp_dict

# plot_rest_categories('South_U_Restaurants.db')

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()
    build_dict = {}
    cur.execute('SELECT * FROM buildings')
    for row in cur:
        build_dict[row[0]] = row[1]
    cur.execute('SELECT * FROM restaurants')
    temp_lst = []
    for row in cur:
        if build_dict[row[3]] == building_num:
            temp_lst.append((row[1],row[-1]))
    temp_lst_2 = sorted(temp_lst, key = lambda x:x[1], reverse=True)
    final_lst = []
    for i in temp_lst_2:
        final_lst.append(i[0])
    return final_lst


    
# find_rest_in_building(1140, 'South_U_Restaurants.db')


#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    dir = os.path.dirname(__file__) + os.sep
    conn = sqlite3.connect(dir + db)
    cur = conn.cursor()
    ## Restaraunts 
    cat_dict = {}
    cur.execute('SELECT * FROM categories')
    for row in cur:
        cat_dict[row[0]] = row[1]

    temp_dict = {}
    cur.execute('SELECT * FROM restaurants')
    for row in cur:
        if cat_dict[row[2]] not in temp_dict:
            temp_dict[cat_dict[row[2]]] = [row[-1]]
        else:
            temp_dict[cat_dict[row[2]]].append(row[-1])
    
    for a in temp_dict:
        temp_dict[a] = sum(temp_dict[a])/len(temp_dict[a])
    
    temp_lst = []
    for a in temp_dict:
        temp_lst.append((a,temp_dict[a]))
    final_lst = sorted(temp_lst, key = lambda x:x[1], reverse = True)
    highest_rest = (final_lst[0])

    ## Buildings
    cat_dict = {}
    cur.execute('SELECT * FROM buildings')
    for row in cur:
        cat_dict[row[0]] = row[1]

    temp_dict = {}
    cur.execute('SELECT * FROM restaurants')
    for row in cur:
        if cat_dict[row[3]] not in temp_dict:
            temp_dict[cat_dict[row[3]]] = [row[-1]]
        else:
            temp_dict[cat_dict[row[3]]].append(row[-1])
    
    # print(temp_dict)
    
    for a in temp_dict:
        temp_dict[a] = sum(temp_dict[a])/len(temp_dict[a])
    
    temp_lst = []
    for a in temp_dict:
        temp_lst.append((a,temp_dict[a]))
    final_lst = sorted(temp_lst, key = lambda x:x[1], reverse = True)
    highest_build = (final_lst[0])

    return_lst = [highest_rest, highest_build]
    return return_lst

    

    


# get_highest_rating('South_U_Restaurants.db')


#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
