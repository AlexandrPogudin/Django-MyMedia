function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("buttonexit").addEventListener("click", function() {
    var ExitFrame = document.getElementById("ExitFrame");
    if (ExitFrame.style.display === "none" || ExitFrame.style.display === "") {
        ExitFrame.style.display = "block";
    } else {
        ExitFrame.style.display = "none";
    }
});

document.getElementById("buttonsettings").addEventListener("click", function() {
    var NewInfoFrame = document.getElementById("NewInfoFrame");
    if (NewInfoFrame.style.display === "none" || NewInfoFrame.style.display === "") {
        NewInfoFrame.style.display = "block";
    } else {
        NewInfoFrame.style.display = "none";
    }
});

document.getElementById("newinfobuttoncansel").addEventListener("click", function() {
    var NewInfoFrame = document.getElementById("NewInfoFrame");
    NewInfoFrame.style.display = "none";
});

document.getElementById("signinpageclick").addEventListener("click", function() {
    var homeUrl = this.getAttribute("data-home-url");
    // Перенаправляем пользователя на главную страницу
    window.location.href = homeUrl;
});

document.getElementById("canselexitclick").addEventListener("click", function() {
    var ExitFrame = document.getElementById("ExitFrame");
    ExitFrame.style.display = "none";
});

document.getElementById("addfile").addEventListener("click", function() {
    var NewFileFrame = document.getElementById("NewFileFrame");
    NewFileFrame.style.display = "block";
});

document.getElementById("newfilebuttoncansel").addEventListener("click", function() {
    var NewFileFrame = document.getElementById("NewFileFrame");
    NewFileFrame.style.display = "none";
});

document.getElementById("newfilebuttonsave").addEventListener("click", function() {
    var fileName = document.querySelector(".newfileinputname").value;
    var fileInput = document.getElementById("file").files[0];
    var file = fileInput;
    var fileSize = file.size;
    var fileType = file.type;
    var currentPageString = window.location.pathname.split('/').filter(Boolean).pop();
    var currentPageNumber = parseInt(currentPageString, 10);

    var formData = new FormData();
    formData.append("FK_user", currentPageNumber);
    formData.append("file_name", fileName);
    formData.append("file", file);
    formData.append("file_size", fileSize);
    formData.append("file_type", fileType);

    var csrftoken = getCookie('csrftoken');

    // Отправка данных на сервер с использованием fetch API
    fetch("/upload/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        // Обработка ответа от сервера, если необходимо
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });

    var NewFileFrame = document.getElementById("NewFileFrame");
    NewFileFrame.style.display = "none";

    setTimeout(function() {
        location.reload();
    }, 3000);
});

document.getElementById("newinfobuttonsave1").addEventListener("click", function() {
    var oldpassword = document.querySelector(".inputoldpassword").value;
    var newpassword = document.querySelector(".inputnewpassword").value;
    var currentPageString = window.location.pathname.split('/').filter(Boolean).pop();
    var currentPageNumber = parseInt(currentPageString, 10);

    var formData = new FormData();
    formData.append("FK_user", currentPageNumber);
    formData.append("oldpassword", oldpassword);
    formData.append("newpassword", newpassword);


    var csrftoken = getCookie('csrftoken');

    // Отправка данных на сервер с использованием fetch API
    fetch("/changepassword/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        // Обработка ответа от сервера, если необходимо
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });

    var NewInfoFrame = document.getElementById("NewInfoFrame");
    NewInfoFrame.style.display = "none";

    setTimeout(function() {
        location.reload();
    }, 2000);
});


document.getElementById("newinfobuttonsave2").addEventListener("click", function() {
    var name = document.querySelector(".inputname").value;
    if (name == "") {
        name = "default";
    }
    var surname = document.querySelector(".inputsurname").value;
    if (surname == "") {
        surname = "default";
    }
    var avatar = document.getElementById("avatar");
    var haveavatar = true;
    if (avatar.files.length > 0){
        avatar = avatar.files[0];
    }
    else {
        haveavatar = false;
        avatar = "default";
    }

    var currentPageString = window.location.pathname.split('/').filter(Boolean).pop();
    var currentPageNumber = parseInt(currentPageString, 10);

    var formData = new FormData();
    formData.append("FK_user", currentPageNumber);
    formData.append("name", name);
    formData.append("surname", surname);
    formData.append("haveavatar", haveavatar);
    formData.append("avatar", avatar);

    var csrftoken = getCookie('csrftoken');

    // Отправка данных на сервер с использованием fetch API
    fetch("/changeinfo/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        // Обработка ответа от сервера, если необходимо
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });

    var NewInfoFrame = document.getElementById("NewInfoFrame");
    NewInfoFrame.style.display = "none";

    setTimeout(function() {
        location.reload();
    }, 2000);
});



