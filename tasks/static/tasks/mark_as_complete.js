const url = window.location.href
const csrf = Cookies.get('csrftoken')

const updateField = (task_id) =>{
    var form = new FormData();
    var csrftoken = csrf;

    form.append('task_id', task_id);

    $.ajax({
        type:'post',
        url :`${url}`,
        data:{'task_id':task_id, csrfmiddlewaretoken: csrftoken},
        dataType: 'json',
        success:function(response){
            const results = response.results}
        })
    }
