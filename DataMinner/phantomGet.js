var page = require('webpage').create();
var fs = require('fs');
var url = fs.read('d:/url.txt');
console.log('The default user agent is ' + page.settings.userAgent);
page.settings.userAgent = 'SpecialAgent';
page.open(url, function(status) {
  if (status !== 'success') {
    console.log('Unable to access network');
  } else {
    var ua = page.evaluate(function() {
	  var con = document.getElementsByTagName('html')[0].innerHTML;
	  return "<html>" + con + "</html>"
    });
    console.log(ua);
	var path = 'd:/output.html';
    fs.write(path, ua, 'w');
  }
  phantom.exit();
});