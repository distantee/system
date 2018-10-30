function operateCode(){
				globalnum = Math.floor(Math.random()*9000+1000);
				//alert(globalnum);
				var obj = document.getElementById("codeVeri");
				obj.innerHTML = globalnum;
				//alert(obj.value);
			}
function getTime(){
				//获取当前的时间
				var now = new Date();
				//输出当前的时间
				document.getElementById("timeset").innerHTML=now.toLocaleString();
				//一秒之后调用一次，必须放到方法中，每次调用方法，都执行该语句
				//window.setTimeout(getTime,1000);

				window.setTimeout("getTime()",1000);
			}

function loadXMLDoc() {
	var xmlhttp;
	if (window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
	}
	xmlhttp = onreadystatechange = function () {
		if (xmlhttp.readyState==4 && xmlhttp.status==200){
			document.getElementById(delallc).innerHTML = xmlhttp.responseText;
		}
    }
	xmlhttp.open('GET','/student/update/')
}

// $(function(){
//         	$("#delallc").empty(function(){
//
//         		//使用jquery最底层的ajax封装方法来发送ajax请求
//         		var url1='/student/update';//file/andy.js   file/tony.js
//         		var data1={"allcourse":"allcourse"};
//         		$.ajax({
//         			 url:url1,
//         			 type:"get",
//         			 data:data1,
//         			 dataType:"json",
//         			 success:function(result){
//
//         				//alert(result);
//              			// var name=result.person.name;
//              			// var website=result.person.website;
//              			// var email=result.person.email;
//                         //
//              			// alert(name+"   "+website+"   "+email);
//
//              			//根据用户的需求进行编码  按照如下方式放入div进行显示  dom  操作元素文档结构
//
//        				    //  <h2><a href="个人网站">姓名</a></h2>
//                          // <a href="个人网站">邮箱</a>
//
//        				  //append();向每个匹配的元素内部追加内容
//        				  //empty():删除匹配的元素集合中所有的子节点
//        				  $("#message").empty().append("<h2><a href="+website+">"+name+"</a></h2>")
//        				               .append("<a href="+website+">"+email+"</a>");
//         			 }
//         		});
//         		return false;
//         	});
//         });

