function IsInt(str) {
    return /^\+?([1-9]\d*)$/.test(str);
}

function IsFloat(str){
    return /^[-+]?[0-9]*\.?[0-9]+$/.test(str);
}
