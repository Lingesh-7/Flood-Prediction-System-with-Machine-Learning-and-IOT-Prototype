import json
import pickle
# import sklearn
from sklearn.ensemble import RandomForestClassifier
# import tensorflow as tf
# from tensorflow import keras
import numpy as np
from flask_wtf import FlaskForm
from sklearn.preprocessing import StandardScaler
from wtforms.validators import DataRequired,Optional,Length,URL
from wtforms import StringField, SubmitField,SelectField,IntegerField,FloatField


model=None
data_columns=None



def scaling(values):
    scaler=StandardScaler()
    # yp=model.predict(scaler.fit_transform(values))
    return scaler.fit_transform([values])


def load_columns():
    global data_columns
    with open(r'prototype\model_\columns.json','r') as f:
        data_columns=json.load(f)['data_columns']

def load_model():
    global model
    with open(r'prototype\model_\fp_ml_rf.pickle','rb') as f:
        model=pickle.load(f)


def model_predict(rainfall, temperature, humidity, river, water, elevation, land, soil):
    load_columns()
    load_model()
    x=np.zeros(len(data_columns))
    x[0]=rainfall
    x[1]=temperature
    x[2]=humidity
    x[3]=river
    x[4]=water
    x[5]=elevation
    x[6]=land
    x[7]=soil
    return round(model.predict(scaling(x))[0],2)

class DetailsForm(FlaskForm):
    rainfall=FloatField('Rainfall(mm)',validators=[DataRequired()])
    temperature=FloatField('Temperature(C)',validators=[DataRequired()])
    humidity=FloatField('Humidity(%)',validators=[DataRequired()])
    river=FloatField('River Discharge (m³/s)',validators=[DataRequired()])
    water=FloatField('Water Level (m)',validators=[DataRequired()])
    elevation=FloatField('Elevation (m)',validators=[DataRequired()])
    land=SelectField(label='Land Cover',validators=[DataRequired()],choices=['0',"1","2","3","4"])
    soil=SelectField(label='soil type',validators=[DataRequired()],choices=['0',"1","2","3"])
    submit = SubmitField('Submit')
    


# if __name__=='__main__':
#     load_columns()
#     # print(get_location_names())
#     print(model_predict(2.18999493e+02, 3.41443371e+01, 4.39129633e+01, 4.23618289e+03,
#        7.41555203e+00, 3.77465433e+02, 4.00000000e+00, 0.00000000e+00))
#     # print(model_estimate_price('1st phase jp nagar',1000,2,2))
#     # print(model_estimate_price('kalhalli',1000,2,2))