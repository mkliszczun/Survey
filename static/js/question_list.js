document.addEventListener('DOMContentLoaded', function() {
    const loadQuestions = async () => {
        try {
            const response = await fetch('/admin/api/question_list', {
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

        questions.forEach(question => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${question.id}</td>
                <td>${question.question_content}</td>
                <td>${question.question_type.toUpperCase()}</td>
                <td>
                    <div class="rating-progress">
                        <div class="progress">
                            <div class="progress-bar
                                ${getRatingColor(question.global_rating)}"
                                role="progressbar"
                                style="width: ${question.global_rating * 100}"
                                aria-valuenow="${question.global_rating}"
                                aria-valuemin="0"
                                aria-valuemax="10">
                                ${question.global_rating.toFixed(3)}
                            </div>
                        </div>
                    </div>
                </td>
                <td>${question.choices.length}</td>
                <td>${question.choices.join(', ')}</td>
                <td>
                <button class="btn btn-danger btn-sm" onclick="confirmDelete(${question.id})">
                    Usuń
                </button>
            </td>
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
                <td colspan="6" class="text-danger text-center">
                    ${message}
                </td>
            </tr>
        `;
    };

    loadQuestions();
});

window.confirmDelete = function(questionId) {
    if (confirm("Czy na pewno chcesz usunąć to pytanie?")) {
        deleteQuestion(questionId);
    }
};

const deleteQuestion = async (id) => {
    try {
        const response = await fetch(`/admin/delete_question`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ question_id: id })
        });

        if (!response.ok) throw new Error("Nie udało się usunąć pytania.");

        // refresh list after deleting
        loadQuestions();
    } catch (err) {
        alert("Błąd podczas usuwania pytania: " + err.message);
    }
};