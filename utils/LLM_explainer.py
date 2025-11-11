import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY_1")
print(API_KEY)

if not API_KEY:
    raise ValueError("API key not found! Ensure GEMINI_API_KEY_1 is set in .env file")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_explanation(data: dict) -> str:
    """
    Generate an educational explanation for why one algorithm won.
    
    Args:
        data: dict containing keys:
            - category
            - p1_algo, p2_algo
            - p1_input, p2_input
            - p1_time, p2_time
            - p1_memory, p2_memory
            - p1_score, p2_score
            - winner
    
    Returns:
        str: Gemini-generated explanation text
    """

    prompt = f"""
You are an educational AI system analyzing algorithm performance battles.
Explain clearly and accurately *why* one algorithm won the competition.

Context:
Category: {data['category']}
Player 1 Algorithm: {data['p1_algo']}
Player 2 Algorithm: {data['p2_algo']}

Player 1 Input: {str(data['p1_input'])[:400]}
Player 2 Input: {str(data['p2_input'])[:400]}

Performance Summary:
- Player 1: Time = {data['p1_time']} ms | Memory = {data['p1_memory']} KB | Score = {data['p1_score']}
- Player 2: Time = {data['p2_time']} ms | Memory = {data['p2_memory']} KB | Score = {data['p2_score']}

Winner: {data['winner']}

Now, write a 4-6 sentence educational explanation of why {data['winner']}’s algorithm won.
Include algorithmic principles like time complexity, space usage, or internal mechanics that led to this result.
Avoid generic praise. Focus on technical clarity and educational insight.
"""

    try:
        print("[INFO] Requesting Gemini explanation...")
        start = time.time()
        response = model.generate_content(prompt)
        end = time.time()
        print(f"[INFO] Response received in {round(end - start, 2)}s")

        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Gemini API failed: {e}")
        return "Unable to generate explanation due to an API issue."
