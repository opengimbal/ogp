
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8" />
<style type="text/css">
#up {	
	height: 5em;
	width: 544px;
	background-color: transparent;
	font-size: 80%;
	font-weight: bold;
	color: #ffffff;
}
#down {	
	height: 5em;
	width: 544px;
	background-color: transparent;
	font-size: 80%;
	font-weight: bold;
	color: #ffffff;
}
#left {	
	
	height: 288px;
	width: 145px;
	background-color: transparent;
	font-weight: bold;
	color: #ffffff;
}
#right {	
	
	height: 288px;
	width: 145px;
	background-color: transparent;
	font-weight: bold;
	color: #ffffff;
}
input.pic1 {	
	height: 5em;
	width: 145px;
	background-color: transparent;
	font-size: 80%;
	font-weight: bold;
	color: #ffffff;
}
input.stop1 {	
	height: 5em;
	width: 145px;
	background-color: transparent;
	font-size: 80%;
	font-weight: bold;
	color: #ffffff;
}
input.stop2 {	
	height: 5em;
	width: 145px;
	background-color: red;
	font-size: 80%;
	font-weight: bold;
	color: #ffffff;
}
div.centre
{ 
	background-image:url('ogp2gui.jpg');
	display: block;
	margin-left: auto;
	margin-right: auto;
	max-height: 3000px; 
	max-width: 850px;
	min-width: 850px;
	min-height: 600px;
}

input.padbutton
{ 
width:80px;
 color:white;
 height:100px;
}
input.padbutton2
{ 
width:100px;
 color:black;
 height:100px;
 background-color: red;
}


input.padbutton3
{ 
width:80px;
 color:white;
 height:30px;
}
input.padbutton6
{ 
width:80px;
 color:white;
 height:100px;
 background-color: yellow;
}

input.padbutton4
{ 
width:100px;
 color:white;
 height:30px;
}

div.bottom{
	max-height: 250px;
	columns: 200px 3 ;
	-webkit-columns: 200px 3;
}
body {	
	
	text-align: center;
	background-color: #000000;
     }

</style>

