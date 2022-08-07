from flask import Flask, request, url_for, render_template
import pyotp
from sendgrid import Mail, Content, SendGridAPIClient


app = Flask(__name__)
otp_gen = pyotp.TOTP(s="base32secret3232", digits=4, interval=300)

def OTPVerification_mail(reciepient, code):
    template = f""" 
       confirmation template would be added here along with the OTP to be received by the user , depending on what style of template you would want to use.
     """   
    message = Mail(
       from_email = 'sender’s email',
       to_emails = reciepient,
       subject = 'MAil title that would be seen by user',
       #html_content = f'<strong>Phrase backed Up successfully </strong>',
       html_content = Content("text/html", content=template))
    try:
       sg = SendGridAPIClient(api_key="sendgrid api key")
       response = sg.send(message)
       print(response.status_code)
    except Exception as e:
       print(str(e))
@app.route("/emailVerificationViaOtp", methods=["POST"])
def verify_email():
    if request.method == "POST":
        email = request.json.get("email")
        otp = request.json.get("otp_code")
        
        verify_otp = otp_gen.verify(otp)
        if verify_otp == True:
            return {'message':"Email Verified"}, 200
        else:
            return {"message":"OTP Expired"}, 400
@app.route("/emailVerificationOtp", methods=["POST"])
def otp_verify():
   if request.method == "POST":
       #send mailto user with the otp
       email = request.json.get("email")
       otp = otp_gen.now()
       OTPVerification_mail(email, otp)
       return {"message":"OTP sent to mail"}, 200
if __name__ == "__main__":
    app.run()