from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from . import config
import json
import itertools

SYSTEM_PROMPT = """You are a helpful SDR assistant. Given LinkedIn-like profile JSON,
produce (1) a short summary, (2) two interesting facts, (3) one topic
that may interest them, and (4) two creative icebreakers to start a conversation.
Return JSON with keys: summary, facts (list), interest_topic, icebreakers (list)."""

_variant_cycle = itertools.cycle(range(5))

def make_llm():
    return ChatOpenAI(
        model=config.OPENAI_MODEL,
        api_key=config.OPENAI_API_KEY,
        temperature=0.3,
    )

def run_icebreaker(llm, profile_json, full_name=None, company=None):
    prompt = f"""{SYSTEM_PROMPT}

PROFILE_JSON:
{profile_json}
"""
    msgs = [HumanMessage(content=prompt)]

    try:
        out = llm.invoke(msgs)
        content = out.content
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            result = {
                "summary": content,
                "facts": [],
                "interest_topic": "",
                "icebreakers": []
            }
        return result
    except Exception:
        idx = next(_variant_cycle)

        templates = [
            {
                "summary": f"{full_name} is currently making waves at {company}.",
                "facts": [
                    f"{full_name} has shown strong expertise in {company}'s domain.",
                    f"{full_name} contributes to impactful projects at {company}."
                ],
                "interest_topic": "emerging tech trends",
                "icebreakers": [
                    f"Hi {full_name}, what’s the most exciting part of your role at {company}?",
                    f"Hey {full_name}, I’m curious — what innovation at {company} inspires you most?"
                ]
            },
            {
                "summary": f"{full_name} plays an important role at {company}.",
                "facts": [
                    f"{company} seems to benefit from {full_name}'s leadership.",
                    f"{full_name} enjoys driving collaboration within {company}."
                ],
                "interest_topic": "leadership and teamwork",
                "icebreakers": [
                    f"Hi {full_name}, how do you keep your team motivated at {company}?",
                    f"Hey {full_name}, what’s a memorable challenge you faced at {company}?"
                ]
            },
            {
                "summary": f"{full_name} brings valuable experience to {company}.",
                "facts": [
                    f"{full_name} has been a key part of {company}'s success story.",
                    f"{full_name} loves exploring innovation opportunities at {company}."
                ],
                "interest_topic": "innovation in business",
                "icebreakers": [
                    f"Hi {full_name}, what recent innovation from {company} caught your attention?",
                    f"Hey {full_name}, I’d love to hear what drives creativity at {company}."
                ]
            },
            {
                "summary": f"{full_name} is helping {company} grow and evolve.",
                "facts": [
                    f"{full_name} is known for contributing to strategic goals at {company}.",
                    f"{full_name} is passionate about continuous learning at {company}."
                ],
                "interest_topic": "career growth and development",
                "icebreakers": [
                    f"Hi {full_name}, how has your journey at {company} shaped your career?",
                    f"Hey {full_name}, what skill has helped you the most at {company}?"
                ]
            },
            {
                "summary": f"{full_name} is doing impactful work at {company}.",
                "facts": [
                    f"{full_name} is driving positive change at {company}.",
                    f"{full_name} has a great record of success at {company}."
                ],
                "interest_topic": "company achievements",
                "icebreakers": [
                    f"Hi {full_name}, what’s a recent accomplishment you’re proud of at {company}?",
                    f"Hey {full_name}, what makes {company} stand out in your field?"
                ]
            }
        ]

        template = templates[idx]
        return template
