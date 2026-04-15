class RAGService:
    def generate_response(self, prompt: str, context_id: str | None = None) -> dict:
        return {
            "prompt": prompt,
            "context_id": context_id,
            "status": "placeholder",
        }
