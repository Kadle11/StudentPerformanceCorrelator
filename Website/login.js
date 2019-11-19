var url = "http://localhost:70";

function login()
{
	var api=url + "/api/v1/login";
	var uname= document.getElementById("username").value;
	var passwd= document.getElementById("password").value;
	console.log(uname);
	console.log(passwd);
  //var curl=api +"?"+"username="+ uname + "&" + "password=" + passwd;
  var curl=api;
  console.log(curl);
	data={};
  data["username"]=uname;
  data["password"]=passwd;
	var json= JSON.stringify(data);
	console.log(json);
  console.log(api);

	var xhttp = new XMLHttpRequest();
    xhttp.open("POST", curl, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');

    xhttp.onreadystatechange = function () {

         
          if (xhttp.readyState == 4 && xhttp.status == "200") {
            var res = xhttp.responseText;
            console.log(res);
            window.location.href="page1.html";            
          } 
          else if(xhttp.readyState == 4) {
            document.getElementById("username").value="";
            document.getElementById("password").value="";
            alert("Invalid Credentials");

          }

      }

    xhttp.send(json);
}
