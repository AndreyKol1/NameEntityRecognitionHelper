document.getElementById('test-form').addEventListener('submit', async function(e) {
    e.preventDefault(); 
    const sentence = document.getElementById('sentence').value;

    const formData = new FormData();
    formData.append('sentence', sentence);
    try {
        const response = await fetch('/test', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json(); 
        console.log(result)
        const resultContainer = document.getElementById('result-container');
        const resultList = document.getElementById('result-list');

        resultList.innerHTML = '';
        result.data.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${item.word}</strong>: ${item.entity}`;
            resultList.appendChild(li);
        });

        resultContainer.style.display = 'block';
        document.getElementById('error-container').style.display = 'none';

    } catch (err) {
        document.getElementById('error-message').textContent = err.toString();
        document.getElementById('error-container').style.display = 'block';
        document.getElementById('result-container').style.display = 'none';
    }
});