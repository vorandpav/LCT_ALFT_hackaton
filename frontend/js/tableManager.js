// js/tableManager.js

let currentWorkId;
let currentWorkStage;
let openImageModalCallback;

function setContext(workId, stage, callbacks) {
    currentWorkId = workId;
    currentWorkStage = stage;
    openImageModalCallback = callbacks.openImageModal;
}

const tableBody = document.getElementById('tools-table-body');

async function renderApprovedRows() {
    for (const box of workDataState.approvedBoxes) {
        const photo = workDataState.photos.find((p) => p.photo_id === box.photo_id);
        if (!photo) continue;

        const thumbnailUrl = await cropAndDrawBox(photo.photo_base64, box.bbox, 1.2);

        const row = document.createElement('tr');
        row.innerHTML = `
            <td><img src="${thumbnailUrl}" alt="Инструмент" class="tool-thumbnail" style="cursor: pointer;"></td>
            <td>${box.tool_name}</td>
            <td>${box.tool_id}</td>
            <td></td>
            <td><span class="status-confirmed">Подтверждено</span></td>
        `;
        tableBody.appendChild(row);

        const thumbnailImg = row.querySelector('.tool-thumbnail');
        thumbnailImg.addEventListener('click', async () => {
            const fullImageWithBox = await drawImageWithBox(photo.photo_base64, box.bbox);
            openImageModalCallback(fullImageWithBox);
        });
    }
}

async function renderLastScanRows() {
    const scanIndex = workDataState.scanResults.length - 1;
    if (scanIndex < 0) return;

    const scanResult = workDataState.scanResults[scanIndex];

    for (const [boxIndex, box] of scanResult.boxes.entries()) {
        const thumbnailSrc = await cropAndDrawBox(scanResult.photo_base64, box.bbox, 1.2);

        const row = document.createElement('tr');
        row.classList.add('unconfirmed-row');
        row.dataset.scanIndex = scanIndex;
        row.dataset.boxIndex = boxIndex;

        row.innerHTML = `
            <td><img src="${thumbnailSrc}" alt="Инструмент" class="tool-thumbnail" style="cursor: pointer;"></td>
            <td>${createNameInputHTML()}</td>
            <td>${createIdInputHTML()}</td>
            <td class="actions-cell">
                <button class="btn-confirm">Подтвердить</button>
                <button class="btn-delete">Удалить</button>
            </td>
            <td>${(box.confidence * 100).toFixed(0)}%</td>
        `;
        tableBody.appendChild(row);

        const nameInput = row.querySelector('.tool-name-input');
        nameInput.dataset.recommended = JSON.stringify(box.predicted_name);

        if (box.predicted_name.length === 1 && workDataState.tool_name_to_id[box.predicted_name[0]]) {
            nameInput.value = box.predicted_name[0];
            handleSync(row, 'name');
        }

        const thumbnailImg = row.querySelector('.tool-thumbnail');
        thumbnailImg.addEventListener('click', async () => {
            const fullImageWithBox = await drawImageWithBox(scanResult.photo_base64, box.bbox);
            openImageModalCallback(fullImageWithBox);
        });
    }
}

/**
 * Исправленная функция синхронизации
 * @param {HTMLTableRowElement} row - Строка таблицы.
 * @param {'name' | 'id'} source - Поле, которое было изменено.
 */
function handleSync(row, source) {
    const nameInput = row.querySelector('.tool-name-input');
    const idInput = row.querySelector('.tool-id-input');

    if (source === 'name') {
        const selectedName = nameInput.value;
        if (workDataState.tool_name_to_id[selectedName]) {
            idInput.value = workDataState.tool_name_to_id[selectedName];
        } else {
            idInput.value = '';
        }
    }

    if (source === 'id') {
        const enteredId = idInput.value;
        if (workDataState.id_to_tool_name[enteredId]) {
            nameInput.value = workDataState.id_to_tool_name[enteredId];
        } else {
            nameInput.value = '';
        }
    }
}

function initializeTableEventListeners() {
    tableBody.addEventListener('focusin', (e) => {
        document.querySelectorAll('.autocomplete-list').forEach((list) => {
            list.classList.add('hidden');
        });

        if (e.target.matches('.tool-name-input')) {
            updateNameDropdown(e.target);
        }
        if (e.target.matches('.tool-id-input')) {
            updateIdDropdown(e.target);
        }
    });

    tableBody.addEventListener('input', (e) => {
        const row = e.target.closest('tr');
        if (e.target.matches('.tool-name-input')) {
            updateNameDropdown(e.target, e.target.value);
            handleSync(row, 'name');
        }
        if (e.target.matches('.tool-id-input')) {
            updateIdDropdown(e.target, e.target.value);
            handleSync(row, 'id');
        }
    });

    tableBody.addEventListener('click', async (e) => {
        const row = e.target.closest('tr');

        if (e.target.matches('.autocomplete-list-item')) {
            const container = e.target.closest('.autocomplete-container');
            const input = container.querySelector('.autocomplete-input');
            input.value = e.target.dataset.value;
            container.querySelector('.autocomplete-list').classList.add('hidden');
            const source = input.matches('.tool-name-input') ? 'name' : 'id';
            handleSync(row, source);
        }

        if (e.target.matches('.btn-delete')) {
            row.remove();
        }

        if (e.target.matches('.btn-confirm')) {
            const confirmButton = e.target;
            confirmButton.disabled = true;
            confirmButton.textContent = '...';

            try {
                const toolId = row.querySelector('.tool-id-input').value;
                const toolName = row.querySelector('.tool-name-input').value;

                if (!toolId || !toolName || !workDataState.id_to_tool_name[toolId]) {
                    alert('Пожалуйста, выберите корректный инструмент из списка.');
                    return;
                }

                const {scanIndex, boxIndex} = row.dataset;
                const scanResult = workDataState.scanResults[scanIndex];
                const originalBox = scanResult.boxes[boxIndex];

                const boxDataToApprove = {
                    photo_id: scanResult.photo_id, bbox: originalBox.bbox, tool_id: parseInt(toolId),
                };

                await approveBox(currentWorkId, currentWorkStage, boxDataToApprove);

                const newApprovedBox = {...boxDataToApprove, tool_name: toolName};
                updateStateAfterApproval(newApprovedBox);
                row.classList.remove('unconfirmed-row');
                row.innerHTML = `
                    <td>${row.cells[0].innerHTML}</td>
                    <td>${toolName}</td>
                    <td>${toolId}</td>
                    <td></td>
                    <td><span class="status-confirmed">Подтверждено</span></td>
                `;
                const thumbnailImg = row.querySelector('.tool-thumbnail');
                thumbnailImg.addEventListener('click', async () => {
                    const fullImageWithBox = await drawImageWithBox(scanResult.photo_base64, originalBox.bbox);
                    openImageModal(fullImageWithBox);
                });
            } catch (error) {
                alert(`Ошибка подтверждения: ${error.message}`);
            } finally {
                confirmButton.disabled = false;
                confirmButton.textContent = 'Подтвердить';
            }
        }
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.autocomplete-container')) {
            document
                .querySelectorAll('.autocomplete-list')
                .forEach((list) => list.classList.add('hidden'));
        }
    });
}
