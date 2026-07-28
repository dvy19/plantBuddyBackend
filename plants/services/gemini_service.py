from google import genai
from django.conf import settings
import json
import traceback
import re

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




def plant_faq_question(plant, faq_question):
    try:

        user_question = faq_question.prompt_template.format(
            plant_name=plant.name,
            scientific_name=plant.scientific_name
        )

        prompt = f"""
You are PlantBuddy AI.

Use the following plant information as the PRIMARY source of truth.

Plant Information

Name: {plant.name}
Scientific Name: {plant.scientific_name}
Category: {plant.category.name}
Description: {plant.description}
Light Requirement: {plant.light_requirement.name}
Water Requirement: {plant.water_requirement.name}
Soil: {plant.soil_type.name}
Season: {plant.season.name}
Temperature: {plant.temperature_min}°C - {plant.temperature_max}°C
Humidity: {plant.humidity}
Growth Rate: {plant.growth_rate.name}
Lifespan: {plant.lifespan.name}
Average Height: {plant.average_height}
Fertilizer: {plant.fertilizer}

Instructions

- Use the supplied plant information whenever possible.
- Use botanical knowledge only to supplement missing information.
- Never contradict the supplied data.
- Keep the answer concise and practical.
- Answer in simple English.
- Return ONLY valid JSON.
- Do NOT wrap the JSON in markdown.
- Do NOT use ```json.
- The "tips" array must contain exactly 3 items.

Return this JSON format only:

{{
    "question": "{user_question}",
    "answer": "...",
    "tips": [
        "...",
        "...",
        "..."
    ]
}}

User Question:
{user_question}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        response_text = response.text.strip()

        # Remove ```json ... ```
        response_text = re.sub(r"^```json\s*", "", response_text)
        response_text = re.sub(r"^```\s*", "", response_text)
        response_text = re.sub(r"\s*```$", "", response_text)

        return json.loads(response_text)

    except Exception as e:
        print("Gemini API Error:", e)
        traceback.print_exc()
        raise

