var page = require('webpage').create();
var fs = require('fs');
var url = fs.read('d:/url.txt');
console.log(url);
page.settings.userAgent = 'SpecialAgent';
page.open(url, function(status) {
  if (status !== 'success') {
    console.log('Unable to access network');
  } else {
	window.setTimeout(function () {
			console.log("phantom get url:" + url)
			var ua = page.content;
			var path = 'd:/output.html';
			fs.write(path, ua, 'w');
			fs.write('d:/flag', '0', 'w');
			phantom.exit();
          }, 30000);
  }
});