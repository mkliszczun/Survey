document.addEventListener('DOMContentLoaded', function () {
    const loadQuestions = async () => {
        try {
            const response = await fetch('/api/user_top_questions', {
                method: 'GET',
                credentials: 'include'
            });

            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                    return;
                }
                throw new Error(`Błąd HTTP! status: ${response.status}`);
            }

            const questions = await response.json();
            renderQuestions(questions.data);
        } catch (error) {
            console.error('Błąd ładowania danych:', error);
            showError(error.message);
        }
    };

    const renderQuestions = (questions) => {
        const tbody = document.getElementById('question-list');
        tbody.innerHTML = '';

        if (!questions.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted">
                        Brak pytań do wyświetlenia.
                    </td>
                </tr>
            `;
            return;
        }

        questions.forEach(question => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${question.id}</td>
                <td>${question.question_content}</td>
                <td>${question.question_type.toUpperCase()}</td>
                <td>
                    <div class="progress">
                        <div class="progress-bar ${getRatingColor(question.global_rating)}"
                             role="progressbar"
                             style="width: ${(question.global_rating / 5 * 100).toFixed(1)}"
                             aria-valuenow="${question.global_rating.toFixed(3)}"
                             aria-valuemin="0" aria-valuemax="5">
                             ${question.global_rating.toFixed(3)}
                        </div>
                    </div>
                </td>
                <td>${question.rating.toFixed(3)}</td>
                <td>${question.choices.length}</td>
                <td>${question.choices.join(', ')}</td>
            `;
            tbody.appendChild(row);
        });
    };

    const getRatingColor = (rating) => {
        if (rating >= 0.8) return 'bg-success';
        if (rating >= 0.5) return 'bg-warning';
        return 'bg-danger';
    };

    const showError = (message) => {
        const tbody = document.getElementById('question-list');
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-danger text-center">
                    ${message}
                </td>
            </tr>
        `;
    };

    loadQuestions();
});
