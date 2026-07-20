from dotenv import load_dotenv
import os
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI Hospital Receptionist.

Your job is to classify patients into ONLY ONE of these departments:

1. Emergency
2. General
3. Mental Health
4. Pediatrics
5. Orthopedics

Rules:
- Return ONLY valid JSON.
- Never create any department other than:
  Emergency, General, Mental Health, Pediatrics, Orthopedics.
- If symptoms are severe (bleeding, unconscious, accident, stroke, heart attack), use Emergency.
- Fever, cough, headache, stomach pain -> General.
- Stress, anxiety, depression -> Mental Health.
- Child or baby -> Pediatrics.
- Bone pain, fracture, joint injury -> Orthopedics.

Return ONLY this JSON and nothing else:

{{
    "department": "General",
    "urgency": "Low",
    "reason": "Reason for choosing the department."
}}
"""
        ),
        ("human", "{symptoms}")
    ]
)

chain = prompt | llm


def classify_patient(symptoms):
    response = chain.invoke({"symptoms": symptoms})

    content = response.content.strip()

    # Remove markdown if model returns ```json
    if content.startswith("```"):
        content = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        return json.loads(content)

    except Exception:
        return {
            "department": "General",
            "urgency": "Low",
            "reason": "Unable to parse AI response. Assigned to General Department."
        }