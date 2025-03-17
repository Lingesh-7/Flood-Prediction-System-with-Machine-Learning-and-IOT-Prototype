from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,Optional,Length,URL
import util
from util import DetailsForm
from twilio.rest import Client
import smtplib

import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
num=os.environ.get("num")
tonum=os.environ.get("tonum")

from_email=os.environ.get('EMAIL_KEY')
password=os.environ.get('PASSWORD_KEY')
to_emails=['lingesh.r.official@gmail.com','lingesh91918@gmail.com']


app=Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

@app.route('/',methods=['GET','POST'])
def estimate_price():
    form=DetailsForm()
    if form.validate_on_submit():
        rainfall=form.rainfall.data
        temperature=form.temperature.data
        humidity=form.humidity.data
        river=form.river.data
        water=form.water.data
        elevation=form.elevation.data
        land=int(form.land.data)
        soil=int(form.soil.data)
        response=util.model_predict(rainfall,temperature,humidity,river,water,elevation,land,soil)
        if response==1:
            cilent=Client(account_sid,auth_token)
            message=cilent.messages.create(
                from_="+12673949333",
                to="+917397527233",
                body="""\n\nFLOOD WARNING\n\nRegion: Puducherry and surrounding areas\nRisk Level: High Risk\nExpected Impact: Rising water levels in low-lying areas within the next 3 hours.\nActions to Take:\n    - Move to higher ground immediately.\n    - Avoid crossing flooded roads or rivers.\n    - Keep emergency kits ready.\nFor updates, contact the emergency helpline: 112.\nStay safe and alert!""" )
            print(message.status)

            with smtplib.SMTP('smtp.gmail.com') as c:
                c.starttls()
                c.login(user=from_email,password=password)
                for email in to_emails:
                    c.sendmail(from_addr=from_email,to_addrs=f'{email}',msg="""Subject: FLOOD WARNING \n\nRegion: Puducherry and surrounding areas
                    Risk Level: High Risk
                    Expected Impact: Rising water levels in low-lying areas within the next 3 hours.

                     Actions to Take:
                    - Move to higher ground immediately.
                    - Avoid crossing flooded roads or rivers.
                    - Keep emergency kits ready.

                    For updates, contact the emergency helpline: 112.
                    Stay safe and alert!""")

        return render_template('index.html',form=form,response=response,is_=False)
    return render_template('index.html',form=form,is_=True,response='')



if __name__=='__main__':
    app.run(debug=True)