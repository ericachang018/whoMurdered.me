# from flask.ext.wtf import Form
# from wtforms import TextFeild, BooleanFeild, Length, FloatFeild, HiddenFeild
# from wtforms.validators import Required, Email, PasswordFeild, NumberRange, EqualTo
from wtforms import Form, BooleanField, TextField, PasswordField, HiddenField, FloatField
from wtforms.validators import Length, Required, EqualTo, Email
class RegForm(Form):
	name = TextField("Enter Your Name", validators=[Required()])
	email = TextField("Email", validators=[Required(), Email()])
	password = PasswordField("Password", validators=[Required(), Length(min=4)])
	password_confirm = PasswordField("Confirm Password", 
								 validators=[Required(),
								 	         Length(min=4),
										     EqualTo("password")])
	lat = HiddenField("My Latitude", validators=[Required()])
	long = HiddenField("My Longitude", validators=[Required()])
