var url = "http://localhost:70";

function insert()
{
	var api=url + "/api/v1/users";
	var username = document.getElementById("username").value;

 
	console.log(fname);

  var curl=api +"?"+"userName="+ username;
  console.log(curl);
	data={};
  data["uname"]=username;

	var json= JSON.stringify(data);
	console.log(json);
  console.log(api);

	var xhttp = new XMLHttpRequest();
    xhttp.open("GET", curl, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');

    xhttp.onreadystatechange = function () {

         
          if (xhttp.readyState == 4 && xhttp.status == "200") {
            var res = xhttp.responseText;
            console.log(res);

            var response = document.createElement("div");
            response.innerHTML=xhttp.responseText;
            document.getElementById("result").appendChild(response);
            
          } 
          else if(xhttp.readyState == 4) {
            alert(res);
          }

      }

    xhttp.send(json);
}
