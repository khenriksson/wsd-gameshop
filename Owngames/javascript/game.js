
// getting the canvas element from html and configuring it to 2D
var taulu= document.getElementById("taulu");
var tx= taulu.getContext("2d");




// configurable game elements. 
var sizeL=60;
var sizeW=60;
var hyppy=150;
var lim=200-sizeL;
var x=200-sizeL;
var move= 0;


//score and startinstance- our loop- variable so we can also stop it. 
var score=0;
var myfun;

function jump(){
	var i;
	// function for jumping.
	
	x=lim-hyppy;
	}


function roni(){
	// main character 
	tx.beginPath();
	tx.rect(100,x,sizeW,sizeL);
	tx.fillStyle="#000000";
	tx.fill();
	tx.closePath();
	// Floor
	tx.beginPath();
	tx.rect(0,200,500,2);
	tx.fillStyle="#000000";
	tx.fill();
	tx.closePath();
	
	
	
	}
// space is set for jumping and You can't double jump.
document.body.onkeyup=function(e){
	
	if(e.keyCode==32 && x==lim ){
		
		jump();
		
		}
	}



function stopgame(){
	
	
	clearInterval(myfun);
	tx.font="30px Arial";
	tx.fillText("GAME OVER Your score is: "+score.toFixed(0),50,50);
	// Now send score to server->
	var pisteet= {
		"messageType":"SCORE",
		"score":score.toFixed(0)
				
		};
	 
	window.parent.postMessage(pisteet,"*");
	
	var searchBt= document.getElementById('Bt');
	searchBt.onclick=function() {StartGame(); this.onclick=null;};

	searchBt.innerText="Wanna play again?";
	
	}


function blocks(speed,size){
	//create blocks
	var DarcX=taulu.width-move*speed;
	
	tx.beginPath();
	tx.arc(DarcX,lim+10, size, 0, Math.PI*2);
	tx.fillStyle="#ff0000";
	tx.fill();
	tx.closePath();
	move=move+ 1;
	if(DarcX<-size){
		move=0;
		}
	 
// Checking for collision: if ball is closer than 60px collision happens and its over. 
	
	
	var distX=100-(DarcX);
	var distY=x-(lim+10);
	
	
	
	var Distc= Math.sqrt(distX*distX+ distY*distY);
	
	if(Distc<110){
		
		stopgame();
		}
	
	
	}


function createStage(){
	
	// Idea was to create randomly generated world
	blocks(2,50);
	
	
	
	
	/*
	var num= score.toFixed(0)%100;
	//console.log(num);
	if(num==50){
		blocks(6,60);
		}
		* 
		* */
	}

function forward(){
	// Basically Main function that is called in every 10 ms	
	tx.clearRect(0,0,taulu.width,taulu.height);
	tx.font="10px Arial";
	tx.fillText("Score: "+score.toFixed(0),10,20)
	createStage();
	roni();

	// game run time and bringing character back to floor.
	if(x!= lim){
		x+=0.5;
		}
	score+=0.3;
}


function StartGame(){
	//var searchBt= document.getElementById('Bt');
	//searchBt.remove();
	score=0;
	move=0;
	x=lim
	myfun= setInterval(forward,10);
	
	
	}


tx.font="30px Arial";
tx.fillText("Start the game by pressing Start button: ",50,100);
var viesti = {
	messageType: "SETTING",
	options:{"width":600,
		"height":300}}




// starting from here,
//
