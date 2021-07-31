function validate(){
    var error =  validate_text("job-location") + validate_text("job-title") +
                 validate_checkboxes("job-type") + validate_checkboxes("job-site");

    if (error){
        alert(error)
        return false
    }
}

function validate_text(element_name){
    var letters = /^[A-Za-z]+$/;
    var error = "";
    var element = document.getElementById(element_name).value.trim();

    if (element.length == 0){
        error += element_name + " input is empty\n";
    }
    else if (!(element.match(letters))){
        error += element_name + " must only include letters\n";
    }

    if (error){
        document.getElementById(element_name).style.border = "2px solid red";
    }

    return error;
}

function validate_checkboxes(check_class){
    var checks = document.getElementsByClassName(check_class);
    var checked = false;
    var error = "";
    for (var i=0; i < checks.length; i++){
        checked = checked || checks[i].checked;
    }

    if (checked == false){
        error = "must select at least one " + check_class + "\n";
    }

    return error;
}