document.querySelectorAll(".buttondelete").forEach(function(button) {
    button.addEventListener("click", function() {
        var fileId = button.getAttribute("data-file-id");
        var currentPageString = window.location.pathname.split('/').filter(Boolean).pop();
        var currentPageNumber = parseInt(currentPageString, 10);

        var formData = new FormData();
        formData.append("FK_user", currentPageNumber);
        formData.append("idfile", fileId);

        var csrftoken = getCookie('csrftoken');
        
        // Отправка данных на сервер с использованием fetch API
        fetch("/deletefile/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            // Обработка ответа от сервера, если необходимо
            console.log(data);
            location.reload();
        })
        .catch(error => {
            console.error(error);
        });
    });
});



// Получите все радио-кнопки и поле ввода даты
var radioButtons = document.querySelectorAll('.radio-inputs input[type="radio"]');
var dateInput = document.querySelector('.input-box input[type="date"]');

// Получите все файлы
var files = document.querySelectorAll('.file');

// Добавьте слушатели событий для радио-кнопок и поля ввода даты
radioButtons.forEach(function(radio) {
    radio.addEventListener('change', applyFilters);
});

dateInput.addEventListener('input', applyFilters);

// Функция для фильтрации файлов
function applyFilters() {
    var selectedType = document.querySelector('.radio-inputs input[type="radio"]:checked').nextElementSibling.textContent;
    var selectedDate = dateInput.value;

    files.forEach(function(file) {
        // ТИП
        var fileType = file.getAttribute('data-type');
        var fileDate = file.getAttribute('data-date');
        
        var typeParts = fileType.split('/');
        var fileTypeWithoutLastPart = typeParts[typeParts.length - 2];

        // ВРЕМЯ
        const selectedDatenew = new Date(selectedDate);
        fileDateParts = fileDate.split(/[\s,]+/);

        // Парсинг даты и времени
        const month = fileDateParts[0]; // месяц
        const day = parseInt(fileDateParts[1], 10); // день (преобразование в число)
        const year = parseInt(fileDateParts[2], 10); // год (преобразование в число)
        const time = fileDateParts[3]; // время (например, "9:57")

        // Создание объекта Date
        const fileDatenew = new Date(`${month} ${day}, ${year} ${time}`);

        // Установка часов, минут, секунд и миллисекунд в 0 для обеих дат
        selectedDatenew.setHours(0, 0, 0, 0);
        fileDatenew.setHours(0, 0, 0, 0);

        //ФИЛЬТРАЦИЯ
        switch(selectedType){
            case "Видео":
                if (fileTypeWithoutLastPart == "video"){
                    if (isNaN(selectedDatenew.getTime())){
                        console.log(isNaN(selectedDatenew.getTime()))
                        file.style.display = 'block';
                    }
                    else {
                        if (selectedDatenew.getTime() == fileDatenew.getTime()) {
                            file.style.display = 'block';
                        }
                        else {
                            file.style.display = 'none';
                        }
                    }
                }
                else {
                    file.style.display = 'none';
                }
                break;
            case "Фото":
                if (fileTypeWithoutLastPart == "image"){
                    if (isNaN(selectedDatenew.getTime())){
                        console.log(isNaN(selectedDatenew.getTime()))
                        file.style.display = 'block';
                    }
                    else {
                        if (selectedDatenew.getTime() == fileDatenew.getTime()) {
                            file.style.display = 'block';
                        }
                        else {
                            file.style.display = 'none';
                        }
                    }
                }
                else {
                    file.style.display = 'none';
                }
                break;
            case "Аудио":
                if (fileTypeWithoutLastPart == "audio"){
                    if (isNaN(selectedDatenew.getTime())){
                        console.log(isNaN(selectedDatenew.getTime()))
                        file.style.display = 'block';
                    }
                    else {
                        if (selectedDatenew.getTime() == fileDatenew.getTime()) {
                            file.style.display = 'block';
                        }
                        else {
                            file.style.display = 'none';
                        }
                    }
                }
                else {
                    file.style.display = 'none';
                }
                break;
            case "Документы":
                if (fileTypeWithoutLastPart == "application"){
                    if (isNaN(selectedDatenew.getTime())){
                        console.log(isNaN(selectedDatenew.getTime()))
                        file.style.display = 'block';
                    }
                    else {
                        if (selectedDatenew.getTime() == fileDatenew.getTime()) {
                            file.style.display = 'block';
                        }
                        else {
                            file.style.display = 'none';
                        }
                    }
                }
                else {
                    file.style.display = 'none';
                }
                break;
            case "Все":
                if (isNaN(selectedDatenew.getTime())){
                    console.log(isNaN(selectedDatenew.getTime()))
                    file.style.display = 'block';
                }
                else {
                    if (selectedDatenew.getTime() == fileDatenew.getTime()) {
                        file.style.display = 'block';
                    }
                    else {
                        file.style.display = 'none';
                    }
                }
                break;

            default:
                file.style.display = 'block';
        }
    
    });
}

document.querySelectorAll(".buttonnamefile").forEach(function(button) {
    button.addEventListener("click", function() {
        const filePath = this.parentElement.getAttribute('data-file-path');
            
        // Открываем файл в новом окне
        window.open("http://127.0.0.1:8000/media/" + filePath, '_blank');
    });
});

