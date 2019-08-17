import os
from flask import Flask, render_template, url_for, request
from fpdf import FPDF
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=["GET", "POST"])
def index():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

	number = request.form['invoice_number']
	date = request.form['invoice_date']
	service = request.form['service_delivered']
	file = request.files['file']
	file.save(secure_filename(file.filename))

	data = [number, date, service]

	class PDF(FPDF):
		def header(self):
			# Logo
			self.image(file.filename, 10, 8, 33)
			# Arial bold 15
			self.set_font('Arial', 'B', 15)
			# Move to the right
			self.cell(80)
			# Title
			self.cell(30, 10, 'Faktura: ' + str(number), 1, 0, 'C')
			# Line break
			self.ln(20)

	pdf = FPDF(orientation='P', unit='mm', format='A4')
	pdf.add_page()
	pdf.set_font('Arial', size=12)

	for item in data:
		pdf.cell(0, 10, str(item), 0, 1)

	pdf.output(str(number) + '.pdf', 'F')

	return render_template('submit.html')

if __name__=='__main__':
	app.run(debug=True)