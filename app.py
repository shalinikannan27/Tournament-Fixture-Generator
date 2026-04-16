from flask import Flask, render_template, request, send_file, jsonify
from generator.bracket import generate_bracket_data, get_bracket_size, get_round_names
from generator.excel_export import generate_excel
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    num_players = int(data.get('nplayers', 16))
    bracket_data = generate_bracket_data(num_players)
    return jsonify(bracket_data)

@app.route('/export', methods=['POST'])
def export_excel():
    # Receive the current state of the table from the frontend
    # This includes edits made by the user
    data = request.json
    
    excel_buffer = generate_excel(data)
    
    filename = f"{data.get('tname', 'tournament').replace(' ', '_')}_fixtures.xlsx"
    
    return send_file(
        excel_buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
