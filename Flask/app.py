from flask import Flask, request, render_template
import os
from openai import OpenAI
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)  # Set logging to debug level

# Initialize OpenAI client
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ''
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        formatted_ingredients = json.dumps(ingredients.split(','))
        user_message = (
            f"Title: {title}\n\n"
            f"Ingredients: {formatted_ingredients}\n\n"
            "Generic ingredients: "
        )
        try:
            response = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-0125:personal::9HXzQxmi",
                messages=[
                    {"role": "system", "content": "You are a helpful recipe assistant. You are to extract the generic ingredients from each of the recipes provided."},
                    {"role": "user", "content": user_message}
                ]
            )
            # Debugging the path through the response
            if 'choices' in response and len(response['choices']) > 0:
                if 'message' in response['choices'][0]:
                    response_text = response['choices'][0]['message']['content']
                else:
                    response_text = "No 'message' key in response choice."
                    print("Missing 'message' key in the choice:", response['choices'][0])
            else:
                response_text = "No response generated or empty choices array."
                print("Response 'choices' is missing or empty:", response)
        except Exception as e:
            response_text = f"An error occurred: {str(e)}"
            logging.error(f"Error during API call: {str(e)}")
            print("Exception occurred:", e)

        print("API Full Response:", response)
        print("Response Text:", response_text)

    return render_template('index.html', response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True)