let currentQuestionIndex = 0;
let answers = {};
let questions = [];

console.log("Survey script loaded");

async function initializeSurvey() {
    try {
        const response = await fetch('/api/questions');
        questions = await response.json();
        renderQuestion(currentQuestionIndex);
        updateProgress();
    } catch (error) {
        alert('Błąd ładowania pytań!');
    }
}

function renderQuestion(index) {
    const container = document.getElementById('questionsContainer');
    if (!container) return;

    const question = questions[index];
    const questionHTML = `
        <div class="question-card ${index === 0 ? 'active' : ''}">
            <div class="question-text">${question.text}</div>
            ${renderQuestionInput(question)}
        </div>
    `;

    container.insertAdjacentHTML('beforeend', questionHTML);

    requestAnimationFrame(() => {
        const activeQuestion = container.lastElementChild;
        activeQuestion.classList.add('active');
    });
}

function renderQuestionInput(question) {
    if (question.type === 'radio') {
        return `<div class="radio-group">${
            question.options.map(opt => `
                <label class="radio-option">
                    <input type="radio" name="q${question.id}" value="${opt}">
                    ${opt}
                </label>`
        ).join('')}</div>`;
    }
    return `<textarea class="text-answer" name="q${question.id}"></textarea>`;
}

document.getElementById('nextBtn').addEventListener('click', async () => {
    const currentQuestion = document.querySelector('.question-card.active');
    if (!currentQuestion) return;

    const answer = {};
    currentQuestion.querySelectorAll('input, textarea').forEach(input => {
        if ((input.type === 'radio' && input.checked) || input.tagName === 'TEXTAREA') {
            answer[input.name] = input.value;
        }
    });

    if (Object.keys(answer).length === 0) {
        alert('Proszę odpowiedzieć na pytanie!');
        return;
    }

    answers = {...answers, ...answer};
    currentQuestion.classList.add('exit');

    setTimeout(() => {
        currentQuestion.remove();
        currentQuestionIndex++;
        currentQuestionIndex < questions.length
            ? renderQuestion(currentQuestionIndex)
            : submitSurvey();
        updateProgress();
    }, 500);
});

document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderQuestion(currentQuestionIndex);
        updateProgress();
    }
});

function updateProgress() {
    const progress = (currentQuestionIndex + 1)/questions.length * 100;
    document.querySelector('.progress').style.width = `${progress}%`;
    document.getElementById('currentQuestion').textContent =
        `${currentQuestionIndex + 1}/${questions.length}`;
}

async function submitSurvey() {
    try {
        await fetch('/api/submit-survey', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(answers)
        });
        window.location.href = '/dashboard';
    } catch (error) {
        alert('Błąd przesyłania odpowiedzi!');
    }
}

// Start
initializeSurvey();
