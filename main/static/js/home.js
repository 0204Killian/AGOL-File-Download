function updateFeatureDropdown() {
    let folder_id = document.getElementById("folderselect").value;
    fetch(`http://localhost:8000/get_features/${folder_id}`)
        .then(response => response.json())
        .then(data => {
            let featureDropdown = document.getElementById("featureselect");
            featureDropdown.options.length = 0;
            featureDropdown.options[0] = new Option('Features', '');
            for (let i = 0; i < data.features.length; i++) {
                featureDropdown.options[i + 1] = new Option(data.features[i], data.features[i]);
            }
        });
}