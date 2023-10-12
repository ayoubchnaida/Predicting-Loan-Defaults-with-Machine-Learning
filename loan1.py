import streamlit as st
import pickle
import pandas as pd
# Load the trained model
model = pickle.load(open('loan.sav', 'rb'))
# Streamlit web app
def main():
    st.title("Loan Approval Prediction")
    st.image('https://media.tenor.com/i0q4bYZVVHcAAAAC/ppp-loan-please-wait.gif')
    # Sidebar with user inputs
    st.sidebar.header("User Input")

    # User inputs for loan application details
    loan_amnt = st.sidebar.number_input("Loan Amount")
    installment = st.sidebar.number_input("Installment Amount")
    
    grade = st.sidebar.selectbox("Grade", ('A', 'B', 'C', 'D', 'E', 'F', 'G'))
    emp_length = st.sidebar.selectbox("Employment Length", (
        "10+ years", "9 years", "8 years", "7 years", "6 years", "5 years",
        "4 years", "3 years", "2 years", "1 year", "< 1 year", "n/a"
    ))
    annual_inc = st.sidebar.number_input("Annual Income")
    dti = st.sidebar.number_input("Debt-to-Income Ratio")
    delinq_2yrs = st.sidebar.number_input("Number of Delinquencies in the Last 2 Years")
    inq_last_6mths = st.sidebar.number_input("Number of Inquiries in the Last 6 Months")
    open_acc = st.sidebar.number_input("Number of Open Credit Lines")
    pub_rec = st.sidebar.number_input("Number of Public Records")
    revol_bal = st.sidebar.number_input("Revolving Balance")
    revol_util = st.sidebar.number_input("Revolving Utilization Rate (%)")
    total_acc = st.sidebar.number_input("Total Number of Accounts")
    fico_average = st.sidebar.number_input("FICO Average Score")
    
    # User inputs for loan terms and other categorical variables
    term = st.sidebar.selectbox("Loan Term", (' 36 months', ' 60 months'))
    home_ownership = st.sidebar.selectbox("Home Ownership", ('RENT', 'OWN', 'MORTGAGE', 'OTHER', 'NONE'))
    verification_status = st.sidebar.selectbox("Verification Status", ('Source Verified', 'Verified', 'Not Verified'))
    purpose = st.sidebar.selectbox("Loan Purpose", (
        'credit_card', 'debt_consolidation', 'educational', 'home_improvement',
        'house', 'major_purchase', 'medical', 'moving', 'other', 'renewable_energy',
        'small_business', 'vacation', 'wedding'
    ))
    
    # Encode categorical variables
    term_enc = {' 36 months': 0, ' 60 months': 1}[term]
    grade_enc = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7
    }[grade]
    emp_length_enc = {
        '10+ years': 10, '9 years': 9, '8 years': 8, '7 years': 7, '6 years': 6,
        '5 years': 5, '4 years': 4, '3 years': 3, '2 years': 2, '1 year': 1,
        '< 1 year': 0, 'n/a': 0
    }[emp_length]
    home_ownership_enc = {
        'RENT': 1, 'OWN': 2, 'MORTGAGE': 3, 'OTHER': 4, 'NONE': 5
    }[home_ownership]
    verification_status_enc = {
        'Source Verified': 1, 'Verified': 2, 'Not Verified': 3
    }[verification_status]
    purpose_enc = {
        'credit_card': 1, 'debt_consolidation': 2, 'educational': 3, 'home_improvement': 4,
        'house': 5, 'major_purchase': 6, 'medical': 7, 'moving': 8, 'other': 9,
        'renewable_energy': 10, 'small_business': 11, 'vacation': 12, 'wedding': 13
    }[purpose]

    # Create a DataFrame with user inputs
    input_data = pd.DataFrame({
        'loan_amnt': [loan_amnt],
        'installment': [installment],
        'grade': [grade_enc],
        'emp_length': [emp_length_enc],
        'annual_inc': [annual_inc],
        'dti': [dti],
        'delinq_2yrs': [delinq_2yrs],
        'inq_last_6mths': [inq_last_6mths],
        'open_acc': [open_acc],
        'pub_rec': [pub_rec],
        'revol_bal': [revol_bal],
        'revol_util': [revol_util],
        'total_acc': [total_acc],
        'fico_average': [fico_average],
        'term_ 60 months': [term_enc],
        'home_ownership_NONE': [int(home_ownership == 'NONE')],
        'home_ownership_OTHER': [int(home_ownership == 'OTHER')],
        'home_ownership_OWN': [int(home_ownership == 'OWN')],
        'home_ownership_RENT': [int(home_ownership == 'RENT')],
        'verification_status_Source Verified': [int(verification_status == 'Source Verified')],
        'verification_status_Verified': [int(verification_status == 'Verified')],
        'purpose_credit_card': [int(purpose == 'credit_card')],
        'purpose_debt_consolidation': [int(purpose == 'debt_consolidation')],
        'purpose_educational': [int(purpose == 'educational')],
        'purpose_home_improvement': [int(purpose == 'home_improvement')],
        'purpose_house': [int(purpose == 'house')],
        'purpose_major_purchase': [int(purpose == 'major_purchase')],
        'purpose_medical': [int(purpose == 'medical')],
        'purpose_moving': [int(purpose == 'moving')],
        'purpose_other': [int(purpose == 'other')],
        'purpose_renewable_energy': [int(purpose == 'renewable_energy')],
        'purpose_small_business': [int(purpose == 'small_business')],
        'purpose_vacation': [int(purpose == 'vacation')],
        'purpose_wedding': [int(purpose == 'wedding')]
    })

    # Make predictions
    if st.sidebar.button("Predict"):
        prediction = model.predict(input_data)
        st.markdown("<h1 style='text-align:;'>Loan Prediction Result:</h1>", unsafe_allow_html=True)
        if prediction == 1:
            st.write("Approved")
            st.image('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbms0Y2V5emRlNnVjYnBxc2ZzaHhpM2h0Ym02NWJudzlnenpxdnQ5cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3kuSo744UIPJjcJUEn/giphy.gif')
        else:
            st.write("Not Approved")
            st.image('https://gifdb.com/images/high/denied-413-x-498-gif-3vfuqyjn5kmy8uto.gif')
if __name__ == '__main__':
    main()
