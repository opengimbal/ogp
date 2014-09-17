<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8" />
<style type="text/css">
#up {	
	height: 5em;
	width: 181px;
	background-color: transparent;
	font-size: 80%;
	font-weight: bold;
	color: #ffffff;
}
#down {	
	height: 5em;
	width: 181px;
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
input.stepsize {	
	height: 5em;
	width: 100px;
	background-color: transparent;
	font-size: 80%;
	font-weight: bold;
	color: #ffffff;
}
input.up2 {	
	height: 5em;
	width: 177px;
	background-color: transparent;
	font-size: 80%;
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

<script src="http://192.168.42.1/jquery-1.11.0.min.js"></script><!--make sure this .js file is in the folder with this php file-->
<script>
      var chasing = "n";           // sets default state as "not chasing anything"
      var chx = 277;             // variables involved in chasing
      var chy = 144;              // variables ivolved in chasing
      var mapping = "n";             //sets default state as "not mapping"
      var mapx =  "0";            // variables involved in mapping
      var mapy = "0";              // variables involved in mapping
      var dgear = "s";                // sets default gear as "none"

      $(function(){                     //main loop
       var ws;                           // declare websocket
       var logger = function(msg){                   // this function runs when a message comes in
         var now = new Date();                 // gets date info from browser system
         var sec = now.getSeconds();               //gets time info
         var min = now.getMinutes();               //gets time info
         var hr = now.getHours();                 // gets time info
	 
         $("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " " + msg  ); //displays message info (msg), date and time
	 $("#log").scrollTop($("#log")[0].scrollHeight);             //scrolls down one line on the "message field"
	 var h = "n";                   // h is the variable that will hold the first line of the incoming message

	 packet = msg.toString();           // here we begin to break up the message into parts (parsing)
	 var res = packet.split("_", 4);       //breaks up the packet of info into slices dvided by underscores(_)

	 var h = res.slice(0,1);                //grabs the first slice and puts it into variable h

	 var x = res.slice(1,2);                 //second slice - x position
	 var y = res.slice(2,3);                  //third slice - y position
	 var p = res.slice(3,4);                  //fourth slice - file number

	 
	 var xpos = parseInt(x);                       //turns variable x info into an integer
	 var ypos = parseInt(y);                       //turns variable y info into an integer


	 var c = document.getElementById("myCanvas"); // instanciates canvas as variable c for use in the javascript 
	 var ctx = c.getContext("2d");                  // this line lets you deal with the canvas 2D layer
	 xpos = xpos * 20;                       // new x position of new thumbnail on canvas
	 ypos = -ypos * 20 ;                       // new y position of new thumbnail on canvas
	 var x2 = xpos + 20;                         // new x position of new thumbnail on canvas
	 var y2 = ypos + 20;                        // new y position of new thumbnail on canvas
	 var y3 = ypos + 35;                        // position of numbering of thumbnail
	 var d = "d";                      // variables we use to compare variables, this is completely unnecessary
	 var c2 = "c";                    // variables we use to compare variables, this is completely unnecessary
	 var no = "n";                   // variables we use to compare variables, this is completely unnecessary
	 var yes = "y";                // variables we use to compare variables, this is completely unnecessary
	 h = h.slice(0,1);                                   // gets slice 0, again?
	 var thp1 = "/images/thumbs/thumb";                 // path to new thumb (address) - part one
	 var thp2 = ".png";                             //path to new thumb - part three
	 var thumbpath = thp1.concat(p,thp2);              // merges the parts of the path (concatonation)
         
         $("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " " + mapping + ","+chy  ); //message for message field
	 $("#log").scrollTop($("#log")[0].scrollHeight); // bumps the message field down one line
	if (h == "m"){             // if part one of the incoming message(h) is "m" then that means that we are mapping
	 if (mapping == "y"){            // if "y" then we continue to map
	    ws.send("b");            // send the letter "b" to the websocket(ws)- this requests that the mapping continue
	 } else if(mapping == "n"){                  // if you press the stop button then the mapping will cease
	 }
	 }
	 if (h == "d"){  // "d" declares that we are dropping a new thumb on the canvas
	  var imageObj = new Image(); // load the thumb into a variable
	  imageObj.onload = function(){  //waits for the thumb to load
	    ctx.drawImage(imageObj, xpos, ypos);  // once loaded it is drawn
	    ctx.fillStyle = "#ffffff";   // and then we draw the reference number next to it
	    ctx.font="10px Arial"; //
	    ctx.fillText(p, xpos, y3);  //
	   };
	  imageObj.src = thumbpath; // part of the image loading script, not sure what it does but its necessary
	  
	 }
	 if (x == "u"){   // if we are in chase mode, then x is the direction we have just moved
           chy = chy - 5;   // edits the chase position
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

	 if (chasing == "y"){  // if we are in chasing mode 
	    ws.send("c");  //send the signal to continue chasing
  	    ctx.fillStyle = "#ffffff";  //draw an x onto the canvas to represent the motion of the chasing
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
	$("#cam2").click(function(){

	    ws.send('c2');
	});
	$("#cam1").click(function(){

	    ws.send('c1');
	});
	$("#cam4").click(function(){

	    ws.send('c4');
	});
	$("#cam3").click(function(){

	    ws.send('c3');
	});
	$("#mapsizea").click(function(){
	    ws.send('p');
	
	});
	$("#cam2").click(function(){
	    ws.send('c2');
	
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
	$("#splus").click(function(){

	    ws.send('+');
	});
	$("#sminus").click(function(){

	    ws.send('-');
	});
     });
   </script>
</head>

<body>
 <div class="centre" id="main">
  <div id="top">
 <input type="image" class="pic1" id="pic2" value="PIC-" />
  <input type="image" class="up2" id="cam2" value="CAM2" />
  <input type="image" id="up" value="UP" /<br>
  <input type="image" class="up2" id="cam3" value="CAM3" />
  <input type="image" class="pic1" id="pic1" value="PIC+" />
  </div>

  <div id="middle">
  <input type="image" id="left" value="LEFT"  ;/>
  <iframe src="http://192.168.42.1:8080" width="544" height="288" frameborder="0" scrolling="no">...</iframe>
  <input type="image" id="right" value="RIGHT"  />
  </div>

  <div>
  <input type="image" class="stop1" id="allstop" value="STOP X" />
  <input type="image" class="up2" id="sminus" value="STEPSIZE-" />
  <input type="image" id="down" value="DOWN" />
  <input type="image" class="up2" id="splus" value="STEPSIZE+" />
  <input type="image" class="stop1" id="allstop2" value="STOP Y" />
  </div>

  <div id="bottom" class="bottom">
   <div id="padleft">

   <input class= "padbutton" type="image" id="short" value="NUDGE" />
   <input class= "padbutton" type="image" id="long" value="MAP STEP" />
   <input class= "padbutton" type="image" id="open" value="OPEN GEAR" />
   <input class= "padbutton" type="image" id="map" value="NEW MAP" />

   <input class= "padbutton" type="image" id="map2" value="MAP ON/OFF" />
   <input class= "padbutton" type="image" id="chase" value="CHASE" /><br><br>
     <div id="log" style="overflow:scroll; width:100%; height:100px; color:white; background-color:#000000; margin: 1px; text-align:left">Messages go Here </div>
 <br><input type="text" id="msg" style=" color:white; background-color:#000000; height: 100%; width:60% " />
   <input type="image" id="thebutton" class= "padbutton3" value="SEND" /><br><br>
  <input class= "padbutton4" type="image" id="manual" value="MANUAL" />  
 <input class= "padbutton4" type="image" id="picf"  value="PIC FOLDER" />
    <input class= "padbutton" type="image" id="in"  value="IN" />
   <input class= "padbutton" type="image" id="out" value="OUT" />
  <input class= "padbutton" type="image" id="cam1" value="CAM 1" />




  <input class= "padbutton" type="image" id="autocal" value="AUTOCAL" />

   <input class= "padbutton" type="image" id="mapsizea" value="MAPSIZE+" />
   <input class= "padbutton" type="image" id="mapsizeb" value="MAPSIZE-" />

</div>
    </div>
<div>


<canvas id="myCanvas" width="544" height="544" style="border:1px solid#000000;"></canvas>

</div>

</body>
</html>