<script src="http://192.168.42.1/jquery-1.11.0.min.js"></script>
<script>
      var chasing = "n";
      var chx = 277;
      var chy = 144;
      var mapping = "n";
      var mapx =  "0";
      var mapy = "0";
      var dgear = "o";

      $(function(){
       var ws;
       var logger = function(msg){
         var now = new Date();
         var sec = now.getSeconds();
         var min = now.getMinutes();
         var hr = now.getHours();
	 
         $("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " " + msg  );
	 $("#log").scrollTop($("#log")[0].scrollHeight);
	 var h = "n";

	 packet = msg.toString();
	 var res = packet.split("_", 4);

	 var h = res.slice(0,1);

	 var x = res.slice(1,2);
	 var y = res.slice(2,3);
	 var p = res.slice(3,4);

	 
	 var xpos = parseInt(x);
	 var ypos = parseInt(y);


	 var c = document.getElementById("myCanvas");
	 var ctx = c.getContext("2d");
	 xpos = xpos * 20;
	 ypos = -ypos * 20 ;
	 var x2 = xpos + 20;
	 var y2 = ypos + 20;
	 var y3 = ypos + 35;
	 var d = "d";
	 var c2 = "c";
	 var no = "n";
	 var yes = "y";
	 h = h.slice(0,1);
	 var thp1 = "/images/thumbs/thumb";
	 var thp2 = ".png";
	 var thumbpath = thp1.concat(p,thp2);
         
         $("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " " + mapping + ","+chy  );
	 $("#log").scrollTop($("#log")[0].scrollHeight);
	if (h == "m"){
	 if (mapping == "y"){
	    ws.send("b");
	 } else if(mapping == "n"){
	 }
	 }
	 if (h == "d"){
	  var imageObj = new Image();
	  imageObj.onload = function(){
	    ctx.drawImage(imageObj, xpos, ypos);
	    ctx.fillStyle = "#ffffff";
	    ctx.font="10px Arial";
	
	    ctx.fillText(p, xpos, y3);
	   };
	  imageObj.src = thumbpath;
	  
	 }
	 if (x == "u"){
           chy = chy - 5;
		}	   
	 if (x == "d"){
           chy = chy + 5;
		}
	 if (x == "l"){
           chx = chx - 5;
		}
	 if (x == "r"){
           chx = chx + 5;
		}
         if (h == "m"){

		}
	 if (h == c){

		}

	 if (chasing == "y"){
	    ws.send("c");
  	    ctx.fillStyle = "#ffffff";
	    ctx.font="10px Arial";
	
	    ctx.fillText("x", chx, chy) ;
	}
	}

	
	

	var sender = function() {
	  var msg = $("#msg").val();
	  if (msg.length > 0)
	    ws.send(msg);
	   $("#msg").val(msg);
	}
	
	ws = new WebSocket("ws://192.168.42.1:8888/ws");
	ws.onmessage = function(evt) {

	  logger(evt.data);
	};
	ws.onclose = function(evt) {
	    $("#log").text("Connection Closed");
	    $("#thebutton #msg").prop('disabled', true);
	};
	ws.onopen = function(evt) { 
	   $("#log").text("OGP-- SOCKET OPEN"); 
	   	  ws.send('n');
	   
	};

	$("#msg").keypress(function(event) {
	    if (event.which == 13) {
	      sender();
	    }
	});

	$("#up").click(function(){
	 if (dgear == "n"){
	    
	  ws.send('y');
         }
	 if (dgear == "m"){
	  ws.send('w');
	 }    
	 if (dgear == "o"){
	  ws.send('7');

	 }
	 });

	$("#down").click(function(){
	 if (dgear == "n"){
	    
	  ws.send('g');
         }
	 if (dgear == "m"){
	  ws.send('z');
	 }    
	 if (dgear == "o"){
	  ws.send('9');

	 }
	});

	$("#left").click(function(){
	 if (dgear == "n"){
	    
	  ws.send('h');
         }
	 if (dgear == "m"){
	  ws.send('a');
	 }    
	 if (dgear == "o"){
	  ws.send('2');

	 }
	});

	$("#right").click(function(){
	 if (dgear == "n"){
	    
	  ws.send('j');
         }
	 if (dgear == "m"){
	  ws.send('s');
	 }    
	 if (dgear == "o"){
	  ws.send('4');
	
	 }
	});

	$("#in").click(function(){
	    ws.send('f');
	});

	$("#out").click(function(){
	    ws.send('t');
	});

	$("#short").click(function(){
	    
	    dgear = "n";


	});

	$("#long").click(function(){	


	  
	    dgear = "m";
	});
	$("#open").click(function(){

	    dgear = "o";
	});
	$("#map").click(function(){
	    ws.send('n');

	});

	$("#chase").click(function(){
	 var yes = "y";
	 var no = "n";

	 if (chasing == no){
	  
	  chasing = yes;
	  mapping = no;

          ws.send('c');
	} else if (chasing == yes){
	  chasing = no;
	  ws.send('3');
	 
	}
	});
	$("#map2").click(function(){
	 var yes = "y";
	 var no = "n";
	 if (mapping == no){
	  mapping = yes; 
	  chasing = no;
          ws.send('b');
	} else if (mapping == yes){
	  mapping = no;
	  ws.send('3');

	 
	}
	});


	$("#autocal").click(function(){
	    chasing = "n";
	    mapping = "n";
	    ws.send('k');
	});

	$("#allstop").click(function(){

	    chasing = "n";
	    ws.send('3');
	   var ch = 0;
	});

	$("#allstop2").click(function(){

	    ws.send('8');
	});

	$("#mapsizea").click(function(){
	    ws.send('p');
	
	});

	$("#mapsizeb").click(function(){
	    ws.send('l');
	
	});

	$("#don").click(function(){
	    ws.send('9');

	});

	$("#lon").click(function(){
	    ws.send('2');

	});


	$("#ron").click(function(){
	    ws.send('4');

	});
	$("#pic1").click(function(){
	    ws.send('v');

	});
	$("#pic2").click(function(){
	    ws.send('x');

	});

	$("#thebutton").click(function(){
	    sender();
	});
     });
   </script>
</head>

<body>
 <div class="centre" id="main">
  <div id="top">
  <input type="image" class="pic1" id="pic2" value="PIC-" />
  <input type="image" id="up" value="UP" /<br>
  <input type="image" class="pic1" id="pic1" value="PIC+" />
  </div>

  <div id="middle">
  <input type="image" id="left" value="LEFT"  ;/>
  <iframe src="http://192.168.42.1:8080" width="544" height="288" frameborder="0" scrolling="no">...</iframe>
  <input type="image" id="right" value="RIGHT"  />
  </div>

  <div>
  <input type="image" class="stop1" id="allstop" value="STOP X" />
  <input type="image" id="down" value="DOWN" />
  <input type="image" class="stop1" id="allstop2" value="STOP Y" />
  </div>

  <div id="bottom" class="bottom">
   <div id="padleft">

   <input class= "padbutton" type="image" id="short" value="NUDGE" />
   <input class= "padbutton" type="image" id="long" value="MAP STEP" />
   <input class= "padbutton6" type="image" id="open" value="OPEN GEAR" />
   <input class= "padbutton" type="image" id="map" value="NEW MAP" />

   <input class= "padbutton" type="image" id="map2" value="MAP ON/OFF" />
   <input class= "padbutton" type="image" id="chase" value="CHASE" /><br><br>
     <div id="log" style="overflow:scroll; width:100%; height:100px; color:white; background-color:#000000; margin: 1px; text-align:left">Messages go Here </div>
 <br><input type="text" id="msg" style=" color:white; background-color:#000000; height: 100%; width:60% " />
   <input type="image" id="thebutton" class= "padbutton3" value="SEND" /><br><br>
  <input class= "padbutton4" type="image" id="manual" value="MANUAL" />  
 <input class= "padbutton4" type="image" id="in"  value="PIC FOLDER" />
    <input class= "padbutton" type="image" id="in"  value="IN" />
   <input class= "padbutton" type="image" id="out" value="OUT" />
  <input class= "padbutton" type="image" id="cam2" value="CAM 2" />




  <input class= "padbutton" type="image" id="autocal" value="AUTOCAL" />

   <input class= "padbutton" type="image" id="mapsizea" value="MAPSIZE+" />
   <input class= "padbutton" type="image" id="mapsizeb" value="MAPSIZE-" />

</div>
    </div>
<div>
<canvas id="myCanvas" width="544" height="544" style="border:1px solid#ffffff;"></canvas><canvas id="myCanvas" width="544" height="288" style="border:1px solid#000000;"></canvas>
</div>

</body>
</html>
##(c) Copyright 2014   C. Robert Barnett III
