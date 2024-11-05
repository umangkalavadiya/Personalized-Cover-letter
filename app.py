from flask import Flask, render_template, request, flash, redirect, url_for
from openai import OpenAI
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# Simplified personal data
PERSONAL_INFO = """
I have professional certification in Data science and AI foundation from IBM. I have 1 year of experience as an expert prompt engineer optimizing and refining the best quality prompt and generating the highest quality output from LLMS like Llama, GPTs ,Gemini, Mistral and etc. I have extensive experience working with OpenAI assistant API and integrating to the application. Utilizing the ai and integrating to any application is my expertise.

I have great experience with Generative AI. I have created conversation chatbot using LLMs like GPT and also with frameworks like RASA, botpress , chatbase etc. I have  3 years of experience in AI/ML technology, including 1 year of professional experience as a conversational AI engineer.

I have extensive experience in python with frameworks like flask,streamlit and fastAPI I can create great UI for any AI application. My skillset includes: python,html,css, OpenAI, API integration, LLM , Prompt engineering , Prompt optimization, LLM integration, LLM fine tunning, NLP, classifiers, machine learning,deep learning , tensorflow, keras, transfer learning, chatbot, CNN  data labelling, GenerativeAI
"""

class CoverLetterGenerator:
    def __init__(self):
        self.client = client
        self.personal_info = PERSONAL_INFO

    def generate_cover_letter(self, job_description, special_notes=""):
        prompt = f"""
        Generate a compelling cover letter for the following job description using my background information.
        Match my experience and skills to the job requirements.
        
        MY BACKGROUND:
        {self.personal_info}
        
        JOB DESCRIPTION:
        {job_description}
        
        SPECIAL NOTES TO INCLUDE:
        {special_notes}

        Please write a professional cover letter that:
        1. Matches my relevant experience and skills to the job requirements
        2. Emphasizes my AI/ML expertise and practical implementation experience
        3. Highlights my ability to integrate and optimize AI solutions
        4. Maintains a confident yet professional tone
        5. Dont forget to add the special note provide by user.
        6. Make sure the generated cover letter does not lool like AI Generated
        7. Generate a cover letter under 350 words stricly.
        8. Do not introduce any additional oppinion of extra information from your side, Only use the information provide above to generate the best cover letter.
        9. Only picks the necessary information based on the Job description which is relevant to the job requirements.
        10. Dont start with the simple sentence like "I am writting to express" or "I am exited to apply". Use something engaging and interesting to make it look like human generated cover letter.
        11. Dont include the details like [Your Address]  [City, State, Zip] [Your Email] [Your Phone Number] [Date] [Hiring Manager's Name][Company Name] [Company Address][City, State, Zip]  
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional cover letter writer focused on AI/ML positions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error generating cover letter: {str(e)}"

    def refine_cover_letter(self, original_cover_letter, recommendation):
        prompt = f"""
        Please refine this cover letter based on the given recommendation.
        Keep the core message and experience details intact while implementing the suggested improvements.

        ORIGINAL COVER LETTER:
        {original_cover_letter}

        RECOMMENDATION:
        {recommendation}

        Please provide an improved version that:
        1. Addresses the points in the recommendation
        2. Maintains accuracy about experience and skills
        4. Preserves the relevant job-specific details
        4. Maintains a confident yet professional tone
        5. Dont forget to add the special note provide by user.
        6. Make sure the generated cover letter does not lool like AI Generated
        7. Generate a cover letter under 350 words stricly.
        8. Do not introduce any additional oppinion of extra information from your side.
        10. Dont start with the simple sentence like "I am writting to express" or "I am exited to apply". Use something engaging and interesting to make it look like human generated cover letter.
        11. Dont include the details like [Your Address]  [City, State, Zip] [Your Email] [Your Phone Number] [Date] [Hiring Manager's Name][Company Name] [Company Address][City, State, Zip]
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional cover letter editor. Maintain accuracy while implementing improvements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error refining cover letter: {str(e)}"

generator = CoverLetterGenerator()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    job_description = request.form.get('job_description')
    special_notes = request.form.get('special_notes', '')

    if not job_description:
        flash('Please provide the job description.')
        return redirect(url_for('index'))

    cover_letter = generator.generate_cover_letter(job_description, special_notes)
    return render_template('result.html', cover_letter=cover_letter)

@app.route('/refine', methods=['POST'])
def refine():
    original_cover_letter = request.form.get('original_cover_letter')
    recommendation = request.form.get('recommendation')

    if not original_cover_letter or not recommendation:
        flash('Please provide both the original cover letter and recommendation.')
        return redirect(url_for('index'))

    refined_letter = generator.refine_cover_letter(original_cover_letter, recommendation)
    return render_template('result.html', cover_letter=refined_letter, show_original=True, original_letter=original_cover_letter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))