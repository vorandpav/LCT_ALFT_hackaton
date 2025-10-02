// js/autocomplete.js

/**
 * Создает HTML-разметку для поля ввода названия инструмента с автоподстановкой.
 * @returns {string} HTML-строка.
 */
function createNameInputHTML() {
    return `
        <div class="autocomplete-container">
            <input type="text" class="autocomplete-input tool-name-input" placeholder="Введите название...">
            <div class="autocomplete-list hidden"></div>
        </div>
    `;
}

/**
 * Создает HTML-разметку для поля ввода ID инструмента с автоподстановкой.
 * @returns {string} HTML-строка.
 */
function createIdInputHTML() {
    return `
    <div class="autocomplete-container">
        <input type="text" class="tool-id-input autocomplete-input" placeholder="ID">
        <ul class="autocomplete-list hidden"></ul>
    </div>
`;
}

/**
 * Отрисовывает список элементов автодополнения.
 * @param {string[]} items - Элементы для отображения.
 * @param {HTMLElement} listElement - Элемент <ul> для списка.
 * @param {'name' | 'id'} type - Тип автодополнения.
 * @param {function(string): void} onSelect - Функция обратного вызова при выборе элемента.
 */
function renderItems(items, listElement, type, onSelect) {
    listElement.innerHTML = '';
    const recommendedTools = workDataState.id_to_tool_name;
    const recommendedIds = Object.keys(recommendedTools);

    items.forEach((item) => {
        const li = document.createElement('li');
        li.textContent = item;
        li.classList.add('autocomplete-list-item');

        if (type === 'id' && recommendedIds.includes(item)) {
            li.classList.add('is-recommended');
        }

        li.addEventListener('mousedown', (e) => {
            e.preventDefault();
            onSelect(item);
        });
        listElement.appendChild(li);
    });
}

/**
 * Обновляет и показывает выпадающий список для поля "Название".
 * @param {HTMLInputElement} inputElement - Поле ввода названия.
 * @param {string} filterText - Текст для фильтрации.
 */
function updateNameDropdown(inputElement, filterText = '') {
    const dropdown = inputElement.nextElementSibling;
    dropdown.innerHTML = '';
    const recommendedNames = JSON.parse(inputElement.dataset.recommended || '[]');
    let items = [];

    recommendedNames.forEach((name) => {
        if (workDataState.tool_name_to_id[name] && name.toLowerCase().includes(filterText.toLowerCase())) {
            items.push({name, isRecommended: true});
        }
    });

    for (const name of Object.keys(workDataState.tool_name_to_id)) {
        if (!items.some((item) => item.name === name) && name.toLowerCase().includes(filterText.toLowerCase())) {
            items.push({name, isRecommended: false});
        }
    }

    items.forEach(({name, isRecommended}) => {
        const itemEl = document.createElement('div');
        itemEl.className = 'autocomplete-list-item';
        if (isRecommended) itemEl.classList.add('is-recommended');
        itemEl.textContent = name;
        itemEl.dataset.value = name;
        dropdown.appendChild(itemEl);
    });

    dropdown.classList.toggle('hidden', items.length === 0);
}

/**
 * Обновляет и показывает выпадающий список для поля "ID" с корректной подсветкой.
 * @param {HTMLInputElement} inputElement - Поле ввода ID.
 * @param {string} filterText - Текст для фильтрации.
 */
function updateIdDropdown(inputElement, filterText = '') {
    const dropdown = inputElement.nextElementSibling;
    dropdown.innerHTML = '';

    const row = inputElement.closest('tr');
    const nameInput = row.querySelector('.tool-name-input');
    const recommendedNames = JSON.parse(nameInput.dataset.recommended || '[]');
    const recommendedIds = recommendedNames
        .map((name) => workDataState.tool_name_to_id[name])
        .filter(Boolean);

    let items = [];

    recommendedIds.forEach((id) => {
        if (id.includes(filterText) && workDataState.id_to_tool_name[id]) {
            items.push({id, isRecommended: true});
        }
    });

    for (const id of Object.keys(workDataState.id_to_tool_name)) {
        if (!items.some((item) => item.id === id) && id.includes(filterText)) {
            items.push({id, isRecommended: false});
        }
    }

    items.forEach(({id, isRecommended}) => {
        const itemEl = document.createElement('li');
        itemEl.className = 'autocomplete-list-item';
        if (isRecommended) {
            itemEl.classList.add('is-recommended');
        }
        itemEl.textContent = id;
        itemEl.dataset.value = id;
        dropdown.appendChild(itemEl);
    });

    dropdown.classList.toggle('hidden', items.length === 0);
}
