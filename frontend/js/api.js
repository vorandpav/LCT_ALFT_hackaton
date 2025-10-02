// js/api.js

var API_BASE_URL = 'http://localhost:9002';

/**
 * Авторизация пользователя.
 * @param {string|number} userId - ID пользователя.
 * @param {string|number} workId - ID работы.
 * @returns {Promise<object>} - Данные пользователя и работы.
 */
async function authorize(userId, workId) {
    const response = await fetch(`${API_BASE_URL}/users/authorize/${userId}/work/${workId}`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const detail = errorData ? errorData.detail : response.statusText;
        throw new Error(`Ошибка авторизации: ${detail}`);
    }
    return response.json();
}

/**
 *  Завершение текущего этапа работы.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап.
 * @returns {Promise<object>} - Новый этап работы.
 */
async function completeStage(workId, stage) {
    const response = await fetch(`${API_BASE_URL}/works/${workId}/${stage}/complete`, {
        method: 'POST',
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const detail = errorData ? errorData.detail : 'Не удалось завершить этап';
        throw new Error(detail);
    }
    return response.json();
}

/**
 * Загрузка всех данных по работе на данном этапе.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап.
 * @returns {Promise<object>} - Данные о работе (инструменты, фото, подтвержденные боксы).
 */
async function getWorkData(workId, stage) {
    const response = await fetch(`${API_BASE_URL}/works/${workId}/${stage}`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const detail = errorData ? errorData.detail : 'Не удалось загрузить данные о работе';
        throw new Error(detail);
    }
    return response.json();
}

/**
 * Запрашивает полные данные по работе для отчёта.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап (GIVING или GETTING).
 * @returns {Promise<object>} - Данные по этапам GIVING и GETTING.
 */
async function getReportData(workId, stage) {
    const response = await fetch(`${API_BASE_URL}/works/${workId}/${stage}/report`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const detail = errorData ? errorData.detail : 'Не удалось загрузить данные о работе';
        throw new Error(detail);
    }
    return response.json();
}

/**
 * Запускает один цикл сканирования на сервере.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап.
 * @returns {Promise<object>} - Результат сканирования (фото, рамки, совет).
 */
async function scanTable(workId, stage) {
    const response = await fetch(`${API_BASE_URL}/works/${workId}/${stage}/scan`, {
        method: 'POST',
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const detail = errorData ? errorData.detail : 'Не удалось выполнить сканирование';
        throw new Error(detail);
    }
    return response.json();
}

/**
 * Отправляет подтвержденный бокс на сервер.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап.
 * @param {object} boxData - Данные о подтверждаемом боксе.
 * @returns {Promise<object>} - Статус операции.
 */
async function approveBox(workId, stage, boxData) {
    const response = await fetch(`${API_BASE_URL}/works/${workId}/${stage}/approve`, {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(boxData),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const detail = errorData ? errorData.detail : 'Не удалось подтвердить инструмент';
        throw new Error(detail);
    }
    return response.json();
}

/**
 * Отправляет запрос на завершение текущего этапа работы.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап.
 * @returns {Promise<object>} - Результат операции ({ok: boolean, new_stage?: string, error?: string}).
 */
async function completeWorkStage(workId, stage) {
    const response = await fetch(`${API_BASE_URL}/works/${workId}/${stage}/complete`, {
        method: 'POST',
    });
    return response.json();
}

/**
 * Отправляет запрос о переводе работы в состояние ошибки.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап.
 * @returns {Promise<object>} - Результат операции ({ok: boolean, new_stage: "ERROR"}).
 */
async function reportErrorStage(workId, stage) {
    const response = await fetch(`${API_BASE_URL}/works/${workId}/${stage}/error`, {
        method: 'POST',
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const detail = errorData ? errorData.detail : 'Не удалось сообщить об ошибке';
        throw new Error(detail);
    }
    return response.json();
}
