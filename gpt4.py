import streamlit as st
import openai
import re
st.set_page_config(
    page_title='Private Chat',
    layout='wide'
)
st.title("PrivateChat")
api_key = st.secrets['OPENAI_API_KEY']
openai.api_key = api_key
with st.form("form"):
    user_input = st.text_area("질문을 입력하세요", key='user_input')
    if 'user_input' not in st.session_state:
        st.session_state['질문을 입력하세요'] = user_input
    gpt4submit = st.form_submit_button("gpt-4에게 질문하기")

# Function for modifying filenames
def modify_fname(fname):
    illegal_chars = r"[\/\\\:\*\?\"\<\>\|]" # Add other characters here if needed
    return re.sub(illegal_chars, "", fname)

if gpt4submit and user_input :
    openai.api_key = api_key
    gpt_prompt =[
        {
            'role':'user',
            'content':user_input
        }
    ]
    st.markdown("----")
    res_box = st.empty()
    report = []
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=gpt_prompt,
        stream = True
    )
    for chunk in response:
        report.append(chunk['choices'][0]['delta'].get('content',''))
        result = "".join(report).strip()
        res_box.markdown(f'*{result}*')

    # Save Q&A set into a txt file
    filename = modify_fname(user_input[:40]) + ".txt"
    with open('./history/' + filename, "w") as f:
        f.write("Question: " + user_input + "\n")
        f.write("Answer: " + result + "\n")

    st.markdown("----")
else :
    st.write('ID와 질문을 확인하세요')