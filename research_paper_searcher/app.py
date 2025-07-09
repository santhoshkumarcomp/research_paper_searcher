# app.py

from flask import Flask, request, Response
from pubmed.fetch import get_pubmed_csv  

app = Flask(__name__)

@app.route('/get-data')
def get_data():
    search = request.args.get('search')
    csv_data = get_pubmed_csv(search)

    if csv_data:
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=report.csv"}
        )
    else:
        return {"error": "Failed to fetch data"}, 500

if __name__ == '__main__':
    app.run(debug=True)
