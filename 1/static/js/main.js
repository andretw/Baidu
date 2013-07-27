var win, wrapper, landing, maincontent, browserWidth, browserHeight, browserRatio;

$(document).ready(function()
{
	_createVars();
	_resizeHandler();
	win.bind("resize", _resizeHandler);

});

function _createVars()
{
	win				= $(window);
	wrapper			= $("#wrapper");
	landing			= $("#landing");
	maincontent		= $("#maincontent");
	browserWidth	= win.width(); //視窗寬
	browserHeight	= win.height() //視窗高
	browserRatio	= browserHeight / browserWidth; //視窗比
	screenWidth		= screen.availWidth //螢幕寬
	screenHeight	= screen.availHeight; //螢幕高
	viewportWidth	= screenWidth; //螢幕寬參考
	viewportHeight	= screenHeight; //螢幕高參考
}

function _resizeHandler()
{
	browserWidth = win.width(); 
	browserHeight = win.height(); 
	browserRatio = browserHeight / browserWidth;
	landing.css({ "width":browserWidth, "height":browserHeight });
}