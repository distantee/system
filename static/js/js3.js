function operateCode(){
				globalnum = Math.floor(Math.random()*9000+1000);
				//alert(globalnum);
				var obj = document.getElementById("codeVeri");
				obj.innerHTML = globalnum;
				//alert(obj.value);
			}
