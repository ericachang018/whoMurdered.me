var tfgSnow = function(){	
	var doc = document;
	var canvas = doc.createElement('canvas');
	var cWidth = 1200;
	var cHeight = 1104;
	canvas.width = cWidth;
	canvas.height = cHeight;	
	$('#canvas-holder').append(canvas);	
	var ctx = canvas.getContext('2d');
	
	var snow = [];
	var snowCount = 450;
	var snowSizeMin = 50;
	var snowSizeMax = 250;
	var snowXSpeedMin = -25;
	var snowXSpeedMax = 25;
	var snowYSpeedMin = 50;
	var snowYSpeedMax = 125;
	var snowXSpeedChangeMin = -25;
	var snowXSpeedChangeMax = 25;
	var snowYSpeedChangeMin = 0;
	var snowYSpeedChangeMax = 50;	
	var snowAlphaMin = 10;
	var snowAlphaMax = 100;
	
	var mx = 0;
	var trail = false;
	
	function init(){
		createSnow();
		animationLoop();
	}
	
	function createSnow(){
		while(snowCount--){
			var newSize = rand(snowSizeMin, snowSizeMax)/100;
			var newX = rand(-1*(cWidth/8), cWidth+(cWidth/8));
			var newY = rand(cHeight*-1, (newSize/2)*-1);
			var newXSpeed = rand(snowXSpeedMin, snowXSpeedMax)/100;
			var newYSpeed = rand(snowYSpeedMin, snowYSpeedMax)/100;
			var newXSpeedChange = rand(snowXSpeedChangeMin, snowXSpeedChangeMax)/100;
			var newYSpeedChange = rand(snowYSpeedChangeMin, snowYSpeedChangeMax)/100;			
			var newAlpha = rand(snowAlphaMin, snowAlphaMax);
			snow.push({
				size: newSize,
				x: newX,
				y: newY,
				xSpeed: newXSpeed,
				ySpeed: newYSpeed,
				xSpeedChange: newXSpeedChange,
				ySpeedChange: newYSpeedChange,
				alpha: newAlpha
			});
		}
	}
	var yAdd = 0;
	var refill = 1;
	function draw(){
		var i = snow.length;
		if(trail){
			ctx.globalCompositeOperation = 'destination-out';
			ctx.fillStyle = 'rgba(0,0,0,'+refill+')';
			ctx.fillRect(0,0,cWidth,cHeight);
			if(yAdd < .2){
				yAdd += .005;
			}
			if(refill > .1){
				refill -= .02;
			}
			if(refill < .1){
				refill = .1;	
			}
		} else {		
			ctx.globalCompositeOperation = 'destination-out';
			ctx.fillStyle = 'rgba(0,0,0,'+refill+')';
			ctx.fillRect(0,0,cWidth,cHeight);
			if(yAdd > 0){
				yAdd -= .01;
			}
			if(yAdd < 0){
				yAdd = 0;	
			}
			if(refill < 1){
				refill += .02;
			}
			
			if(refill > 1){
				refill = 1;
			}
		}
		while(i--){
			var flake = snow[i];
			ctx.globalCompositeOperation = 'source-over'
			ctx.fillStyle = 'hsla(0, 100%, 100%, '+flake.alpha/100+')';
			ctx.beginPath();
			ctx.arc(flake.x,flake.y,flake.size,0, Math.PI*2, true)
			ctx.closePath();
			ctx.fill();		
			
			flake.x += flake.xSpeed + mx/600;
			flake.y += flake.ySpeed;
			if(flake.y > 0){
				flake.xSpeed += flake.xSpeedChange/100;
				flake.ySpeed += flake.ySpeedChange/100 + yAdd;
			}
						
			if(flake.y-(flake.size) > cHeight){
				var resetSize = rand(snowSizeMin, snowSizeMax)/100;
				flake.size = resetSize;
				flake.x = rand(-1*(cWidth/8), cWidth+(cWidth/8));
				flake.y = -resetSize;
				flake.xSpeed = rand(snowXSpeedMin, snowXSpeedMax)/100;
				flake.ySpeed = rand(snowYSpeedMin, snowYSpeedMax)/100;
				flake.xSpeedChange = rand(snowXSpeedChangeMin, snowXSpeedChangeMax)/100;
				flake.ySpeedChange = rand(snowYSpeedChangeMin, snowYSpeedChangeMax)/100;				
				flake.alpha = rand(snowAlphaMin, snowAlphaMax); 
			}	
		}
	}
	
	$(window).mousemove(function(e){
		mx = Math.floor(e.pageX - $('canvas').offset().left - cWidth/2);
	});
	
	$(window).bind({
		mousedown: function(){
			trail = true;
		},
		mouseup: function(){
			trail = false;
		}
	});	
	
	var animationLoop = function(){
		draw();
		requestAnimFrame(animationLoop, canvas);
	}
	
	window.requestAnimFrame=function(){return window.requestAnimationFrame||window.webkitRequestAnimationFrame||window.mozRequestAnimationFrame||window.oRequestAnimationFrame||window.msRequestAnimationFrame||function(a){window.setTimeout(a,1E3/60)}}();
	var rand = function(rMi, rMa){return ~~((Math.random()*(rMa-rMi+1))+rMi);}
	
	init();
}