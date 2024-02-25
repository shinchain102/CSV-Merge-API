from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def merge_files(files, has_header):
    merged_df = pd.DataFrame()
    for file in files:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file, header=0 if has_header else None)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file, header=0 if has_header else None)
        else:
            return None, "Unsupported file format"

        merged_df = pd.concat([merged_df, df], ignore_index=True)

    return merged_df, None

@app.route('/merge_files', methods=['POST'])
def merge_files_api():
    try:
        files = request.files.getlist('files')
        has_header = bool(request.form.get('has_header', False))

        if not files:
            return jsonify({'error': 'No files uploaded'}), 400

        merged_df, error = merge_files(files, has_header)

        if error:
            return jsonify({'error': error}), 400

        # Convert merged data to CSV format
        csv_data = merged_df.to_csv(index=False)
        
        # Create a BytesIO buffer to store the CSV data
        output_buffer = BytesIO()
        output_buffer.write(csv_data.encode())
        output_buffer.seek(0)

        # Return the CSV file as a downloadable attachment
        return send_file(output_buffer, as_attachment=True, download_name='merged_data.csv', mimetype='text/csv')

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
