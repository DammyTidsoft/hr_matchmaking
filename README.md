# HR Matchmaking Application

## Overview
The **HR Matchmaking Application** is an AI-powered tool designed to streamline the hiring process by matching freelancers with job opportunities that align with their skills. The application includes the following features:
- **Job Matching:** Matches freelancers with job postings based on their resumes and skills.
- **Resume Scanning:** Utilizes an ATS (Applicant Tracking System) to scan resumes and compare them to job descriptions.
- **Email Notifications:** Sends personalized emails to matched candidates and hiring companies to facilitate the recruitment process.

This application aims to simplify hiring, enhance job matching accuracy, and provide seamless communication between job seekers and recruiters.

---

## Features
### 1. **Freelancer and Job Matching**
- Matches freelancers with job opportunities using a SQL database containing `freelancers` and `linkedin_jobs` tables.
- Ensures accurate matching by comparing required job skills with freelancer profiles.

### 2. **Applicant Tracking System (ATS)**
- Scans uploaded resumes and compares them to job descriptions.
- Provides a detailed analysis, including:
  - Matching percentage.
  - Missing keywords.
  - Suggestions to improve the resume.

### 3. **Email Notifications**
- Automatically generates and sends personalized emails to:
  - Freelancers about job matches.
  - Hiring managers about suitable candidates.
- Ensures efficient communication for faster recruitment decisions.

---

## Installation
### Prerequisites
- Python 3.9 or later.
- A MySQL database with tables for freelancers and job postings.
- Installed dependencies listed in `requirements.txt`.
- Access to a server with Llama 3.2 installed (for AI functionalities).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hr-matchmaking-app.git
   cd hr-matchmaking-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file and configure the following:
   ```env
   DB_USER=your_db_username
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=3306
   DB_NAME=your_database_name
   SENDER_EMAIL=your_email@example.com
   SENDER_PASSWORD=your_email_password
   LLAMA_API_KEY=your_llama_api_key
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage
### Connecting to the Database
1. Open the application in your browser.
2. Navigate to the **Database Connection** sidebar.
3. Enter your database credentials and connect.

### Job Matching
1. Go to the **HR Matchmaking** tab.
2. Type your query (e.g., "Find matches for web developer").
3. View the SQL query and results.

### ATS Resume Scanning
1. Navigate to the **Smart ATS** tab.
2. Paste a job description.
3. Upload a freelancer's resume in PDF format.
4. View the analysis and suggested improvements.

### Sending Emails
1. Navigate to the **Email** tab.
2. Fill in the recipient's email, subject, and message.
3. Click **Send Email** to notify matched candidates or companies.

---

## Technologies Used
- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** MySQL
- **AI Models:** Llama 3.2 for natural language processing and resume/job matching
- **Libraries:**
  - `PyPDF2`: For parsing resumes.
  - `smtplib`: For sending emails.
  - `langchain`: For AI-based text generation and queries.

---

## Future Enhancements
- Add support for multiple languages.
- Integrate advanced analytics to track recruitment metrics.
- Expand the ATS system to support additional file formats like Word and Excel.

---

## Contribution
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your branch.
4. Submit a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For questions or support, please reach out to:
- **Email:** Ibrahimdamilare123@gmail.com
- **GitHub:** DammyTidsoft(https://github.com/DammyTidsoft)

---

Enjoy using the **HR Matchmaking Application** to revolutionize the hiring process! 🚀
