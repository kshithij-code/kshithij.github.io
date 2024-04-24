import datetime

from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    date=datetime.date.today().strftime("%d/%m/%Y")
    name = request.form['name']
    roll_number = request.form['roll_number']
    grade = request.form['grade']
    branch=request.form['branch']
    course = request.form['course']

    template_path = "input//template.pdf"

    output_filename = f"{name}_report_with_template.pdf"

    template_pdf = PdfReader(template_path)
    output_pdf = PdfWriter()

    packet = io.BytesIO()
    pdf = canvas.Canvas(packet)

    pdf.setFont("Courier", 12)
    pdf.drawString(300, 580, f"{name}")
    pdf.drawString(300, 540, f"{roll_number}")
    pdf.drawString(300, 500, f"{branch}")
    pdf.drawString(300, 460, f"{grade}")
    pdf.drawString(200, 690, f"{course}")
    pdf.drawString(400, 690, f"{date}")
    pdf.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    template_pdf.pages[0].merge_page(new_pdf.pages[0])
    output_pdf.add_page(template_pdf.pages[0])

    with open(output_filename, "wb") as output_file:
        output_pdf.write(output_file)
    output_file.close()
    print(output_filename)
    return send_file(output_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=Flase,host="0.0.0.0")

