#This is HR matchmaking application for matchmaking freelancers with jobs that fit their skills and sending them mails
import os
import smtplib
import logging
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import streamlit as st

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):
    template = """
        You are an HR Recruiter having two tables: 
        1. `freelancers` table with details about freelancers' skills and career information.
        2. `linkedin_jobs` table with job postings and their details.

        Your tasks include:
        - Perform any SQL CRUD operation based on user input.
        - Match freelancers with LinkedIn jobs using skills and requirements.
        - Generate emails for matched freelancers and companies.

        SQL Queries Examples:
        1. Retrieve data: `SELECT * FROM freelancers;`
        2. Insert data: `INSERT INTO freelancers (name, skills, email) VALUES ('John Doe', 'Python, SQL', 'john@example.com');`
        3. Update data: `UPDATE linkedin_jobs SET salary_range = '50k-70k' WHERE job_id = 1;`
        4. Delete data: `DELETE FROM freelancers WHERE id = 10;`
        5. Match freelancers: `SELECT f.name, j.title FROM freelancers f JOIN linkedin_jobs j ON f.skills LIKE CONCAT('%', j.requirements, '%');`

        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

        Question: {question}
        SQL Query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
    
    def get_schema(_):
        return db.get_table_info()

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)
    template = """
        You are an HR assistant that retrieves and matches data from two tables (`freelancers` and `linkedin_jobs`) in a database. You also generate email content for matched freelancers and companies based on job matches.

        <SCHEMA>{schema}</SCHEMA>
        Conversation History: {chat_history}
        SQL Query: <SQL>{query}</SQL>
        User question: {question}
        SQL Response: {response}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })

def send_email(recipient: str, subject: str, body: str):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    msg = f"Subject: {subject}\n\n{body}"
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg)
        logging.info(f"Email sent to {recipient}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        st.error(f"Error sending email: {e}")

# Streamlit UI
st.set_page_config(page_title="HR MatchMaker Assistance", page_icon=":speech_balloon:")
st.title("HR MatchMaker Assistance")

# Sidebar for database connection
with st.sidebar:
    st.subheader("Database Connection")
    user = st.text_input("User", value="root")
    password = st.text_input("Password", type="password", value="admin")
    host = st.text_input("Host", value="localhost")
    port = st.text_input("Port", value="3306")
    database = st.text_input("Database", value="Chinook")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            try:
                db = init_database(user, password, host, port, database)
                st.session_state.db = db
                st.success("Connected to the database!")
            except Exception as e:
                st.error(f"Connection failed: {e}")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm an HR MatchMaker Assistant. Ask me anything about your database."),
    ]

# Tabs for functionalities
tabs = st.tabs(["Chat", "Email"])

# Chat tab for SQL queries
with tabs[0]:
    st.header("Ask SQL Queries")
    user_query = st.chat_input("Type a SQL-related question...")
    if user_query and st.session_state.db:
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        
        with st.chat_message("Human"):
            st.markdown(user_query)
        
        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)
        
        st.session_state.chat_history.append(AIMessage(content=response))

# Email tab for sending emails
with tabs[1]:
    st.header("Send Emails to Matches")
    
    # Inputs for manual email sending
    sender_email = st.text_input("Sender Email", value="Ibrahimakanni1995@gmail.com")
    sender_password = st.text_input("Sender Password", type="password")
    receiver_email = st.text_input("Receiver Email")
    email_subject = st.text_input("Subject")
    email_message = st.text_area("Message")
    
    # Button to send email
    if st.button("Send Email"):
        if not receiver_email or not email_subject or not email_message:
            st.error("Please provide all required fields: Receiver Email, Subject, and Message Body.")
        else:
            try:
                from email.message import EmailMessage
                import smtplib
                import ssl

                # Create email message
                em = EmailMessage()
                em['From'] = sender_email
                em['To'] = receiver_email
                em['Subject'] = email_subject
                em.set_content(email_message)

                # Add SSL (layer of security) and send the email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(sender_email, sender_password)
                    smtp.sendmail(sender_email, receiver_email, em.as_string())

                st.success(f"Email successfully sent to {receiver_email}")
            except Exception as e:
                st.error(f"Error sending email: {e}")