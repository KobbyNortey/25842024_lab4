import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# File Names
VOTERS_FILE = 'voters.json'
ELECTIONS_FILE = 'elections.json'


# Error Handling
def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def write_file(file_name, data):
    try:
        with open(file_name, 'w') as f:
            f.write(json.dumps(data))
    except Exception as e:
        print(f"Error writing to {file_name}: {e}")


# Registering a student as a voter
@app.route('/register_voter', methods=['POST'])
def register_voter():
    record = json.loads(request.data)
    voters_data = read_file(VOTERS_FILE)
    if not voters_data:
        records = [record]
    else:
        records = json.loads(voters_data)
        for r in records:
            if r['id'] == record['id']:
                return jsonify({"error": "Voter already exists"})
        records.append(record)
    write_file(VOTERS_FILE, records)
    return jsonify(record)


# De-registering a Student as a Voter
@app.route('/voter/<id>', methods=['DELETE'])
def deregister_voter(id):
    voters_data = read_file(VOTERS_FILE)
    if voters_data:
        records = json.loads(voters_data)
        for r in records:
            if r['id'] == int(id):
                records.remove(r)
                write_file(VOTERS_FILE, records)
                return jsonify(r)
    return jsonify({"error": "student not found"}), 404


# Updating a voter
@app.route('/update_voter/<id>', methods=['PUT'])
def update_voter(id):
    if not request.data:
        return jsonify({"error": "no data has been entered"})
    voters_data = read_file(VOTERS_FILE)
    if voters_data:
        records = json.loads(voters_data)
        for r in records:
            if r["id"] == int(id):
                r["name"] = request.json.get("name", r["name"])
                r["age"] = request.json.get("age", r["age"])
                r["major"] = request.json.get("major", r["major"])
                r["class"] = request.json.get("class", r["class"])
                write_file(VOTERS_FILE, records)
                return jsonify(r)
    return jsonify({"error": "student not found"}), 404


# Retrieving a registered voter
@app.route('/retrieve-voter/', methods=['GET'])
def retrieve_voter():
    student_id = request.args.get('id')
    if not student_id:
        return jsonify({"error": "student ID not provided"}), 400
    voters_data = read_file(VOTERS_FILE)
    if voters_data:
        records = json.loads(voters_data)
        for r in records:
            if r['id'] == int(student_id):
                return jsonify(r)
    return jsonify({"error": "student not found"}), 404


# Creating an Election
@app.route('/create_election', methods=['POST'])
def create_election():
    record = json.loads(request.data)
    elections_data = read_file(ELECTIONS_FILE)
    if not elections_data:
        records = [record]
    else:
        records = json.loads(elections_data)
        for r in records:
            if r['electionID'] == record['electionID']:
                return jsonify({"error": "Election already exists"})
        records.append(record)
    write_file(ELECTIONS_FILE, records)
    return jsonify(record)


# Retrieving an Election
@app.route('/retrieve_election/<id>', methods=['GET'])
def retrieve_election(id):
    elections_data = read_file(ELECTIONS_FILE)
    if elections_data:
        records = json.loads(elections_data)
        for r in records:
            if r['electionID'] == id:
                return jsonify(r)
    return jsonify({"error": "Election not found"}), 404


# Deleting an Election
@app.route('/delete_election/<id>', methods=['DELETE'])
def delete_election(id):
    elections_data = read_file(ELECTIONS_FILE)
    if elections_data:
        records = json.loads(elections_data)
        for r in records:
            if r['electionID'] == id:
                records.remove(r)
                write_file(ELECTIONS_FILE, records)
                return jsonify(r)
    return jsonify({"error": "election not found"}), 404


# Voting in an Election
@app.route('/election/<electionid>/<candidateid>', methods=['PATCH'])
def vote_election(electionid, candidateid):
    elections_data = read_file(ELECTIONS_FILE)
    if elections_data:
        records = json.loads(elections_data)
        for r in records:
            if r["electionID"] == electionid:
                for candidate in r["candidates"]:
                    if candidate["candidateID"] == candidateid:
                        candidate["votesCast"] = candidate.get("votesCast", 0) + 1
                        write_file(ELECTIONS_FILE, records)
                        return jsonify(r)
                return jsonify({"error": "candidate not found"}), 404
    return jsonify({"error": "election not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
