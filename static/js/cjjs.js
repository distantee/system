  // function test1(studentname) {
  //
  //       location.href = '/student/gradelr/?studentname='+studentname.value;
  //   }
  //    function test2(clazzname) {
  //       location.href = '/student/gradelr/?clazzname='+clazzname.value;
  //   }
  //    function test3(coursename) {
  //       location.href = '/student/gradelr/?coursename='+coursename.value;
  //   }


 function test1(studentname) {
    //alert('222');
     $.ajax({
        url : '/student/gradelr/',
        data:{studentname:studentname,'csrfmiddlewaretoken':$('input[name="csrfmiddlewaretoken"]').val()},
        cache : false,
        async : false,
        type : "POST",
        dataType : 'json',

         error:function(){
            console.log('12345')
            },
        success : function (result) {

             //console.log(result)
             // console.log(result.clazz),
             // console.log(result.clazz['clazzname']),
             //console.log(result.courseList),
                 console.log(result);


            $("#clazzname").empty();
            $("#clazzname").append('<option value=' + result.clazzname + '>' + result.clazzname + '</option>');


            $("#coursename").empty();
            $("#coursename").append("<option value='-1'>-请 选 择 课 程-</option>");
            for (var i = 0; i < result.courseList.length; i++) {
                $("#coursename").append('<option value=' + result.courseList[i] + '>' + result.courseList[i] + '</option>');
                //console.log(result.courseList.i)
            }
        }


})

 }
