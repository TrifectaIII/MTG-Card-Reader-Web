var findFeatures = function(fast_threshold, vidfeed) {
	var vid_width = vidfeed.videoWidth;
	var vid_height = vidfeed.videoHeight;
	tracking.Fast.THRESHOLD = fast_threshold;
	var temp = document.createElement("CANVAS");
	temp.width = vid_width;
	temp.height = vid_height;
	var temp_context = temp.getContext('2d');
	temp_context.drawImage(vidfeed,0,0,vid_width,vid_height);
	var imageData = temp_context.getImageData(0, 0, vid_width, vid_height);
	var gray = tracking.Image.grayscale(imageData.data, vid_width, vid_height);
	var corners = tracking.Fast.findCorners(gray, vid_width, vid_height);
	var descriptors = tracking.Brief.getDescriptors(gray,vid_width,corners)
	console.log("Features Detected:",corners.length);
	var features = {
		corners:corners,
		descriptors:descriptors
		}
	return features;
};