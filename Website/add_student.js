var url = "http://localhost:70";

function insert()
{
  var api=url + "/api/v1/student";
  var fname = document.getElementById("fname").value;
  var lname = document.getElementById("lname").value;
  var math = document.getElementById("math").value;
  var chem = document.getElementById("chem").value;
  var bio = document.getElementById("bio").value;
  var comp = document.getElementById("cs").value;
  var sports = document.getElementById("sports").value;
  console.log(fname);
  console.log(lname);
  console.log(math);
  console.log(chem);
  console.log(bio);
  console.log(comp);
  console.log(sports);
  var curl=api;
  console.log(curl);
  data={};
  data["FName"]=fname;
  data["LName"]=lname;
  data["Math"]=math;
  data["Chem"]=chem;
  data["Bio"]=bio;
  data["CS"]=comp;
  data["Sports"]=sports;
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

            var response = document.getElementById("result");
            response.innerHTML="Student Details Inserted into Database";

            document.getElementById("fname").value = "";
            document.getElementById("lname").value = "";
            document.getElementById("math").value = "";
            document.getElementById("chem").value = "";
            document.getElementById("bio").value = "";
            document.getElementById("cs").value = "";
            var ele = document.getElementsByName("Choose");
   			for(var i=0;i<ele.length;i++)
   			{
      			ele[i].checked = false;
   			}
            
            
          } 
          else if(xhttp.readyState == 4) {
            alert(res);
          }

      }

    xhttp.send(json);
}
