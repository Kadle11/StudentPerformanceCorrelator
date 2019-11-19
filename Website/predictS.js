var url = "http://localhost:70";

function predict()
{
	var api=url + "/api/v1/predict";
	var sub = document.getElementById("sub").value;
	var marks = document.getElementById("marks").value;
	console.log(sub);
	console.log(marks);
  var curl=api +"?"+"Subject="+ sub + "&" + "Score=" + marks;
  console.log(curl);
	data={};
  data["Subject"]=sub;
  data["Score"]=marks;
	var json= JSON.stringify(data);
	console.log(json);
  console.log(api);

	var xhttp = new XMLHttpRequest();
    xhttp.open("GET", curl, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');

    xhttp.onreadystatechange = function () {

          if (xhttp.readyState == 4 && xhttp.status == "200") {
            var res = xhttp.responseText;
            res = res.split('"').join('');
            var str=res.split(',');
            
            for(var i=0;i<str.length;i++)
            {
            	console.log(str[i]);
            }
            
            var list1=str[0].split(':');
            console.log(list1[0]);
            console.log(list1[1]);

            if(str[1]){

            	var list2=str[1].split(':');
            	console.log(list2[0]);
            	console.log(list2[1]);
            }
            if(str[1])
            {
            	if(list2[1]==1)
            	{

            	res= "The Predicted marks in "+list1[0]+ " is"+ list1[1] + " and the student is Interested in Sports";
        		}
        		else if(list2[1]=='0')
        		{
        		res= "The Predicted marks in "+list1[0]+ " is"+ list1[1] + " and the student is Not Interested in Sports";
        		}
        	}
        	else
        	{
        		res= "The Predicted marks in "+list1[0]+ " is"+ list1[1];
        	}
     
            var response = document.getElementById("result");
            response.innerHTML=res;
            
          } 
          else if(xhttp.readyState == 4) {
            alert("Error");
          }

      }

    xhttp.send(json);
}
