const url = window.location.href



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const updateField = (task_id) =>{
    var form = new FormData();
    var csrftoken = getCookie('csrftoken');

    form.append('order_id', task_id);

    $.ajax({
        type:'post',
        url :`${url}`,
        data:{'task_id':task_id, csrfmiddlewaretoken: csrftoken},
        dataType: 'json',
        success:function(response){
            const results = response.results}
        })
    }
