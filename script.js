window.onload = function() {
	
	//Load Hidden Test Images from Files
	var imgnames = ['bgl','cct','dbm','dkp','drv','evw','grf','lts','mom','ms','ptm','svc','tdy','tsc','vsn'];
	var imgs = [];
	var imgfeatures = [];
	var loaded = 0;
	for (var i = 0 ; i < imgnames.length ; i++){
		let imgname = 'resources/test_web/'+imgnames[i]+'_ima.png';
		let img = new Image();
		img.src = imgname
		img.onload = function () {
			loaded += 1;
		}
		imgs.push(img)
	}
	
	//Video Feed From Webcam
	var webcam_feed = document.getElementById("webcam_feed");
	
	var cam_working = false;
	
	if (navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ video: true })
			.then(function (stream) {
				webcam_feed.srcObject = stream;
				cam_working = true;
			})
			.catch(function (err0r) {
				console.log("Something went wrong!");
				cam_working = false;
			});
	}
	
	//Setup for Corner Testings
	var vid_width;
	var vid_height;
	var canvas = document.getElementById('canvas');
	var context = canvas.getContext('2d');
	//var image = document.getElementById('image');
	var vid_temp = document.createElement("CANVAS");
	var pic_temp = document.createElement("CANVAS");
	
	
	var ft = 25;
	
	//Button to Process Frame of Webcam Video
	scan_button = document.getElementById('scan_button');
	scan_button.onclick = function () {
		if (!cam_working){
			console.log('camera not working yet')
		} else {
			vid_width = webcam_feed.videoWidth;
			vid_height = webcam_feed.videoHeight;
			canvas.width = vid_width;
			canvas.height = vid_height;
			var vid_features = findFeaturesVid(webcam_feed,ft,256,vid_temp);
			var vid_corners = vid_features.corners;
			console.log("Features Detected:",vid_corners.length/2);
			context.drawImage(webcam_feed, 0, 0, vid_width, vid_height);
			for (var i = 0; i < vid_corners.length; i += 2) {
					context.fillStyle = 'lime';
					context.fillRect(vid_corners[i], vid_corners[i + 1], 3, 3);
			}
		}
	}
	
	//Button to compare Webcam Image to Test Files
	match_button = document.getElementById('match_button');
	match_button.onclick = function () {
		if (loaded < 15) {
			console.log('Not all pics loaded yet')
		} else if (!cam_working) {
			console.log('camera not working yet')
		} else {
			let vid_features = findFeaturesVid(webcam_feed,ft,256,vid_temp);
			// let best_name = 'none';
			// let best_matches = 0;
			// let best_i = 0;
			for (var i = 0; i < imgs.length; i++) {
				let img = imgs[i];
				let pic_features = findFeaturesPic(img,ft,256,pic_temp);
				let good_matches = matchFeatures(vid_features.corners,vid_features.descriptors,pic_features.corners,pic_features.descriptors,0.75)
				console.log(imgnames[i],good_matches.length)
			}
		}
	}
}