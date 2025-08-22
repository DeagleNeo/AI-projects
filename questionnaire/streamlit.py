import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from docx import Document

load_dotenv() # Import environment variables from .env
#import os
#os.environ["http_proxy"] = "http://127.0.0.1:1083"
#os.environ["https_proxy"] = "http://127.0.0.1:1083"

client = OpenAI()

# Access the file paths from the environment variables
file_in_docx = os.getenv("FILE_IN_DOCX")
file_out_docx = os.getenv("FILE_OUT_DOCX")

def main():
    st.title("LLM Learning Background Questionnaire")

    # Create input fields for each question
    q1 = st.text_area("1. Where are you? Are you employed? What are you responsible for?")

    q2= st.text_area("2. What do you know about LLM theories or techniques?")
    
    q3 = st.text_area("3. What do you learn LLM for?")
    
    q4 = st.text_area("4. Have you used Python or other coding languages before?")
    
    q5 = st.text_area("5. How long on average can you spend on learning? When are you usually free?")
    
    q6 = st.text_area("6. Anything else to tell us?")

    # The Generate button
    if st.button("Generate"):
        user_input = {
            "Q1": q1,
            "Q2": q2,
            "Q3": q3,
            "Q4": q4,
            "Q5": q5,
            "Q6": q6
        }

        # st.write("### Your response:")
        # for key, value in user_input.items():
        #     st.write(f"**{key}**: {value}")

        # Here you can add logic to send the responses to an LLM API
        result = get_completion(str(user_input))
        file_in_docx = ""
        file_out_docx = ""
        replace_text_in_docx(file_in_docx, "[[replace]]", result, file_out_docx)
        st.success(result)

def get_completion(user_input, model="gpt-4o", temperature=0):
    instruction = """
            You are a professional large language model (LLM) tutor, providing personalized learning advice to help students better master large language model knowledge and skills. 
            Please provide professional, detailed answers and study suggestions based on the student's questions. Please reply in the following format:
        """

    examples = """
        # Example 1
            Q: Which city are you in now, are you employed, and what is your current job?
            A: I just graduated from high school. I'm in Changsha, Hunan, and I'll be going to university on the 29th in Guilin. Currently, I'm a soon-to-be university student.
            Q: How much do you know about large language models (LLMs), their principles, and technical aspects?
            A: I know nothing.
            Q: What is your core need for learning about LLMs?
            A: I want to use AI to make money and achieve financial independence during university. I also want to do more internships. Learning AI can increase my core competitiveness. I plan to work directly after my bachelor's degree, and I believe that understanding AI is essential right now.
            Q: Do you have a programming background in Python or any other language? Have you ever written code?
            A: No.
            Q: How much time can you spend on studying each day, and what are your general free time slots?
            A: Two hours, probably in the evening. I'm not entirely sure yet, as I don't know my exact university schedule.
            Q: Do you have anything else to add besides the five points above? If so, please add it here.

            Here is the reply for the student:
            The main language for LLMs is Python, which is a very simple language to learn. You can quickly watch the pre-study videos I sent you. 
            They include an explanation of basic Python syntax, as well as some videos on large models that you can get a head start on. 
            Since you don't have a basic understanding of LLMs yet, you can also continue to learn about them on platforms like YouTube by watching some relevant videos.
            Your study time is quite flexible, so you can spend more time on the basics at the beginning. Once you get started, the rest of the learning process will be much easier. 
            The prospects for LLMs are fairly good, and the industry is currently still in its early stages, so there are many opportunities. I hope you have some great achievements here.


        # Example 2
            Q: Which city are you in now, are you employed, and what is your current job?
            A: I'm in Beijing, and I'm currently employed in an agriculture-related field.
            Q: How much do you know about large language models (LLMs), their principles, and technical aspects?
            A: My knowledge is quite limited.
            Q: What is your core need for learning about large models?
            A: Personal skill improvement and business needs.
            Q: Do you have a programming background in Python or any other language? Have you ever written code?
            A: Yes.
            Q: How much time can you spend on studying each day, and what are your general free time slots?
            A: About 3 hours, usually after 6 PM.
            Q: Do you have anything else to add besides the five points above? If so, please add it here.

            Here is the reply for the student:
            As someone working in agriculture in Beijing, although your understanding of LLMs is limited, your Python programming background and experience with writing code are excellent starting points for learning about LLMs, as Python is the primary language used. 
            I recommend you start with our pre-study courses to fill in the gaps in your knowledge. Your goals of personal skill enhancement and business needs align perfectly with the current trend of AI development in the agricultural sector. 
            With about three hours available after 6 PM each day, your schedule is very flexible. Given your programming background and commitment to learning, it is very feasible for you to transition into AI project management.
            While the AI field is still in its early stages, its rapid technological development means its application prospects are vast. Now it is a great time to learn and seize these new industry opportunities.
    """

    prompt = f"""
            {instruction}
            {examples}
            User input:
            {user_input}
            Constraints: Constraints
                - Only provide advice related to learning LLMs; decline to answer questions unrelated to LLMs.
                - The advice must be specific, feasible, targeted, and actionable.
                - When replying, do not add "Here is the reply for the student:" or repeat the questions.
        """
    print(prompt)
    
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

def replace_text_in_docx(doc_path, old_text, new_text, output_path):
    doc = Document(doc_path)
    for para in doc.paragraphs:
        if old_text in para.text:
            para.text = para.text.replace(old_text, new_text)
    doc.save(output_path)

if __name__ == "__main__":
    main()

    
