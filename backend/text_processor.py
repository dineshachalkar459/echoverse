"""Text processing helpers for tone-based rewriting."""


class TextProcessor:
    """Applies different tones to the input text."""

    TONE_PROMPTS = {
        "Neutral": "Rewrite the following text in a neutral, professional tone while preserving the original meaning:",
        "Suspenseful": "Rewrite the following text in a suspenseful, dramatic tone while preserving the original meaning:",
        "Inspiring": "Rewrite the following text in an inspiring, motivational tone while preserving the original meaning:",
    }

    @staticmethod
    def rewrite_text(text, tone):
        if tone == "Neutral":
            return text
        if tone == "Suspenseful":
            return f"{text}... with dramatic tension building throughout the narrative, creating an atmosphere of anticipation and mystery."
        if tone == "Inspiring":
            return f"{text} - a powerful and uplifting message that inspires hope, motivation, and positive change in the listener."
        return text

    @staticmethod
    def get_tone_prompt(tone):
        return TextProcessor.TONE_PROMPTS.get(tone, TextProcessor.TONE_PROMPTS["Neutral"])
