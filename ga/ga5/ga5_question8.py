import re

def generate_duckdb_query(question):
    # Regex to extract the timestamp and useful stars
    timestamp_pattern = r"after (\S+)"
    useful_stars_pattern = r"with (\d+) useful stars"
    
    # Extract values using regex
    timestamp_match = re.search(timestamp_pattern, question)
    useful_stars_match = re.search(useful_stars_pattern, question)
    
    if timestamp_match and useful_stars_match:
        timestamp = timestamp_match.group(1)
        useful_stars = useful_stars_match.group(1)
        
        # Constructing the SQL query using the extracted values
        query = f"""
        SELECT post_id
        FROM (
            SELECT post_id
            FROM (
                SELECT post_id,
                       json_extract(comments, '$[*].stars.useful') AS useful_stars
                FROM social_media
                WHERE timestamp >= '{timestamp}'
            )
            WHERE EXISTS (
                SELECT 1 FROM UNNEST(useful_stars) AS t(value)
                WHERE CAST(value AS INTEGER) >= {useful_stars}
            )
        )
        ORDER BY post_id;
        """
        cleaned_answer = query.replace("\n", " ").strip()
        return cleaned_answer
    else:
        return "Couldn't extract values from the question."
