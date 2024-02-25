from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO
import os

app = Flask(__name__)

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

        merged_df, error = merge_files(files, has_header)

        if error:
            return jsonify({'error': error}), 400

        output_buffer = BytesIO()
        merged_df.to_csv(output_buffer, index=False)
        output_buffer.seek(0)

        return jsonify({'result': output_buffer.read().decode()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
