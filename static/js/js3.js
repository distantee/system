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