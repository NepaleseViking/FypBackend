document.addEventListener('DOMContentLoaded', function () {
    const categoryField = document.getElementById('id_category');
    const storageField = document.querySelector('.form-row.field-storages');

    function toggleStorageField() {
        const selectedOption = categoryField.options[categoryField.selectedIndex].text.toLowerCase();
        if (selectedOption === 'smartphone') {
            storageField.style.display = 'block';
        } else {
            storageField.style.display = 'none';
            const storageInput = document.getElementById('id_storages');
            if (storageInput) storageInput.value = '';
        }
    }

    if (categoryField && storageField) {
        toggleStorageField(); // Run on load
        categoryField.addEventListener('change', toggleStorageField); // Run on change
    }
});