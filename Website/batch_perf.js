var url = "http://localhost:70";

function correlate()
{
	var api=url + "/api/v1/correlate";
	var sub_1 = document.getElementById("cat1").value;
	var sub_2 = document.getElementById("cat2").value;
	console.log(sub_1);
	console.log(sub_2);
    var curl=api +"?"+"S1="+ sub_1 + "&" + "S2=" + sub_2;
    console.log(curl);
    
	console.log(curl);
	var xhttp = new XMLHttpRequest();
    xhttp.open("GET", curl, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');

    xhttp.onreadystatechange = function () {

         
          if (xhttp.readyState == 4 && xhttp.status == "200") {
            var res = xhttp.responseText;
            console.log(res);
            var list=JSON.parse(res);
            
            var response = document.getElementById("result");
            if(list[0] > 0.5)
            {
            	response.innerHTML = "There is a significant relationship among these 2 Subjects<br /> The Correlation Score between them is "+list[0]
            }
            
            else
            {            	
            	response.innerHTML = "There is no relationship among these 2 Subjects<br /> The have a low Correlation Score of "+list[0]
            }

            var img_source="http://localhost/Plots/"+sub_1+"_vs_"+sub_2+".png"
            console.log(img_source);

            
            var image = document.getElementById("image");
            image.setAttribute("src",img_source);

                       
          } 
          else if(xhttp.readyState == 4) {
            alert("Error");
          }

      }

    xhttp.send();
}
