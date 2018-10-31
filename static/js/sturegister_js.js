//验证用户名
function checkName() {
    var val = document.getElementById('name').value;
    //alert(val);
    var spanObj = document.getElementById("nameSpan");
    if (val == "") {// 空验证
        spanObj.innerHTML = '姓名' + "不能为空";
        spanObj.style.color = "red";
        return false;
    } else if (val) {
        spanObj.innerHTML = "OK";
        spanObj.style.color = "green";
        return true;
    } else {
        spanObj.innerHTML = '姓名' + "不符合要求";
        spanObj.style.color = "red";
        return false;
    }
}

//验证班级
function checkClazz() {
    var val = document.getElementById('clazz').value;
    //alert(val);
    var spanObj = document.getElementById("clazzSpan");
    if (val == "") {// 空验证
        spanObj.innerHTML = '班级' + "不能为空";
        spanObj.style.color = "red";
        return false;
    } else if (val) {
        spanObj.innerHTML = "OK";
        spanObj.style.color = "green";
        return true;
    } else {
        spanObj.innerHTML = '班级' + "不符合要求";
        spanObj.style.color = "red";
        return false;
    }
}



//验证年龄
function checkAge() {
    var reg = /^\d{1,2}$/;
    var val = document.getElementById('age').value;
    //alert(val);
    var spanObj = document.getElementById("ageSpan");
    // var dataName = document.getElementById(age).alt;
    if (val == "") {// 空验证
        spanObj.innerHTML = '年龄' + "不能为空";
        spanObj.style.color = "red";
        return false;
    } else if (reg.test(val)) {
        spanObj.innerHTML = "OK";
        spanObj.style.color = "green";
        return true;
    } else {
        spanObj.innerHTML = '年龄' + "不符合要求";
        spanObj.style.color = "red";
        return false;
    }
}

//按钮提交前  再对所有数据项的格式做一下验证     都通过  才能提交    否则不让提交
function checkAll(){
    // alert(checkUname());
    var flag = checkName() & checkClazz() & checkAge();
    return flag == 1 ? true : false;
}
