from google import genai
from django.conf import settings
import json
import traceback

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def plant_facts_for_a_day():
    try:
        prompt = """
            You are an expert botanist.

            Generate one unique Plant Fact of the Day.

            Choose a random topic from:
            - Plant biology
            - Indoor plants
            - Medicinal plants
            - Flowers
            - Trees
            - Fruits
            - Seeds
            - Plant adaptations
            - Gardening
            - Environmental importance
            - Plant history
            - Rare plants
            - Carnivorous plants
            - Desert plants
            - Rainforest plants

            Rules:
            - The fact must be scientifically accurate.
            - Keep the fact between 30 and 60 words.
            - Use simple, easy-to-understand English.
            - Make the fact interesting and educational.
            - Do not include emojis.
            - Do not use markdown.
            - Do not include any introductory or concluding text.
            - Return ONLY valid JSON.
            - Ensure the JSON is valid and can be parsed directly.

            Return this exact JSON structure:

            {
            "title": "Short, catchy title",
            "fact": "Interesting plant fact.",
            "category": "Science | Nature | Gardening | History | Environment | Fun Fact"
            }
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        print("========== GEMINI RESPONSE ==========")
        print(response)
        print("=====================================")

        response_text = response.text
        print("Response Text:", response_text)

        try:
            return json.loads(response_text)

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            print("Raw Response:", response_text)
            traceback.print_exc()
            raise

    except Exception as e:
        print("Gemini API Error:", str(e))
        traceback.print_exc()
        raise