// Wrap the code in a DOMContentLoaded event listener to ensure the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Get references to the HTML elements
    const filesInput = document.getElementById('files');
    const hasHeaderCheckbox = document.getElementById('hasHeader');
    const fileTypeSelect = document.getElementById('fileType');
    const loadingDiv = document.getElementById('loading');
    const downloadLink = document.getElementById('downloadLink');

    // Attach an event listener to the button
    document.getElementById('mergeButton').addEventListener('click', mergeFiles);

    async function mergeFiles() {
        // Reset UI elements
        loadingDiv.style.display = 'none';
        downloadLink.style.display = 'none';
    
        // Check if at least one file is selected
        if (filesInput.files.length === 0) {
            console.error('Please select at least one file.');
            alert('Please select at least one file.');
            return;
        }
    
        // Prepare form data
        const formData = new FormData();
        for (let i = 0; i < filesInput.files.length; i++) {
            formData.append('files', filesInput.files[i]);
        }
        formData.append('has_header', hasHeaderCheckbox.checked);
        formData.append('file_type', fileTypeSelect.value);
    
        // Show loading message
        loadingDiv.style.display = 'block';
    
        try {
            // Make a POST request to the Flask API
            const response = await fetch('http://65.2.10.13:8000/merge_files', {
                method: 'POST',
                body: formData
            });
    
            // Handle the response
            if (response.ok) {
                // Hide loading message
                loadingDiv.style.display = 'none';
    
                // Get the blob data
                const blob = await response.blob();
                const blobUrl = URL.createObjectURL(blob);
    
                // Display success message and download button using SweetAlert2
                Swal.fire({
                    icon: 'success',
                    title: 'Files merged successfully!',
                    showCancelButton: true,
                    confirmButtonText: 'Download Merged File',
                    cancelButtonText: 'Close',
                    allowOutsideClick: false
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Trigger download
                        const a = document.createElement('a');
                        a.href = blobUrl;
                        a.download = 'merged_data.' + fileTypeSelect.value;
                        a.click();
                    }
                });
            } else {
                // Handle error
                const data = await response.json();
                console.error('Error:', data.error);
                alert('Error: ' + data.error);
            }
        } catch (error) {
            // Handle network or other errors
            console.error('An error occurred:', error.message);
            alert('An error occurred: ' + error.message);
        }
    }
}
)