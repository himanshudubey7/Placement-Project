import streamlit as st
import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt

import PyPDF2
from google import genai

client = genai.Client(api_key="YOUR API KEY")

for m in client.models.list():
    print(m.name)
def ask_gemini(question, policy_text):
    prompt = f"""
    You are a placement assistant chatbot.

    Placement Policy:
    {policy_text}

    Student Question:
    {question}

    Answer clearly and briefly.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text



st.set_page_config(page_title= "Placement Dashboard 2026- KNIT", layout= 'wide')

st.title("Placement Dashboard 2026 - KNIT Sultanpur")

#loading data
df = pd.read_excel("./Placement Sheet 2025-26(On Campus + Off Campus).xlsx")
page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "Companies", "Statistics", "Chatbot"]
)



# ------------------HOME PAGE --------------------------------------------
if page == "Home":
    st.header("Overall Placemnt Overview")
    total_students = 6*60
    total_placed = len(df)
    total_companies = df["Company"].nunique()
    highest_package = df["Package(LPA)"].max()
    average_package = df["Package(LPA)"].mean()
    placement_percent = (len(df)/total_students) *100

    col1, col2 , col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Total Placed", total_placed)
    col3.metric("Placement %", f"{placement_percent:.2f}%")

    col4, col5 = st.columns(2)
    col4.metric("Highest Package(LPA)", highest_package)
    col5.metric("Average Package(LPA)", f"{average_package:.2f}")


#--------------------- Companies Page -----------------------    
elif page == "Companies":
    st.header("Companies Visited")
    company_hiring = df["Company"].value_counts().reset_index()
    company_hiring.columns = ["Company","Students Hired"]

    st.subheader("Company Hiring Summary")
    st.dataframe(company_hiring, use_container_width = True)

    #Bar chart code
    st.subheader("Company-wise Hiring(Top Companies)")
    st.bar_chart(company_hiring.set_index("Company"))



#------------------------------------Statistics Page ---------------------- 
elif page == "Statistics":
    st.header("Placement Statistics")
    st.subheader("Branch wise Placement")
    branchgroup = df.groupby("Branch")

    branchstats = branchgroup["Package(LPA)"].agg(
        students_placed = "count",
        highestpkg = "max",
        avgpkg = "mean"
    ).reset_index()

    branchstats["Placement %"] =(branchstats["students_placed"]/60)*100

    st.dataframe(branchstats, use_container_width= True)

    st.subheader("Branch-wise Placement Count")
    
    st.bar_chart(
        branchstats.set_index("Branch")["students_placed"]
    )


    st.subheader("Package Distribution")

    fig, ax = plt.subplots()
    ax.hist(df["Package(LPA)"], bins = 10)
    ax.set_xlabel("Package(LPA)")
    ax.set_ylabel("Number of Students")
    ax.set_title("Package Distribution")
    st.pyplot(fig)


#--------------------------chatbot page --------------------------

elif page == "Chatbot":
    st.header("Placement Policy Assistent")
    policy_text = f""" 
 All students eligible for On-campus/Pool campus/ Off campus (managed by 
Institute/CDC) jobs must register themselves for the placement of the current session 
with the Career Development Cell. 
2. The registration can be made through either of the two 
modes: a) By visiting the website www.knit.ac.in 
b) By submitting Google form. 
3. It is mandatory to submit a signed hardcopy of registration form to Placement Cell. 
4. A separate registration form available with the Placement Cell is to be submitted (to 
Placement Cell) for each company by those students who wish to appear for 
placement of that company. 
Application rules 
I. 
II. 
There is no restriction on appearing in interviews until the first job is 
secured. A student will be considered to have secured a job if her/his name 
appears in the selection list provided by recruiter. 
The placement for any academic year is divided into 2 categories: 
(a)  Regular: less than 5 LPA 
(b) Dream: more than or equal to 5 LPA 
III. 
IV. 
V. 
In Regular category a student can have at most 1 offer. If the package 
difference more than or equal to 3 LPA then he/she can get opportunity to 
participate in another company. 
If selected in any dream company, second offer in Dream category can be 
availed only if the package difference is more than or equal to 4 LPA as 
compared to previous offer got by student in the Dream category. 
A student cannot downgrade his package even if any company with higher 
value comes with lower package. 
VI. 
If 70% (ex. 49 out of 70 students) placement of registered students is 
achieved in any branch then that branch will be made policy free, i.e., all the 
unplaced students will be eligible to appears in a company’s interview 
process (given the company should allow the candidature of students of that 
branch). Also, students of that branch will be excluded from the categories 
Regular and Dream. 
Absenteeism rules and policy: 
1. Absenteeism in any test, interview or any selection process which an applicant has to 
attend as part of a company’s recruiting procedure or if the student has to leave the 
placement due to an emergency, the student is has to fill in the Leave Application 
form within working hours (10 AM to 5 PM) before the activity. Duly filled leave 
application form is to be submitted in person by the student or by a representative on 
behalf of the student in the Placement Cell office. The student can also send an e-mail 
with the filled Leave Application form on tpo@knit.ac.in at least 12 hours prior to the 
start of the activity. Relevant proof needs to be attached with leave application form 
for missing the event which includes: 
● Medical certificate form the medical officer of the Institute for absence on 
health grounds. 
● Other relevant proofs depending on the reason for absence. 
The Placement Cell/CDC authorities will decide whether the case is genuine or not. 
Any student who does not follow the above procedure will be DEBARRED from 
placements for the entire session. 
Off-Campus Placement 
● All the above rules are applicable for Off-Campus Placements. 
● If any student participates in any off-campus placement by his/her own then he/she 
must report and inform Placement Cell/CDC about the outcome of the off-campus 
drive. If someone hides his/her information of off-campus pre-placement offer and 
he/she enrolls in on-campus drive then CDC will take strict action against him/her 
(Any student who does not follow the above procedure will be DEBARRED from 
placements for the entire session). 
● Pre-Placement Offers will also be considered as off-campus placement and students 
who receive any Pre-Placement offer must report the same to Placement Cell/CDC. 
Further his/her campus placement will be governed by the policy described above i.e., 
if he/she gets a Pre-Placement Offer at 4 LPA then he/she can only appear in the 
Dream category.




"""
    user_question = st.text_input("Ask your policy?")

    if(user_question):
        with st.spinner("Analyzing your policy..."):

         answer = ask_gemini(user_question,policy_text)
        st.success(answer)
        





