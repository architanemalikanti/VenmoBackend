import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here

#ROUTE #1: Get all users 
@app.route("/api/users/", methods = ["GET"])
def get_all_users():
    all_users = DB.get_all_users()
    if all_users is None:
        return json.dumps({"error": "Users not found!"}), 400
    
    return json.dumps(all_users), 200
    

#ROUTE #2: Create a user
@app.route("/api/users/", methods = ["POST"])
def create_users():
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance")
    user_id = DB.insert_task_table(name, username, balance)
    #response is to return a user. 
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User not found!"}), 400
    
    return json.dumps(user), 201


#ROUTE #3: Get a specific user 
@app.route("/api/user/<int:user_id>/", methods=["GET"])
def get_specific_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error: Task not found"})

    return json.dumps(user), 202



#ROUTE #4: Delete a specific user
@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_task(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error: Task not found"})
    
    DB.delete_user_by_id(user_id)
    return json.dumps(user), 202


#ROUTE #5: Send money from one user to another
@app.route("/api/send/", methods=["POST"])
def send_money():
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    reciever_id = body.get("reciever_id")
    amount = body.get("amount")

    Reciever = DB.get_user_by_id(reciever_id)
    Sender = DB.get_user_by_id(sender_id)
    
    #validate users and their balances:
    if Sender is None:
        return json.dumps({"error: Sender not found"}), 404
    if Reciever is None:
        return json.dumps({"error: Reciever not found"}), 404
    
    #extract balances from the sender
    sender_balance = Sender["balance"]

    #check if the sender has enough balance to send 
    if sender_balance < amount:
        return json.dumps({"You don't have enough money loser"}), 400
    
    #process the transaction:
    Sender["balance"] = Sender["balance"] - amount
    Reciever["balance"] = Reciever["balance"] + amount

    #update the user's balance:
    DB.update_user_balance(reciever_id, Reciever["balance"])
    DB.update_user_balance(sender_id, Sender["balance"])

    #return a successful JSON response:
    return json.dumps({"Transaction Succesful!"}), 200



    








if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
