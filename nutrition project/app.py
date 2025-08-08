from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import os

app = Flask(__name__)
MEAL_FILE = 'meal_data.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/meal_generator')
def meal_generator():
    return render_template('meal_generator.html')

# This endpoint is called from the frontend to trigger the Relay.app playbook
@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    data = request.get_json()
    relay_webhook_url = "https://hook.relay.app/api/v1/playbook/cme13nuc60fij0om1hbsbbvtv/trigger/wjzFPhTLSc7pQIcRQGhggg"
    
    try:
        # We don't need the response, just that the call was successful
        requests.post(relay_webhook_url, json=data)
        
        # Clear any old data to prepare for the new meal plan
        if os.path.exists(MEAL_FILE):
            os.remove(MEAL_FILE)
            
        return jsonify({"status": "trigger_sent"}), 200

    except requests.exceptions.RequestException as e:
        print("Error communicating with Relay.app:", e)
        return jsonify({"status": "error", "message": "Failed to trigger meal plan generation."}), 500

# This endpoint is the webhook that Relay.app sends the FINAL JSON data to
@app.route('/receive-meal', methods=['POST'])
def receive_meal():
    data = request.get_json()
    print("Received meal data from Relay:", data)
    
    # Save the received data to a file
    with open(MEAL_FILE, "w") as f:
        json.dump(data, f)
        
    return jsonify({"status": "success"}), 200

# This new endpoint is for the client-side JavaScript to poll
@app.route('/check_meal_status')
def check_meal_status():
    if os.path.exists(MEAL_FILE) and os.path.getsize(MEAL_FILE) > 0:
        return jsonify({"status": "ready"})
    return jsonify({"status": "not_ready"})

@app.route('/display_meal')
def display_meal():
    try:
        with open(MEAL_FILE, "r") as f:
            meal_plan = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        meal_plan = {}
    return render_template("display_meal.html", meal=meal_plan)

@app.route('/loading')
def loading():
    return render_template('loading.html')

from nutritional_analyzer import get_nutrition_data, parse_food_nutrients
@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    nutrition_data = None

    if request.method == 'POST':
        meal_text = request.form.get('meal_text')

        api_response = get_nutrition_data(meal_text)
        if api_response:
            nutrition_data = parse_food_nutrients(api_response)

    return render_template('analyze.html', nutrition=nutrition_data)

@app.route('/community_recipe', methods=['GET', 'POST'])
def community_recipes():
    submitted_recipe = None
    
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        recipe_details = request.form.get('recipe_details')
        
        submitted_recipe = {
            'name': recipe_name,
            'details': recipe_details
        }
        
    return render_template('community_recipe.html', submitted_recipe=submitted_recipe)
if __name__ == '__main__':
    app.run(debug=True)