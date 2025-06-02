document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const messageElement = document.getElementById('message');

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            messageElement.textContent = result.message;
            messageElement.className = 'message success';
        } else {
            messageElement.textContent = `Error: ${result.detail}`;
            messageElement.className = 'message error';
        }
    } catch (error) {
        messageElement.textContent = `Error: ${error.message}`;
        messageElement.className = 'message error';
    }
});

document.getElementById('listFilesBtn').addEventListener('click', async () => {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';

    try {
        const response = await fetch('/files');
        const result = await response.json();

        result.files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <i class="fas fa-file-alt"></i>
                <a href="#" onclick="downloadFile('${file}')">${file}</a>
            `;
            fileList.appendChild(fileItem);
        });
    } catch (error) {
        alert('Error fetching file list');
    }
});

async function downloadFile(fileName) {
    try {
        const response = await fetch(`/download/${fileName}`);
        const result = await response.json();
        window.open(result.download_url, '_blank');
    } catch (error) {
        alert('Error generating download link');
    }
}
