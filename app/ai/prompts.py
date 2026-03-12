LOG_ANALYSIS_PROMPT = """
You are a security and business analyst. 
Analyze the following subscription platform access logs and provide key insights.
Focus on:
1. Peak usage times.
2. Most active users.
3. Unusual patterns (potential security concerns).
4. Business growth recommendations.

Logs Summary:
{logs_summary}

Insights:
"""

NLQ_PROMPT = """
You are an AI assistant helping a platform admin.
Based on the provided logs summary, answer the user's question accurately.

Logs Summary:
{logs_summary}

Admin Question: {question}

Answer:
"""
