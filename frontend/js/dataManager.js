// js/dataManager.js

const workDataState = {
    id_to_tool_name: {}, // Словарь инструментов {id: name}, которые нужно найти
    tool_name_to_id: {}, // Словарь инструментов {name: id}, которые нужно найти
    photos: [], // Массив фото {photo_id, photo_base64}
    approvedBoxes: [], // Массив подтвержденных рамок
    scanResults: [], // Массив результатов сканирования {photo_id, boxes: [{bbox, tool_id, tool_name, status}]}
};

/**
 * Загружает и обрабатывает данные о работе.
 * @param {string|number} workId - ID работы.
 * @param {string} stage - Текущий этап.
 */
async function loadAndProcessWorkData(workId, stage) {
    console.log(`Загружаю данные для работы ${workId} на этапе ${stage}...`);
    const data = await getWorkData(workId, stage);

    workDataState.id_to_tool_name = data.tid_to_tname || {};
    workDataState.tool_name_to_id = {};
    for (const [tid, tname] of Object.entries(workDataState.id_to_tool_name)) {
        workDataState.tool_name_to_id[tname] = tid;
    }

    workDataState.photos = data.photo_data || [];
    workDataState.approvedBoxes = data.approved_boxes || [];

    console.log('Данные успешно загружены и обработаны:', workDataState);
}

/**
 * Обрабатывает и сохраняет данные, полученные после сканирования.
 * @param {object} scanData - Данные, полученные от API scanTable.
 */
function processScanData(scanData) {
    console.log('Обработка данных сканирования:', scanData);

    workDataState.scanResults.push(scanData);

    if (!workDataState.photos.some((p) => p.photo_id === scanData.photo_id)) {
        workDataState.photos.push({
            photo_id: scanData.photo_id, photo_base64: scanData.photo_base64,
        });
    }
}

/**
 * Обновляет локальное состояние после подтверждения инструмента.
 * @param {object} approvedBox - Подтвержденный объект бокса, включая tool_id и tool_name.
 */
function updateStateAfterApproval(approvedBox) {
    workDataState.approvedBoxes.push(approvedBox);

    const toolId = approvedBox.tool_id.toString();
    const toolName = approvedBox.tool_name;

    delete workDataState.id_to_tool_name[toolId];
    delete workDataState.tool_name_to_id[toolName];

    console.log('Состояние обновлено после подтверждения:', workDataState);
}
