import requests
import google.generativeai as genai

# Global list to store job entries from the Remotive API
final = []

def get_text(problem, category=None, company_name=None, limit=None):
    """
    Uses Google Generative AI to extract a list of job names from the input prompt,
    then queries the updated Remotive API (https://remotive.com/api/remote-jobs) for job listings
    based on each extracted job name and optional filters.

    Optional querystring parameters (as per Remotive API documentation):
      - category: Filter jobs by category (e.g., "software-dev")
      - company_name: Filter jobs by company name (case insensitive, partial match)
      - limit: Limit the number of results (integer)
    """
    global final
    final = []  # Reset the global list

    # Configure the Generative AI API (replace with your own API key)
    genai.configure(api_key="AIzaSyDY-P9ow5xwXSYVAosPKmZLA5VA40JTC0k")
    model = genai.GenerativeModel('gemini-pro')

    # Instruct the AI to output one job name per line with a leading dash (-)
    prompt = problem + " Give me only job names with no description. Output each job name on a new line starting with a dash (-)."
    
    # Generate job names using a streaming response
    response = model.generate_content(prompt, stream=True)
    
    # Process the response into individual lines
    lines = []
    for chunk in response:
        lines.extend(chunk.text.splitlines())
    
    # Clean and extract job names by removing any leading dashes and extra spaces
    job_names = []
    for line in lines:
        cleaned = line.strip()
        if cleaned.startswith('-'):
            cleaned = cleaned.lstrip('-').strip()
        if cleaned:
            job_names.append(cleaned)

    # Remotive API endpoint
    remotive_url = "https://remotive.com/api/remote-jobs"

    # Query the Remotive API for each extracted job name
    for job_name in job_names:
        # Build query parameters with mandatory "search" and optional filters
        params = {"search": job_name}
        if category:
            params["category"] = category
        if company_name:
            params["company_name"] = company_name
        if limit:
            params["limit"] = limit

        try:
            resp = requests.get(remotive_url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                jobs = data.get("jobs", [])
                for job in jobs:
                    job_entry = [
                        job.get("title", "N/A"),
                        job.get("company_name", "N/A"),
                        job.get("candidate_required_location", "N/A"),
                        job.get("job_type", "N/A")
                    ]
                    final.append(job_entry)
            else:
                print(f"Error: Unable to fetch data from Remotive for job '{job_name}'. Status code: {resp.status_code}")
        except Exception as e:
            print(f"Exception occurred while fetching data for job '{job_name}': {e}")

def send():
    """
    Returns the compiled list of job entries.
    """
    return final

# Example usage:
if __name__ == "__main__":
    # Example: Use "Software Developer" as the base problem and filter by the "software-dev" category
    problem_input = "Software Developer"
    get_text(problem_input, category="software-dev", limit=5)
    for job in send():
        print(job)
