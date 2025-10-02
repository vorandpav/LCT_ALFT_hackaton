// js/graphics.js

/**
 * Рисует рамку на изображении и возвращает результат в base64.
 * @param {string} photoBase64 - Изображение.
 * @param {Array<number>} bbox - Рамка [x_center, y_center, width, height].
 * @returns {Promise<string>} - Изображение с нарисованной рамкой в base64.
 */
function drawImageWithBox(photoBase64, bbox) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = `data:image/jpeg;base64,${photoBase64}`;
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            const ctx = canvas.getContext('2d');

            ctx.drawImage(img, 0, 0);

            const [x1, y1, x2, y2, x3, y3, x4, y4] = bbox;

            ctx.strokeStyle = 'red';
            ctx.lineWidth = Math.max(3, img.naturalWidth / 300);

            ctx.beginPath();
            ctx.moveTo(x1 * img.naturalWidth, y1 * img.naturalHeight);
            ctx.lineTo(x2 * img.naturalWidth, y2 * img.naturalHeight);
            ctx.lineTo(x3 * img.naturalWidth, y3 * img.naturalHeight);
            ctx.lineTo(x4 * img.naturalWidth, y4 * img.naturalHeight);
            ctx.closePath();
            ctx.stroke();

            resolve(canvas.toDataURL('image/jpeg'));
        };
        img.onerror = reject;
    });
}

/**
 * Обрезает изображение в форме квадрата по рамке (с расширением) и рисует на нем исходную рамку.
 * @param {string} photoBase64 - Изображение в base64.
 * @param {Array<number>} bbox - Исходная рамка [x_center, y_center, width, height].
 * @param {number} expansionFactor - Коэффициент расширения.
 * @returns {Promise<string>} - Обрезанное изображение с рамкой в base64.
 */
function cropAndDrawBox(photoBase64, bbox, expansionFactor = 1.2) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = `data:image/jpeg;base64,${photoBase64}`;
        img.onload = () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            const xs = [bbox[0], bbox[2], bbox[4], bbox[6]].map(x => x * img.naturalWidth);
            const ys = [bbox[1], bbox[3], bbox[5], bbox[7]].map(y => y * img.naturalHeight);

            const minX = Math.min(...xs);
            const maxX = Math.max(...xs);
            const minY = Math.min(...ys);
            const maxY = Math.max(...ys);

            const boxWidth = maxX - minX;
            const boxHeight = maxY - minY;
            const xCenter = minX + boxWidth / 2;
            const yCenter = minY + boxHeight / 2;

            const expandedWidth = boxWidth * expansionFactor;
            const expandedHeight = boxHeight * expansionFactor;

            const cropSide = Math.max(expandedWidth, expandedHeight);
            const cropX = xCenter - cropSide / 2;
            const cropY = yCenter - cropSide / 2;

            canvas.width = cropSide;
            canvas.height = cropSide;

            ctx.drawImage(img, cropX, cropY, cropSide, cropSide, 0, 0, cropSide, cropSide);

            ctx.strokeStyle = 'red';
            ctx.lineWidth = Math.max(2, cropSide / 100);
            ctx.beginPath();
            ctx.moveTo(xs[0] - cropX, ys[0] - cropY);
            ctx.lineTo(xs[1] - cropX, ys[1] - cropY);
            ctx.lineTo(xs[2] - cropX, ys[2] - cropY);
            ctx.lineTo(xs[3] - cropX, ys[3] - cropY);
            ctx.closePath();
            ctx.stroke();

            resolve(canvas.toDataURL('image/jpeg'));
        };
        img.onerror = reject;
    });
}


/**
 * Рисует все рамки на изображении и возвращает результат в base64.
 * @param {string} photoBase64 - Изображение.
 * @param {Array<Array<number>>} bboxes - Массив рамок [[x_center, y_center, width, height], ...].
 * @returns {Promise<string>} - Изображение с нарисованными рамками в base64.
 */
function drawAllBoxesOnImage(photoBase64, bboxes) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = `data:image/jpeg;base64,${photoBase64}`;
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            const ctx = canvas.getContext('2d');

            ctx.drawImage(img, 0, 0);

            ctx.strokeStyle = 'red';
            ctx.lineWidth = Math.max(3, img.naturalWidth / 300);

            bboxes.forEach((bbox) => {
                const [x1, y1, x2, y2, x3, y3, x4, y4] = bbox;
                ctx.beginPath();
                ctx.moveTo(x1 * img.naturalWidth, y1 * img.naturalHeight);
                ctx.lineTo(x2 * img.naturalWidth, y2 * img.naturalHeight);
                ctx.lineTo(x3 * img.naturalWidth, y3 * img.naturalHeight);
                ctx.lineTo(x4 * img.naturalWidth, y4 * img.naturalHeight);
                ctx.closePath();
                ctx.stroke();
            });

            resolve(canvas.toDataURL('image/jpeg'));
        };
        img.onerror = reject;
    });
}