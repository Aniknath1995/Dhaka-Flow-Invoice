from flask import Flask, render_template, request, make_response, redirect, url_for
import pdfkit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('invoice_form.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    form = request.form
    # Extract and prepare data from form
    amount = float(form['amount'])
    vat_percent = float(form['vat_percent'])
    vat_amount = amount * vat_percent / 100
    total_amount = amount + vat_amount

    data = {
        "invoice_no": form['invoice_no'],
        "date": form['date'],
        "client_name": form['client_name'],
        "client_address": form['client_address'],
        "item": form['item'],
        "amount": amount,
        "vat_percent": vat_percent,
        "vat_amount": vat_amount,
        "total_amount": total_amount,
        "amount_words": form['amount_words'],
        "bank_details": {
            "account_name": form['account_name'],
            "account_number": form['account_number'],
            "bank": form['bank'],
            "branch": form['branch'],
            "swift": form['swift'],
            "phone": form['phone']
        },
        "signatory": form['signatory']
    }

    html = render_template("invoice_template.html", data=data)
    pdf = pdfkit.from_string(html, False)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename={form['invoice_no']}.pdf"
    return response

if __name__ == "__main__":
    app.run(debug=True)
