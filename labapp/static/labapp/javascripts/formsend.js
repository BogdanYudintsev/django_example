/*
Реализация AJAX с помощью асинхронного метода fetch. Современный вариант реализации AJAX.
*/

var sendbtn = document.getElementById("sendbtn");    // выбираем DOM-елемент (кнопку)

// Привязываем к элементу обработчик события "click"
sendbtn.addEventListener("click", function (e) {
    /* Инструкция preventDefault позволяет переопределить стандартное поведение браузера,
    если ее убрать, то браузер по-умолчанию обновит страницу после отправки данных формы */
    e.preventDefault();
    // Получаем данные полей формы
    let fname = document.getElementsByName("fname")[0].value;
    let lname = document.getElementsByName("lname")[0].value;
    let email = document.getElementsByName("email")[0].value;
    let reqtype = document.getElementsByName("reqtype")[0].value
    let reqtext = document.getElementsByName("reqtext")[0].value
    // Преобразуем полученные данные в JSON
    var formdata = JSON.stringify({ firstname: fname, lastname: lname, email: email, reqtype: reqtype, reqtext: reqtext});
    // получаем csrftoken, который используется в Django при отправке данных из формы
    // csrftoken генерируется Django при использовании инструкции {% csrf_token %} в html-шаблоне
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrftoken)
    
    // Отправляем запрос через fetch (необходимо выставить соответствующий заголовок (headers)!)
    fetch("/contact/",
    {
        method: "POST",
        body: formdata,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then( response => {
        // fetch в случае успешной отправки возвращает Promise, содержащий response объект (ответ на запрос)
        // Возвращаем json-объект из response и получаем данные из поля message
        response.json().then(function(data) {
            console.log(data)
            // Добавление данных, полученных через AJAX, в элемент statusfield
            let statfield = document.getElementById("statusfield");
            //statfield.textContent = data.message;
            //statfield.textContent.bold();
            alert(data.message);
        });
    })
    .catch( error => {
        alert(error);
        console.error('error:', error);
    });

});
