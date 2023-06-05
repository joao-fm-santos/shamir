from datetime import datetime, timedelta
import os

from flask import Flask, request

from shamir.api.encryption import cipher, create_hash
from shamir.api.helpers import validate
from shamir.generator.id import get_id

# Initialize flask
datastore = {}
app = Flask("shamir")
salt = os.urandom(16)

# Routing 
@app.route("/create", methods=["POST"])
def create():
    content  = request.get_json(force=True)

    invalid_content, invalid_message = validate("Missing \'secret\' field from request!", content)
    if invalid_content:
        return invalid_message 

    content['id'] = get_id()
    content['expiration'] = content.get('expiration', datetime.now() + timedelta(minutes=15))
    content['salt'] = salt

    # Create a sha256 hash of the secret id 
    content['sha'] = create_hash(content['id'])

    # Encrypt the message
    content['encrypted'] = cipher(content, salt)

    # Insert into redis
    datastore[content['id']] = f"{content['sha']}\n{content['encrypted']}\n{content['expiration']}"
    return {"status": "Sucess", "id": content['id']}


@app.route("/get/<id>")
def get(id):
    data = datastore.get(id, None)
    if not data:
        return {
            "status": "Failed",
            "message": "The secret either no longer exists, never existed or was already read."
        }, 400

    # If stored hash does not exist, it wont match the generated one
    # And this will mean that the secret no longer exist, or 
    # that it was never created
    stored_sha, stored_ciphertext, stored_expiration = data.split("\n")
    sha = create_hash(id)
    if stored_sha != sha:
        return {
            "status": "Failed",
            "message": "This secret either no longer exists or it was already read",
        }, 400

    # Check if secret has expired 
    if datetime.now() > datetime.strptime(stored_expiration, '%Y-%m-%d %H:%M:%S.%f'):
        return {
            "status": "Failed",
            "message": "The secret has expired",
        }, 400

    # After we fetch this value, just delete it 
    del datastore[id]

    # And decrypt the value and return
    new_content = {
        "id": id,
        "secret": stored_ciphertext
    }
    decrypted = cipher(new_content, salt, mode="decrypt")
    return {"success": "True", "message": decrypted}
