from flask import Flask, render_template, request
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://crob0008:GYfLnhxdJgeiOTPO@chefsbhojan.oxsu9gm.mongodb.net/',
    connectTimeoutMS=30000, 
    socketTimeoutMS=None)
db = client['FORMDATACOLLECTION']
Details = db['CONTACTS']

@app.route('/', methods=['GET', 'POST'])
def get_contacts():
    query = request.form.get('query', '')
    search_filter = {}

    if query:
        search_filter = {
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'phone': {'$regex': query, '$options': 'i'}}
            ]
        }

    contacts = list(Details.find(search_filter, {'_id': 0, 'name': 1, 'phone': 1, 'date_created': 1}))
    return render_template('contacts.html', contacts=contacts, query=query)

if __name__ == '__main__':
    app.run(debug=True)