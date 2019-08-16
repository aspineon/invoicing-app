from flask import Flask, render_template, url_for, request
from fpdf import FPDF

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

	number = request.form['invoice_number']
	date = request.form['invoice_date']
	service = request.form['service_delivered']

	data = [number, date, service]

	pdf = FPDF(orientation='P', unit='mm', format='A4')
	pdf.add_page()
	pdf.set_font('Arial', size=12)

	for item in data:
		pdf.cell(0, 10, str(item), 0, 1)

	pdf.output('test.pdf', 'F')

	return render_template('submit.html')

if __name__=='__main__':
	app.run(debug=True)