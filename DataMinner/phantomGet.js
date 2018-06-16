var page = require('webpage').create();
var fs = require('fs');
var url = fs.read('d:/url.txt');
page.settings.userAgent = 'SpecialAgent';
page.open(url, function(status) {
  if (status !== 'success') {
  } else {
    var ua = page.evaluate(function() {
	  var con = document.getElementsByTagName('html')[0].innerHTML;
	  return "<html>" + con + "</html>"
    });
	var path = 'd:/output.html';
    fs.write(path, ua, 'w');
    fs.write('d:/flag', '0', 'w')
  }
  phantom.exit();
});