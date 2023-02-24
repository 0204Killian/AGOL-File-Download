function updateFeatureDropdown() {
    let folder_id = document.getElementById("folderselect").value;
    let featureDropdown = document.getElementById("featureselect");
    let currentOptions = Array.from(featureDropdown.options).map(option => option.value);
    fetch(`http://localhost:8000/get_features/${folder_id}`)
        .then(response => response.json())
        .then(data => {
            let newOptions = ['Features', ...data.features];
            if (!arraysEqual(currentOptions, newOptions)) {
                featureDropdown.options.length = 0;
                for (let i = 0; i < newOptions.length; i++) {
                    featureDropdown.options[i] = new Option(newOptions[i], newOptions[i]);
                }
            }
        });
}

function arraysEqual(arr1, arr2) {
    if (arr1.length !== arr2.length) {
        return false;
    }
    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] !== arr2[i]) {
            return false;
        }
    }
    return true;
}

function updateSublayerDropdown() {
    let feature_id = document.getElementById("featureselect").value;
    fetch(`http://localhost:8000/get_sublayers/${feature_id}`)
        .then(response => response.json())
        .then(data => {
            let featureDropdown = document.getElementById("sublayerselect");
            featureDropdown.options.length = 0;
            featureDropdown.options[0] = new Option('Sublayer', '');
            for (let i = 0; i < data.sublayers.length; i++) {
                featureDropdown.options[i + 1] = new Option(data.sublayers[i], data.sublayers[i]);
            }
        });
}

async function download(){
    let feature_id = document.getElementById("featureselect").value;
    let sublayer = document.getElementById("sublayerselect").value;
    let filetype = document.getElementById("filetype").value;
    
    await fetch(`http://localhost:8000/download/${feature_id}/${sublayer}/${filetype}/`)
      .then(response => response.json())
      .then(data => {
        let filename = data.download_trigger;

        filename = filename.replace(/ /g,"_");
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/static/downloads/' + filename + '.zip', true);
        xhr.responseType = 'blob';
        xhr.onload = function() {
            if (xhr.status === 200) {
            var blob = new Blob([xhr.response], {type: 'application/zip'});
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            fetch('http://localhost:8000/clear/')
        }
        };

        xhr.send();
      })
      .catch(error => {
        alert(error);
      });
  }