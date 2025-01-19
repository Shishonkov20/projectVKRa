window.onload = function () {
    let app = document.getElementById('app');
    let projectListLoader = new XMLHttpRequest()
    projectListLoader.onreadystatechange = function (){
        if (projectListLoader.readyState == 4){
            if (projectListLoader.status == 200){
                let data = JSON.parse(projectListLoader.responseText);
                console.log(data);
            }
        }
    }

    function projectLoad(){
        projectListLoader.open('GET', 'http://127.0.0.1:8000/api/projects', true);
        projectListLoader.send();
    }
    projectLoad();
}