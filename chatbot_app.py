import streamlit as st
import subprocess
import time

def query_chatbot(query_text):
    try:
        result = subprocess.run(
            ["python", "query.py", query_text],
            capture_output=True,
            text=True,
            check=True,

            # timeout=15  
            # Set a timeout for the subprocess
        )
        return result.stdout
    # except subprocess.TimeoutExpired:
    #     return "Error: Chatbot took too long to respond. Please try again."
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    

# Add Font Awesome CSS
css_example = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    .stButton button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
        font-size: 16px;
    }
</style>
'''
st.write(css_example, unsafe_allow_html=True)

st.title("Chatbot Interface")

user_input = st.text_input("You:", "")

# Use native button but styled with HTML
if st.button("Send 🚀"):
    if user_input:
        with st.spinner("Chatbot is thinking..."):
            response = query_chatbot(user_input)
        st.text_area("Chatbot:", value=response, height=200)
    else:
        st.warning("Please enter a query.")


with st.sidebar:
    st.image("logo.png", use_column_width=True)  
    st.title("Options")

    if st.button("TRAIN"):
        subprocess.Popen(["python", "train_app.py"])
        st.success("Training started!")
    st.sidebar.write("Use this to train the chatbot with new data.")
