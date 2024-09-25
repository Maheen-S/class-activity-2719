from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

dataset = [
    ["Sunny", "Hot", "High", "Weak", "No"],
    ["Sunny", "Hot", "High", "Strong", "No"],
    ["Overcast", "Hot", "High", "Weak", "Yes"],
    ["Rainy", "Mild", "High", "Weak", "Yes"],
    ["Rainy", "Cool", "Normal", "Weak", "Yes"],
    ["Rainy", "Cool", "Normal", "Strong", "No"],
    ["Overcast", "Cool", "Normal", "Strong", "Yes"],
    ["Sunny", "Mild", "High", "Weak", "No"],
    ["Sunny", "Cool", "Normal", "Weak", "Yes"],
    ["Rainy", "Mild", "Normal", "Weak", "Yes"],
    ["Sunny", "Mild", "Normal", "Strong", "Yes"],
    ["Overcast", "Mild", "High", "Strong", "Yes"],
    ["Overcast", "Hot", "Normal", "Weak", "Yes"],
    ["Rainy", "Mild", "High", "Strong", "No"]
]

prob_yes = 0.7
prob_no = 0.3
num_features = 4
feature_probabilities = {}

for feature_idx in range(num_features):
    feature_probabilities[feature_idx] = {}
    feature_values = set(row[feature_idx] for row in dataset)
    for class_label in ['Yes', 'No']:
        class_instances = [entry for entry in dataset if entry[-1] == class_label]
        total_class_instances = len(class_instances)
        feature_probabilities[feature_idx][class_label] = {}
        for feature_value in feature_values:
            instances_with_value = [entry for entry in class_instances if entry[feature_idx] == feature_value]
            probability = len(instances_with_value) / total_class_instances
            feature_probabilities[feature_idx][class_label][feature_value] = probability

def pred(user_input):
    class_probabilities_given_input = {}
    for class_label, class_prob in [('Yes', prob_yes), ('No', prob_no)]:
        class_probabilities_given_input[class_label] = class_prob
        for feature_idx, feature_value in enumerate(user_input):
            class_probabilities_given_input[class_label] *= feature_probabilities[feature_idx][class_label].get(feature_value, 0)
    return class_probabilities_given_input

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    outlook = request.form.get('outlook')
    temperature = request.form.get('temperature')
    humidity = request.form.get('humidity')
    wind = request.form.get('wind')

    user_input = [outlook, temperature, humidity, wind]
    probabilities = pred(user_input)
    predicted_class = max(probabilities, key=probabilities.get)
    
    return jsonify({"prediction": predicted_class})

if __name__ == "__main__":
    app.run(debug=True)
