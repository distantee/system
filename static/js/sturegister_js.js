//验证用户名
function checkName(value) {
    // var val = document.getElementById('name').value;
    alert(value);
    var csrf = $("input[type='hidden']").val();
    var spanObj = document.getElementById("nameSpan");
    if (value == "") {// 空验证
        spanObj.innerHTML = '姓名' + "不能为空";
        spanObj.style.color = "red";
        return false;
    } else if (value) {
        //<input type="hidden" name="csrfmiddlewaretoken" value="VqyrgTnr6jmTRMCte4fSLGMA5c7W66DOdUTDfsgPJIoo2bEUBuXQCJwdyZZugs03">
        $.post('/student/register/',{'uname':value,'csrfmiddlewaretoken':csrf},
            function (result) {
            //alert(result.flag);
            if(result.flag){
                spanObj.innerHTML = "OK";
                spanObj.style.color = "green";
                return true;
            }else{
                spanObj.innerHTML = "数据库已存在";
                $('#nameSpan').css('color','red');
                return false;
            }
        });
        // spanObj.innerHTML = "OK";
        // spanObj.style.color = "green";
        // return true;
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
