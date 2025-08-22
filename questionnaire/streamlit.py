import streamlit as st

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
        response = send_to_model(
            "Q1": q1,
            "Q2": q2,
            "Q3": q3,
            "Q4": q4,
            "Q5": q5,
            "Q6": q6
        )

        st.write("### Your response:")
        for key, value in user_input.items():
            st.write(f"**{key}**: {value}")

        # Here you can add logic to send the responses to an LLM API
        st.success("Your responses have been sent to LLM for analysis!")

if __name__ == "__main__":
    main()

    
