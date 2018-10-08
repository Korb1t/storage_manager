Element.prototype.remove = function () {
    this.parentElement.removeChild(this);
};


function insertAlertSuccess(isSuccess, string, idOfParentElement, idToInsertBefore) {
    if (parseInt(isSuccess) === 1) {
        var successAlert = document.createElement("div");
        successAlert.setAttribute("class", "alert alert-success alert-show-success");
        successAlert.setAttribute("role", "alert");
        successAlert.setAttribute("id", "alert");
        successAlert.innerHTML = string;
        document.getElementById(idOfParentElement).insertBefore(successAlert, document.getElementById(idToInsertBefore))
    }
}

function insertAlertWarning(isSuccess, string, idOfParentElement, idToInsertBefore) {
    if (parseInt(isSuccess) === 1) {
        var successAlert = document.createElement("div");
        successAlert.setAttribute("class", "a");
        successAlert.setAttribute("role", "alert");
        successAlert.setAttribute("id", "alert");
        successAlert.innerHTML = string;
        document.getElementById(idOfParentElement).insertBefore(successAlert, document.getElementById(idToInsertBefore))
    }
}

function deleteAlert() {
    if (document.getElementById("alert"))
        document.getElementById("alert").remove()

}
