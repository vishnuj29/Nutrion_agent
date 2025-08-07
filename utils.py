import os
from groq import Groq
from dotenv import load_dotenv
import pytesseract
from PIL import Image

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful AI nutrition assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def get_nutrition_facts(dish_name):
    prompt = f"What are the nutrition facts for {dish_name}?"
    return ask_groq(prompt)

def generate_meal_plan(goal):
    prompt = f"Create a meal plan based on this goal: {goal}. Include breakfast, lunch, and dinner."
    return ask_groq(prompt)

def explain_food_choice(dish_name):
    prompt = f"Explain why {dish_name} is a healthy or unhealthy choice and what makes it suitable or not for common fitness or health goals."
    return ask_groq(prompt)

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
