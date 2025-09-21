// static/js/app.js
function analyzeText() {
    const text = document.getElementById('textInput').value;
    const resultDiv = document.getElementById('result');
    const spinner = document.getElementById('loadingSpinner');
    
    // Hide previous result and show loading spinner
    resultDiv.style.display = 'none';
    spinner.style.display = 'block';
    
    if (!text) {
        alert('Пожалуйста, введите текст для анализа');
        spinner.style.display = 'none';
        return;
    }

    fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        // Hide spinner and show result
        spinner.style.display = 'none';
        
        if (data.error) {
            resultDiv.className = 'alert alert-danger';
            resultDiv.innerHTML = `Error: ${data.error}`;
        } else {
            // CHANGE: Use sentiment color classes instead of Bootstrap alerts
            resultDiv.className = `alert result-${data.sentiment.toLowerCase()}`;
            resultDiv.innerHTML = `
                <strong>Текст:</strong> ${data.text}<br>
                <strong>Настроение:</strong> ${data.sentiment}<br>
                <strong>Уверенность:</strong> ${(data.confidence * 100).toFixed(2)}%
            `;
        }
        resultDiv.style.display = 'block';
    })
    .catch(error => {
        // Hide spinner and show error
        spinner.style.display = 'none';
        resultDiv.className = 'alert alert-danger';
        resultDiv.innerHTML = 'Ошибка соединения с сервером';
        resultDiv.style.display = 'block';
    });
}

function analyzeNews() {
    const newsResults = document.getElementById('newsResults');
    newsResults.innerHTML = '<div class="text-center"><div class="spinner-border text-info"></div><p>Загружаем новости...</p></div>';
    
    fetch('/api/russian-news')
        .then(response => response.json())
        .then(news => {
            let html = '<h4>Результаты анализа:</h4>';
            news.forEach(item => {
                // CHANGE: Use sentiment color classes instead of Bootstrap alerts
                html += `
                    <div class="alert result-${item.sentiment.toLowerCase()} mb-2">
                        <strong>${item.headline}</strong><br>
                        Источник: ${item.source} | 
                        Настроение: ${item.sentiment} | 
                        Уверенность: ${item.confidence}%
                    </div>
                `;
            });
            newsResults.innerHTML = html;
        })
        .catch(error => {
            newsResults.innerHTML = '<div class="alert alert-danger">Ошибка загрузки новостей</div>';
        });
}