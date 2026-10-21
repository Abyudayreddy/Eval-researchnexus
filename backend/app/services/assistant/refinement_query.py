import re
from typing import List
from app.services.assistant.eligibility import ContextEligibility

class RefinementQueryGenerator:
    @staticmethod
    def generate_queries(
        original_query: str,
        suggested_focus: List[str],
        eligibility: ContextEligibility
    ) -> List[str]:
        """
        Generates targeted refinement queries for missing/unsupported claims
        strictly respecting scope eligibility.
        """
        # Rule: current_evidence = zero retrieval
        if not eligibility.should_retrieve:
            return []

        queries = []
        for focus_text in suggested_focus[:2]:  # Limit to top 2 gap areas
            # Extract key words/nouns from focus text
            clean_focus = re.sub(r'[^\w\s]', '', focus_text)
            words = [w for w in clean_focus.split() if len(w) > 3]
            if words:
                keyword_str = " ".join(words[:4])
                queries.append(f"{original_query} {keyword_str}")

        if not queries:
            queries.append(original_query)

        return queries
