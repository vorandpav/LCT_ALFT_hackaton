// js/app.js

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const workId = urlParams.get('workId');
    const userId = urlParams.get('userId');
    let currentStage = null;

    const info = {
        userId: document.getElementById('info-user-id'),
        userName: document.getElementById('info-user-name'),
        powers: document.getElementById('info-powers'),
        workId: document.getElementById('info-work-id'),
        stage: document.getElementById('info-stage'),
    };

    const imageModal = document.getElementById('image-modal');
    const modalImage = document.getElementById('modal-image');
    const modalCloseButton = document.getElementById('modal-close-button');
    const scanButton = document.getElementById('scan-button');
    const completeWorkButton = document.getElementById('complete-work-button');
    const errorButton = document.getElementById('error-button');

    function displayInfo(label, value, element) {
        element.innerHTML = `<span class="label">${label}:</span> ${value}`;
    }

    function openImageModal(imgSrc) {
        modalImage.src = imgSrc;
        imageModal.classList.remove('hidden');
    }

    function closeImageModal() {
        imageModal.classList.add('hidden');
    }

    modalCloseButton.addEventListener('click', closeImageModal);
    imageModal.addEventListener('click', (e) => {
        if (e.target === imageModal) {
            closeImageModal();
        }
    });

    scanButton.addEventListener('click', async () => {
        scanButton.disabled = true;
        scanButton.textContent = 'Сканирование...';
        try {
            const scanData = await scanTable(workId, currentStage);
            processScanData(scanData);
            await renderLastScanRows();
        } catch (error) {
            alert(`Ошибка сканирования: ${error.message}`);
        } finally {
            scanButton.disabled = false;
            scanButton.textContent = 'Сканировать';
        }
    });

    completeWorkButton.addEventListener('click', async () => {
        if (!confirm('Вы уверены, что хотите завершить текущий этап?')) {
            return;
        }

        completeWorkButton.disabled = true;
        try {
            const result = await completeWorkStage(workId, currentStage);

            if (result.ok) {
                alert(`Этап '${currentStage}' успешно завершен. Новый этап: '${result.new_stage}'.`);
                currentStage = result.new_stage;
                window.location.href = 'index.html';
            } else {
                alert(`Не удалось завершить этап: ${result.error}`);
            }
        } catch (error) {
            alert(`Критическая ошибка при завершении этапа: ${error.message}`);
        } finally {
            completeWorkButton.disabled = false;
        }
    });

    errorButton.addEventListener('click', async () => {
        if (!confirm('Вы уверены, что хотите перевести работу в состояние "ОШИБКА"? Это действие необратимо.')) {
            return;
        }

        errorButton.disabled = true;
        try {
            const result = await reportErrorStage(workId, currentStage);
            if (result.ok) {
                alert('Работа успешно переведена в состояние ошибки.');
                currentStage = result.new_stage;
                displayInfo('Stage', currentStage, info.stage);
                window.location.href = 'index.html';
            }
        } catch (error) {
            alert(`Не удалось сообщить об ошибке: ${error.message}`);
            errorButton.disabled = false;
        }
    });

    async function initializeApp() {
        if (!workId || !userId) {
            alert('ID работы или ID пользователя не найдены. Возвращаемся на страницу входа.');
            window.location.href = 'index.html';
            return;
        }

        const initialDataString = sessionStorage.getItem('initialData');
        if (!initialDataString) {
            alert('Страница обновлена, пожалуйста, войдите заново.');
            window.location.href = 'index.html';
            return;
        }

        sessionStorage.removeItem('initialData');
        const initialData = JSON.parse(initialDataString);
        currentStage = initialData.stage;

        if (currentStage === 'PUBLISHED' || currentStage === 'IN_WORK') {
            try {
                console.log(`Завершение этапа '${currentStage}'...`);
                const completeData = await completeStage(workId, currentStage);
                if (completeData.ok) {
                    currentStage = completeData.new_stage;
                    console.log('Новый этап:', currentStage);
                }
            } catch (error) {
                alert(`Не удалось автоматически завершить этап 'PUBLISHED': ${error.message}`);
            }
        }

        displayInfo('User ID', userId, info.userId);
        displayInfo('User Name', initialData.user_name, info.userName);
        displayInfo('Powers', initialData.powers, info.powers);
        displayInfo('Work ID', workId, info.workId);
        displayInfo('Stage', currentStage, info.stage);

        setContext(workId, currentStage, {openImageModal: openImageModal});

        try {
            await loadAndProcessWorkData(workId, currentStage);
            await renderApprovedRows();
        } catch (error) {
            alert(`Не удалось загрузить данные о работе: ${error.message}`);
        }

        initializeTableEventListeners();
    }

    initializeApp();
});
