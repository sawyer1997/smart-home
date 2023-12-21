document.addEventListener('DOMContentLoaded', function () {
    let deviceTypeSelect = document.getElementById('id_device_type');
    let modelNameSelect = document.getElementById('id_model_name');

    deviceTypeSelect.addEventListener('change', function () {
        let selectedDeviceType = this.value;

        // Clear previous options
        modelNameSelect.innerHTML = '';

        if (selectedDeviceType) {
            // Fetch companies based on the selected device type
            fetch('/get_models/' + selectedDeviceType + '/')
                .then(response => response.json())
                .then(data => {
                    // Populate the second dropdown with fetched companies
                    data.forEach(company => {
                        let option = document.createElement('option');
                        option.value = company;
                        option.text = company;
                        modelNameSelect.add(option);
                    });
                });
        }
    });
});
