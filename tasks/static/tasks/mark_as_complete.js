const url = window.location.href
const csrftoken = Cookies.get('csrftoken')
var div = document.getElementById("display-tasks");


const updateField = (task_id) =>{
    $.ajax({
        type:'post',
        url :`${url}/tasks/${task_id}/markascomplete`,
        data:{csrfmiddlewaretoken: csrftoken},
        dataType: 'json',
        error: function(error){
            console.log(':('+error)
            div.innerHTML += "Failed to update."

        }
     })
    }
