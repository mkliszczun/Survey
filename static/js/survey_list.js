document.addEventListener('DOMContentLoaded', function() {
    const loadSurveys = async () => {
        try {
            const response = await fetch('/admin/api/survey_list', {
                method: 'GET',
                credentials: 'include'
            });

            const result = await response.json();

            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                    return;
                }
                throw new Error(`Błąd HTTP! status: ${response.status}`);
            }

            renderSurveys(result.data);

        } catch (error) {
            console.error('Błąd ładowania danych:', error);
            showError(error.message);
        }
    };

    const renderSurveys = (surveys) => {
        const tbody = document.getElementById('survey-list');
        tbody.innerHTML = '';

        if (!Array.isArray(surveys)) {
            throw new Error('Nieprawidłowy format danych ankiet');
        }

        surveys.forEach(survey => {
            const row = document.createElement('tr');

            const dateObj = survey.submission_date ?
                new Date(survey.submission_date) : // Dla stringa w formacie ISO
                new Date();

            row.innerHTML = `
                <td>${survey.id}</td>
                <td>${dateObj.toLocaleDateString()}</td>
                <td>${survey.choices?.length || 0}</td>
                <td>User #${survey.owner_id}</td>
            `;
            tbody.appendChild(row);
        });
    };

    const showError = (message) => {
        const tbody = document.getElementById('survey-list');
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-danger text-center">
                    ${message}
                </td>
            </tr>
        `;
    };

    loadSurveys();
});