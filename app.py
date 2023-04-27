import openai
import json
from flask import Flask, render_template, request
from dotenv import dotenv_values

config = dotenv_values('.env')
openai.api_key=config["API_KEY"]

app = Flask(__name__, 
    template_folder='templates',     
    static_url_path='',
    static_folder='static'    
)

def get_colors(msg):
    
    messages = [
        {"role": "system", "content": "You are a color palette generating assistant that responds to text prompts for color palettes. You should generate color palettes that fit the theme, mood or instructions in the prompt. The palettes should be between 2 and 5 colors."},
        {"role": "user", "content": "Use the following verbal description to create an accurate color palette of colors associated with this word or phrase: 'Pulp Fiction'"},
        {"role": "assistant", "content": '["#000000", "#db7d2f", "#f9d500", "#a10f0f", "#31345a"]'},
        {"role": "user", "content": "Use the following verbal description to create an accurate color palette of colors associated with this word or phrase:  '1980s Living Room'"},
        {"role": "assistant", "content": '["#4d6165", "#f0e3b9", "#9c6755", "#d3e5be", "#817874"]'},
        {"role": "user", "content": "Use the following verbal description to create an accurate color palette of colors associated with this word or phrase:  'Colors of Italy'"},
        {"role": "assistant", "content": '["#000000", "#ce2b37", "#653606", "#009246", "#ffffff"]'},
        {"role": "user", "content": f"Use the following verbal description to create an accurate color palette of colors associated with this word or phrase:  {msg}"}
    ]

    response=openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=100
    )

    
    colors = json.loads(response["choices"][0]["message"]["content"])
    return colors

# def get_colors(msg):
#     prompt = f"""
#     You are a color palette generating assistant that responds to text prompts for color palettes
#     You should generate color palettes that fit the theme, mood or instructions in the prompt.
#     The palettes should be between 2 and 5 colors.

#     Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
#     A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

#     Q: Convert the following verbal description of a color palette into a list of color: sage, nature and earth
#     A: ["#EDF1D6", "#9DC09B", "#609966", "#40513B"]

#     Desired format: a JSON array of hexadecimal colors

#     Q: Convert the following verbal description of a color palette into a list of color: {msg}
#     A:

#     Result:
#     """
#     response=openai.Completion.create(
#         prompt=prompt,
#         model="text-davinci-003",
#         max_tokens=200
#     )

#     colors = json.loads(response["choices"][0]["text"])
#     return colors

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/palette', methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}

if __name__ == "__main__":
    app.run(debug=True)