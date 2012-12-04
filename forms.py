from flask.ext.wtf import Form, TextField, Email, Required, \
						  Length, EqualTo, FloatField, PasswordField, \
						  HiddenField, NumberRange

class RegForm(Form):
	name = TextField("Enter Your Name", validators=[Required()])
	email = TextField("Email", validators=[Required(), Email()])
	password = PasswordField("Password", validators=[Required(), Length(min=4)])
	password_confirm = PasswordField("Confirm Password", 
								 validators=[Required(),
								 	         Length(min=4),
										     EqualTo("password")])
	lat = HiddenField("My Latitude", validators=[Length(min=0)])
	long = HiddenField("My Longitude", validators=[Length(min=0)])