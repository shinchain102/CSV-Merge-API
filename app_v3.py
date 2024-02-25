from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO
import os
import logging
from flask_cors import CORS

# Add more detailed logging configuration
logging.basicConfig(filename='app.log', level=logging.INFO)


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in  this Flask app
def merge_files(files, has_header):
    try:
        merged_df = pd.DataFrame()
        for file in files:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file, header=0 if has_header else None)
            elif file.filename.endswith('.xlsx'):
                df = pd.read_excel(file, header=0 if has_header else None)
            else:
                raise ValueError("Unsupported file format")

            merged_df = pd.concat([merged_df, df], ignore_index=True)

        return merged_df, None
    except Exception as e:
        # Log the error with more details
        logging.error(f"Error in merge_files: {str(e)}")
        return None, str(e)

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
        # Log the error with more details
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request'}), 500

if __name__ == '__main__':
    # Use environment variables or a configuration file for host and port
    app.run(host='0.0.0.0', port=5000, debug=False)