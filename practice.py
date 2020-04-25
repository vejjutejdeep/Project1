# from flask import Flask


# app = Flask(__name__)

# @app.route("/")
# def index():
#     return "hello welcome to the site."
first_list = [1, 2, 2, 5]
second_list = [2, 5, 7, 9]
third_list = [2, 3, 4, 5]

resulting_list = first_list + second_list + third_list

# resulting_list = list(first_list)
# resulting_list.extend(x for x in second_list if x not in resulting_list)
print(list(set(resulting_list)))