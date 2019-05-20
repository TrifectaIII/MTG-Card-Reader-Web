var findFeaturesVid = function(vidfeed, fast_threshold, brief_length) {
	
	// Set Algorithm States
	tracking.Fast.THRESHOLD = fast_threshold;
	tracking.Brief.N = brief_length;
	
	var vid_width = vidfeed.videoWidth;
	var vid_height = vidfeed.videoHeight;
	var temp = document.createElement("CANVAS");
	temp.width = vid_width;
	temp.height = vid_height;
	var temp_context = temp.getContext('2d');
	temp_context.drawImage(vidfeed,0,0,vid_width,vid_height);
	var imageData = temp_context.getImageData(0, 0, vid_width, vid_height);
	var gray = tracking.Image.grayscale(imageData.data, vid_width, vid_height);
	var corners = tracking.Fast.findCorners(gray, vid_width, vid_height);
	var descriptors = tracking.Brief.getDescriptors(gray,vid_width,corners)
	var features = {
		corners:corners,
		descriptors:descriptors
		}
	return features;
};

var findFeaturesPic = function(img, fast_threshold, brief_length) {
	
	// Set Algorithm States
	tracking.Fast.THRESHOLD = fast_threshold;
	tracking.Brief.N = brief_length;
	
	var pic_width = img.width;
	var pic_height = img.height;
	var temp = document.createElement("CANVAS");
	temp.width = pic_width;
	temp.height = pic_height;
	var temp_context = temp.getContext('2d');
	temp_context.drawImage(img,0,0,pic_width,pic_height);
	var imageData = temp_context.getImageData(0, 0, pic_width, pic_height);
	var gray = tracking.Image.grayscale(imageData.data, pic_width, pic_height);
	var corners = tracking.Fast.findCorners(gray, pic_width, pic_height);
	var descriptors = tracking.Brief.getDescriptors(gray,pic_width,corners)
	var features = {
		corners:corners,
		descriptors:descriptors
		}
	return features;
}

var matchFeatures = function (c1,d1,c2,d2,confidence_threshold) {
	var matches = tracking.Brief.reciprocalMatch(c1,d1,c2,d2);
	var good_matches = [];
	for (let i = 0; i < matches.length; i++){
		let match = matches[i];
		if (match.confidence > confidence_threshold){
			good_matches.push(match)
		}
	}
	return good_matches
}