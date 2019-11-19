var url = "http://localhost:70";

function Search()
{
  var url = "http://localhost:70";

 	var api=url + "/api/v1/search";
  var fname = document.getElementById("fname").value;
  var lname = document.getElementById("lname").value;
	var value, pvalue;
    
  if((lname=="") || (fname==""))
  {
    alert("Please Fill all Fields");
    return;
  }

  data={};
  value=3;
  data["Field"]=3;
  pvalue= fname + "," + lname;
  data["pValue"]=pvalue;

	console.log("P1: ", fname);
	console.log("P2: ", lname);


  var curl=api +"?"+"Field="+ value + "&" + "pValue=" + pvalue;
  console.log("Point X:", curl);
  
	var xhttp = new XMLHttpRequest();
    xhttp.open("GET", curl, true);
    xhttp.setRequestHeader('Content-type','application/json; charset=utf-8');

    xhttp.onreadystatechange = function () {

         
          if (xhttp.readyState == 4 && xhttp.status == "200") {
            var res = xhttp.responseText;
            console.log(res);
            var list=JSON.parse(res);
            console.log(list[0]);
            
            var table = document.getElementById("result");
            table.style.visibility= 'visible';

            var a = document.getElementById("a");
            var b = document.getElementById("b");
            var c = document.getElementById("c");
            var d = document.getElementById("d");
            var e = document.getElementById("e");
            var f = document.getElementById("f");
            var g = document.getElementById("g");
            var h = document.getElementById("h");

            a.innerHTML=list[0].split('"').join('');
            b.innerHTML=list[1].split('"').join('');
            c.innerHTML=list[2].split('"').join('');
            d.innerHTML=list[3].split('"').join('');
            e.innerHTML=list[4].split('"').join('');
            f.innerHTML=list[5].split('"').join('');
            g.innerHTML=list[6].split('"').join('');
            if(list[7]=="1")
            {
              h.innerHTML="Interested";
            }
            else
            {
              h.innerHTML="Not Interested";
            }
            






            //response.innerHTML=res; 
          } 
          else if(xhttp.readyState == 4) {
            alert("Error");
          }

      }

    xhttp.send();
}

function Suggest()
{

  var api=url + "/api/v1/search";
 
 
  this.xhr = new XMLHttpRequest();
  this.timer = null;
  Field = this.Field
  XHR = this.xhr
  Obj = this
  this.getTerm=function(FieldS)
  {
    Field = FieldS;
    console.log("Point A : "+ Field)
    if(this.timer)
    {
      clearTimeout(this.timer);
    }
    this.timer=setTimeout(this.sendTerm, 1000)
  }

  this.sendTerm=function()
  {
    console.log("Point B : "+ Field)
    if(Field==1)
    {
      this.fname = document.getElementById("fname").value;
      this.url = api+"?Field="+ Field + "&" + "pValue="+this.fname;
      console.log(this.url) 
    }
    else if(Field==2)
    {
      this.lname = document.getElementById("lname").value;
      this.url = api+"?Field="+ Field + "&" + "pValue="+this.lname;
    }
    
    XHR.open("GET", this.url, true)
    XHR.setRequestHeader('Content-type','application/json; charset=utf-8');
    XHR.send()
    Obj.showSuggestions()
  }

  this.showSuggestions=function()
  {
    XHR.onreadystatechange= function()
    {
      if(XHR.readyState==4 && XHR.status=="200")
      {
          if(Field==1)
          {

            document.getElementById("datalist1").innerHTML="";
            var response = JSON.parse(XHR.responseText)
            
            var len = Math.min(5, response.length)
            for(var i=1; i<len+1; i++)
            {
              console.log(response[i-1])
              var node = document.createElement("option"); 
              var val = document.createTextNode(response[i-1]); 
              node.appendChild(val); 
              console.log(document.getElementById("datalist1"))
              document.getElementById("datalist1").appendChild(node);         
            }
          }

          if(Field==2)
          {

            document.getElementById("datalist2").innerHTML="";
            var response = JSON.parse(XHR.responseText)
            
            var len = Math.min(5, response.length)
            for(var i=1; i<len+1; i++)
            {
              console.log(response[i-1])
              var node = document.createElement("option"); 
              var val = document.createTextNode(response[i-1]); 
              node.appendChild(val); 
              console.log(document.getElementById("datalist2"))
              document.getElementById("datalist2").appendChild(node);         
            }
          }

      }
    }
  }

}

var obj = new Suggest()


