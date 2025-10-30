from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory mock database (for demo)
users = {
    "karthik": {
        "workouts": [],
        "calories": 0,
        "goals": {"daily_steps": 10000, "calories_burn": 500}
    }
}

@app.route('/')
def home():
    return jsonify({
        "message": "?????? Fitness Tracker API is running successfully!",
        "status": "active",
        "author": "Karthik Teja"
    })

@app.route('/add_workout', methods=['POST'])
def add_workout():
    data = request.get_json()
    username = data.get('username', 'karthik')
    workout = data.get('workout')
    calories = data.get('calories', 0)

    if not workout:
        return jsonify({"error": "Workout type required"}), 400

    user = users.get(username)
    if not user:
        users[username] = {"workouts": [], "calories": 0, "goals": {}}
        user = users[username]

    user['workouts'].append(workout)
    user['calories'] += calories

    return jsonify({
        "message": "Workout added successfully!",
        "workouts": user['workouts'],
        "total_calories": user['calories']
    }), 201

@app.route('/get_stats/<username>', methods=['GET'])
def get_stats(username):
    user = users.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": username,
        "workouts": user['workouts'],
        "total_calories": user['calories'],
        "goals": user['goals']
    })

@app.route('/update_goals', methods=['POST'])
def update_goals():
    data = request.get_json()
    username = data.get('username', 'karthik')
    goals = data.get('goals', {})

    user = users.get(username)
    if not user:
        users[username] = {"workouts": [], "calories": 0, "goals": goals}
    else:
        user['goals'] = goals

    return jsonify({
        "message": "Goals updated successfully!",
        "goals": users[username]['goals']
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
