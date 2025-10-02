// js/login.js

document.addEventListener('DOMContentLoaded', () => {
    const workIdInput = document.getElementById('work-id');
    const userIdInput = document.getElementById('user-id');
    const workButton = document.getElementById('work-button');
    const reportButton = document.getElementById('report-button');
    const loginStatus = document.getElementById('login-status');

    workButton.addEventListener('click', async () => {
        const workId = workIdInput.value.trim();
        const userId = userIdInput.value.trim();

        if (!workId || !userId) {
            loginStatus.textContent = 'Пожалуйста, введите ID работы и ID пользователя.';
            return;
        }

        try {
            loginStatus.textContent = 'Проверка...';
            const initialData = await authorize(userId, workId);

            if (['PUBLISHED', 'IN_WORK', 'GIVING', 'GETTING'].includes(initialData.stage)) {
                loginStatus.textContent = `Успешно! Текущий этап: '${initialData.stage}'. Перенаправление...`;
                sessionStorage.setItem('initialData', JSON.stringify(initialData));
                window.location.href = `main.html?workId=${workId}&userId=${userId}`;
            } else {
                loginStatus.textContent = `Текущий этап '${initialData.stage}' не предполагает активной работы.`;
            }
        } catch (error) {
            loginStatus.textContent = `Ошибка: ${error.message}`;
        }
    });

    reportButton.addEventListener('click', async () => {
        const workId = workIdInput.value.trim();
        const userId = userIdInput.value.trim();

        if (!workId || !userId) {
            loginStatus.textContent = 'Пожалуйста, введите ID работы и ID пользователя.';
            return;
        }

        try {
            loginStatus.textContent = 'Проверка...';
            const initialData = await authorize(userId, workId);
            loginStatus.textContent = 'Успешно! Перенаправление на страницу отчета...';
            sessionStorage.setItem('initialData', JSON.stringify(initialData));
            window.location.href = `report.html?workId=${workId}&userId=${userId}`;
        } catch (error) {
            loginStatus.textContent = `Ошибка: ${error.message}`;
        }
    });
});
