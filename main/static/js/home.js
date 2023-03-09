function updateFeatureDropdown() {
    dropdownReset()
    let folder_id = document.getElementById("folderselect").value;
    let featureDropdown = document.getElementById("featureselect");
    let currentOptions = Array.from(featureDropdown.options).map(option => option.value);
    fetch(`http://localhost:8000/get_features/${folder_id}`)
    .then(response => response.json())
    .then(data => {
        let newOptions = ['Features', ...data.features];
        let featureTypes = data.feature_type;
        if (!arraysEqual(currentOptions, newOptions)) {
            featureDropdown.options.length = 0;
            for (let i = 0; i < newOptions.length; i++) {
                let optionValue = newOptions[i];
                let optionText = optionValue;
                if (i > 0) {
                    let featureType = featureTypes[i-1];
                    optionValue = `${optionValue}::${featureType}`;
                }
                featureDropdown.options[i] = new Option(optionText, optionValue);
            }
        }
        colourFeatures();
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

function colourFeatures(){
    let dropdown = document.getElementById("featureselect")
    for (let i = 0; i < dropdown.options.length; i++) {
        try{
            let option = dropdown.options[i];
            let featureType = /(?<=::).*/.exec(option.value)[0];
            switch (featureType) {
                case 'Feature Service':
                    option.style.backgroundColor = 'lightblue';
                    break;
                case 'Web Map':
                    option.style.backgroundColor = 'lightgreen';
                    break;
                case 'Web Mapping Application':
                    option.style.backgroundColor = 'lightpink';
                    break;
                case 'Service Definition':
                    option.style.backgroundColor = 'lightgrey';
                    break;
                case 'Microsoft Excel':
                    option.style.backgroundColor = 'green';
                    break;
                default:
                    option.style.backgroundColor = 'white';
            }
        }catch{
            continue
        }
    }
}

function updateSublayerDropdown() {
    sublayerReset()
    let feature_id = document.getElementById("featureselect").value;
    //Regex to look after the '::'
    let featureType = /(?<=::).*/.exec(feature_id)[0];
    //Regex to look before the '::'
    let featureName = /.+(?=::)/.exec(feature_id)[0];
    
    if (featureType == 'Web Map'){
        let featureDropdown = document.getElementById("sublayerselect");
        let featureDropdownlabel = document.getElementById("sublayerselectlabel");
        featureDropdown.hidden = true
        featureDropdownlabel.hidden = true
        return
    }else{
        let featureDropdown = document.getElementById("sublayerselect");
        let featureDropdownlabel = document.getElementById("sublayerselectlabel");
        featureDropdown.hidden = false
        featureDropdownlabel.hidden = false
    }

    fetch(`http://localhost:8000/get_sublayers/${featureName}`)
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
        let filetyped = document.getElementById('filetype');

        var xhr = new XMLHttpRequest();
        
        if(filetyped.value == 'GeoPackage'){
            xhr.open('GET', '/static/downloads/' + filename + '.gpkg', true)
        }else{
            xhr.open('GET', '/static/downloads/' + filename + '.zip', true);
        }
        xhr.responseType = 'blob';

        xhr.onload = function() {
            if(filetyped.value == 'GeoPackage'){
                var blob = new Blob([xhr.response], {type: 'application/geopackage'});
                filename += '.gpkg';
            }else{
                var blob = new Blob([xhr.response], {type: 'application/zip'});
                filename += '.zip';
            }
    
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            fetch('http://localhost:8000/clear/')

            let filetype = document.getElementById('filetype');
            filetype.selectedIndex = 0;
            let folderselect = document.getElementById('folderselect');
            folderselect.selectedIndex = 0;
            let featureselect = document.getElementById('featureselect');
            featureselect.selectedIndex = 0;
            let sublayerselect = document.getElementById('sublayerselect');
            sublayerselect.selectedIndex = 0;
        };
        xhr.send();
      })
      .catch(error => {
        alert(error);
      });
  }

  function dropdownReset(){
    layer = document.getElementById('featureselect')
    sublayer = document.getElementById('sublayerselect')

    layer.selectedIndex = 0;
    sublayer.selectedIndex = 0;
  }

  function sublayerReset(){
    sublayer = document.getElementById('sublayerselect')
    sublayer.selectedIndex = 0;
  }