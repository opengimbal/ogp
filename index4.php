	<!DOCTYPE HTML>
	<html>
	<head>
	<link rel="stylesheet" type="text/css" href="ogp.css">
	<meta charset="utf-8" />
	
	<script src="http://192.168.42.1/jquery-1.11.0.min.js"></script>
	<script>
	var chasing = false;
	var chx = 277;
	var chy = 144;
	var mapping ;
	var mapx = "0";
	var mapy = "0";
	var dgear = "n";
	
	
	
	$(function(){
	var ws;
	var logger = function(msg){
	var now = new Date();
	var sec = now.getSeconds();
	var min = now.getMinutes();
	var hr = now.getHours();
	
	$("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " " + msg );
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
	
	h = h.slice(0,1);
	var thp1 = "/images/thumbs/thumb";
	var thp2 = ".png";
	var thumbpath = thp1.concat(p,thp2);
	
	
	
	if (h == "m"){
	ws.send("b");
	}
	
	if (h == "live"){
	ws.send("live");
	}
	
	
	if (chasing == "1"){
	if (h == "c"){
	ws.send("c");
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
	if (h == "g"){
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
	var sender2 = function() {
	var msg2 = $("#msg2").val();
	if (msg2.length > 0)
	var msg3 = parseInt(msg2);
	msg3 = msg3 + 100;
	ws.send(msg3);
	$("#msg2").val(msg2);
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
	ws.send('golive');
	
	};
	
	$("#chase").click(function(){
	
	if (chasing == false){
	
	chasing = "1";
	mapping = false;
	
	ws.send('c');
	} else if (chasing == "1"){
	chasing = false;
	ws.send('3');
	
	}
	});
	
	
	$("#msg").keypress(function(event) {
	if (event.which == 13) {
	sender();
	}
	});
	
	$("#msg2").keypress(function(event) {
	if (event.which == 13) {
	sender2();
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
	ws.send('9');
	
	}
	if (dgear == "s"){
	ws.send('sqd');
	
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
	ws.send('7');
	}
	if (dgear == "s"){
	ws.send('squ');
	
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
	if (dgear == "s"){
	ws.send('sqr');
	
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
	if (dgear == "s"){
	ws.send('sql');
	
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
	ws.send('map');
	
	});
	$("#golive").click(function(){
	ws.send('golive');
	
	});
	
	
	
	$("#map2").click(function(){
	if (mapping == false){
	mapping = "1";
	chasing = false;
	ws.send('b');
	} else if (mapping == "1"){
	mapping = false;
	ws.send('3');
	
	}
	$("#log").html($("#log").html() + "<br/>" + (mapping.toString()) );
	$("#log").scrollTop($("#log")[0].scrollHeight);
	
	});
	
	
	$("#allstop").click(function(){
	chasing = "n";
	ws.send('3');
	var ch = 0;
	});
	
	$("#allstop2").click(function(){
	ws.send('8');
	});
	
	$("#position").click(function(){
	ws.send('mx');
	});
	
	$("#cam1").click(function(){
	ws.send('c3');
	});
	$("#cam4").click(function(){
	ws.send('c4');
	});
	
	$("#cam3").click(function(){
	ws.send('c2');
	});
	
	$("#mapsizea").click(function(){
	ws.send('p');
	
	});
	
	$("#cam2").click(function(){
	ws.send('c1');
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
	
	$("#sq").click(function(){
	dgear = "s";
	});
	});
	</script>
	</head>
	
	<body>
	<div class="centre" id="main">
	<div id="top">
	<input type="image" class="up3" id="golive" value="GOLIVE" />
	<input type="image" class="up3" id="null" value="NULL" />
	<input type="image" class="up3" id="cam1" value="CAM1" />
	<input type="image" class="up3" id="cam2" value="CAM2" />
	<input type="image" class="up" id="up" value="UP" />
	<input type="image" class="up3" id="cam3" value="CAM3" />
	<input type="image" class="up3" id="null" value="NULL" />
	<input type="image" class="up3" id="in" value="IN" />
	<input type="image" class="up3" id="out" value="OUT" />
	</div>
	
	<div id="middle">
	<input type="image" class="left" id="left" value="LEFT" />
	<iframe src="http://192.168.42.1:8080" width="544" height="288" frameborder="0" scrolling="no">...</iframe>
	<input type="image" class="right" id="right" value="RIGHT" />
	</div>
	
	<div>
	<input type="image" class="up3" id="allstop" value="STOP X" />
	<input type="image" class="up3" id="allstop2" value="STOP Y" />
	<input type="image" class="up3" id="null" value="NULL" />
	<input type="image" class="up3" id="null" value="NULL" />
	<input type="image" class="down" id="down" value="DOWN" /<br>
	<input type="image" class="up3" id="mapsizea" value="MAPSIZE+" />
	<input type="image" class="up3" id="mapsizeb" value="MAPSIZE-" />
	<input type="image" class="up3" id="null" value="NULL" />
	<input type="image" class="up3" id="map" value="MAP" />
	</div>
	
	<div id="bottom" class="bottom">
	<div id="padleft">
	
	<input class= "up3" type="image" id="open" value="OPEN" />
	<input class= "up3" type="image" id="chase" value="CHASE" />
	<input class= "up3" type="image" id="position" value="POSITION" />
	<input class= "up3" type="image" id="man" value="MANUAL" />
	<input class= "up3" type="image" id="picfolder" value="PICFOLDER" />
	<input class= "up3" type="image" id="thebutton" value="SEND" /><br><br><br> <div>
	<div id="log" style="font-family:arial; overflow:hidden; width:100%; height:150px; color:white; background-color:#000000; text-align:right;">OGP -stand by</div>
	</div> <input class= "up3" type="image" id="short" value="NUDGE" />
	<input class= "up3" type="image" id="long" value="STEP" />
	<input class= "up3" type="image" id="sq" value="SITE" />
	<input type="text" value="ALT" id="msg" style=" color:white; background-color:#000000; font-size: 30px; height: 50px; width:75% " />
	<input type="text" value="AZ" id="msg2" style=" color:white; background-color:#000000; font-size: 30px; height: 50px; width:75% " />
	
	</div>
	</div>
	<div style="color:white; font-family:arial; background-color:black; text-align:left;"><br><br>
	STEP SIZE (ms):
	<form>0ms<input id="slide" type="range" name="stepsize" style="width:100%;" min="0" max="900" step="50" value="200">900ms</form>
	<p id="result"></p>
	NUDGE SIZE (ms):
	<form>0ms<input id="slide" type="range" name="stepsize" style="width:100%;" min="0" max="900" step="50" value="200">900ms</form>
	<p id="result"></p>
	</div><div style="background-color:black;">
	
	<canvas id="myCanvas" width="544" height="544" style="border:1px solid#000000;"></canvas>
	
	</div></div>
	
	</body>
	</html>
