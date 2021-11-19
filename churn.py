import streamlit as st
import joblib

# loading the trained model
model = joblib.load('rfc.pkl')

# loading the scaler
scaler = joblib.load('scaler.pkl')

@st.cache()
# defining the function which will make the prediction using the data which the user inputs
def make_prediction(balance, creditscore, gender, geography, is_active_member, num_products, tenure, age):
    # Pre-processing user inputs
    if is_active_member == 'Yes':
        Is_Active_Member = 1
    else:
        Is_Active_Member = 0

    if geography == 'France':
        Geography = 0
    elif geography == 'Germany':
        Geography = 1
    else:
        Geography = 2

    if gender == 'Female':
        Gender = 0
    else:
        Gender = 1

    if age >= 18 and age <= 33:
        Age = 0
    elif age >= 34 and age <= 42:
        Age = 1
    elif age >= 43 and age <= 52:
        Age = 2
    elif age >= 53 and age <= 64:
        Age = 3
    else:
        Age = 4

    predict_sample = [balance, creditscore, Gender, Geography, Is_Active_Member, num_products, tenure, Age]
    indexes = [0, 1, -3, -2]
    scaled_sample = scaler.transform([[predict_sample[i] for i in indexes]])[0]

    # Assemble the whole sample to predict
    for i in indexes:
        if i == -3:
            predict_sample[i] = scaled_sample[2]
        elif i == -2:
            predict_sample[i] = scaled_sample[-1]
        else:
            predict_sample[i] = scaled_sample[i]

    # Making predictions
    predictions = model.predict([predict_sample])

    if int(predictions) == 0:
        pred = 'The employee gonna leave, ooof lhemdollah fra3.'
    else:
        pred = 'The client is leaving. An action shall be made.'

    return pred
    
# this is the main function in which we define our webpage
def main():
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:lightblue; padding:13px"> 
    <h1 style ="color:black;text-align:center;">Bank Customer Churn Prediction</h1> 
    </div>
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 

    # following lines create boxes in which user can enter data required to make prediction
    balance = st.number_input("Balance", min_value=0, max_value=None)
    creditscore = st.number_input("Credit Score", min_value=0, max_value=1000)
    gender = st.selectbox("Gender", ('Male', 'Female'))
    geography = st.selectbox("Geography", ('France', 'Spain', 'Germany'))
    is_active_member = st.selectbox("Is he/she an Active member?", ('Yes', 'No'))
    num_products = st.slider("Number of Products", 1, 5)
    tenure = st.slider("Tenure", 1, 10)
    age = st.number_input("Age", min_value=18, max_value=100)
    result = ""

    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"):
        result = make_prediction(balance, creditscore, gender, geography, is_active_member, num_products, tenure, age) 
        st.success('{}'.format(result))

if __name__=='__main__':
    main()