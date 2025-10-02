// js/report.js

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const workId = urlParams.get('workId');
    const userId = urlParams.get('userId');

    const initialDataString = sessionStorage.getItem('initialData');
    if (!initialDataString) {
        alert('Страница обновлена, пожалуйста, войдите заново.');
        window.location.href = 'index.html';
        return;
    }
    const initialData = JSON.parse(initialDataString);
    sessionStorage.removeItem('initialData');

    if (!workId || !userId) {
        alert('ID работы или ID пользователя не найдены. Возвращаемся на страницу входа.');
        window.location.href = 'index.html';
        return;
    }
    if (!initialData) {
        alert('Данные сессии не найдены. Пожалуйста, войдите заново.');
        window.location.href = 'index.html';
        return;
    }

    const info = {
        userId: document.getElementById('info-user-id'),
        userName: document.getElementById('info-user-name'),
        powers: document.getElementById('info-powers'),
        workId: document.getElementById('info-work-id'),
        stage: document.getElementById('info-stage'),
    };
    const exitButton = document.getElementById('exit-button');
    const photoSelect = document.getElementById('photo-select');
    const canvas = document.getElementById('photo-canvas');
    const ctx = canvas.getContext('2d');

    const imageModal = document.getElementById('image-modal');
    const modalImage = document.getElementById('modal-image');
    const modalCloseButton = document.getElementById('modal-close-button');

    const tooltip = document.createElement('div');
    tooltip.id = 'tooltip';
    tooltip.className = 'hidden';
    document.querySelector('.image-display').appendChild(tooltip);

    let allPhotos = [];
    let allBoxes = [];
    let currentBoxesOnCanvas = [];

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

    async function renderTable(tableId, boxes, photos) {
        const tableBody = document.querySelector(`${tableId} tbody`);
        tableBody.innerHTML = '';

        for (const box of boxes) {
            const photo = photos.find((p) => p.photo_id === box.photo_id);
            if (!photo) continue;
            const thumb = await cropAndDrawBox(photo.photo_base64, box.bbox, 1.2);
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><img src="${thumb}" class="tool-thumbnail"></td>
                <td>${box.tool_name}</td>
                <td>${box.tool_id}</td>
                <td><span class="status-confirmed">Подтверждено</span></td>
            `;
            tableBody.appendChild(row);
            const thumbnailImg = row.querySelector('.tool-thumbnail');
            thumbnailImg.addEventListener('click', async () => {
                const fullImageWithBox = await drawImageWithBox(photo.photo_base64, box.bbox);
                openImageModal(fullImageWithBox);
            });
        }
    }

    exitButton.addEventListener('click', () => (window.location.href = 'index.html'));
    modalCloseButton.addEventListener('click', closeImageModal);
    imageModal.addEventListener('click', (e) => {
        if (e.target === imageModal) closeImageModal();
    });

    photoSelect.addEventListener('change', async (e) => {
        const selectedPhotoId = e.target.value;
        const photo = allPhotos.find((p) => p.photo_id == selectedPhotoId);
        if (!photo) return;
        currentBoxesOnCanvas = allBoxes.filter((b) => b.photo_id == selectedPhotoId);
        const imageWithBoxes = await drawAllBoxesOnImage(
            photo.photo_base64,
            currentBoxesOnCanvas.map((b) => b.bbox)
        );
        const img = new Image();
        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        };
        img.src = imageWithBoxes;
    });

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;

        let foundBox = null;

        for (const box of currentBoxesOnCanvas) {
            const polygon = [];
            for (let i = 0; i < box.bbox.length; i += 2) {
                polygon.push({
                    x: box.bbox[i] * canvas.width,
                    y: box.bbox[i + 1] * canvas.height
                });
            }

            let isInside = false;
            for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
                const xi = polygon[i].x, yi = polygon[i].y;
                const xj = polygon[j].x, yj = polygon[j].y;

                const intersect = ((yi > y) !== (yj > y))
                    && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
                if (intersect) isInside = !isInside;
            }

            if (isInside) {
                foundBox = box;
                break;
            }
        }

        if (foundBox) {
            tooltip.textContent = foundBox.tool_name;
            tooltip.style.left = `${e.clientX - rect.left + 15}px`;
            tooltip.style.top = `${e.clientY - rect.top}px`;
            tooltip.classList.remove('hidden');
        } else {
            tooltip.classList.add('hidden');
        }
    });

    canvas.addEventListener('mouseleave', () => {
        tooltip.classList.add('hidden');
    });

    async function initializeReport() {
        displayInfo('User ID', userId, info.userId);
        displayInfo('User Name', initialData.user_name, info.userName);
        displayInfo('Powers', initialData.powers, info.powers);
        displayInfo('Work ID', workId, info.workId);
        displayInfo('Stage', initialData.stage, info.stage);

        try {
            const reportData = await getReportData(workId, initialData.stage);
            const {GIVING, GETTING} = reportData;
            await renderTable('#giving-table', GIVING.approved_boxes || [], GIVING.photo_data || []);
            await renderTable('#getting-table', GETTING.approved_boxes || [], GETTING.photo_data || []);
            (GIVING.photo_data || []).forEach((p) => allPhotos.push({...p, stage: 'GIVING'}));
            (GETTING.photo_data || []).forEach((p) => allPhotos.push({...p, stage: 'GETTING'}));
            (GIVING.approved_boxes || []).forEach((b) => allBoxes.push({...b, stage: 'GIVING'}));
            (GETTING.approved_boxes || []).forEach((b) => allBoxes.push({...b, stage: 'GETTING'}));
            photoSelect.innerHTML = '';
            allPhotos.forEach((p) => {
                photoSelect.innerHTML += `<option value="${p.photo_id}">Фото ${p.photo_id} (Этап: ${p.stage})</option>`;
            });
            if (allPhotos.length > 0) {
                photoSelect.dispatchEvent(new Event('change'));
            }
        } catch (error) {
            alert(`Не удалось загрузить отчёт: ${error.message}`);
        }
    }

    initializeReport();
});
