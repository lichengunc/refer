This directory should contain the following data:
```
$DATA_PATH
├── images
│   ├── mscoco
│   └── saiaprtc12
├── refcoco
│   ├── instances.json
│   ├── refs(google).p
│   └── refs(unc).p
├── refcoco+
│   ├── instances.json
│   └── refs(unc).p
├── refcocog
│   ├── instances.json
│   └── refs(google).p
└── refclef
   	├── instances.json
  	├── refs(unc).p
	  └── refs(berkeley).p
```

Note, each detections/xxx.json contains 
``{'dets': ['box': {x, y, w, h}, 'image_id', 'object_id', 'score']}``. The ``object_id`` and ``score`` might be missing, depending on what proposal/detection technique we are using.

## Download
Download my cleaned data and extract them into this folder.
- 1) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refclef.zip
- 2) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refcoco.zip
- 3) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refcoco+.zip 
- 4) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refcocog.zip 

Besides make a folder named as "images".
Add "mscoco" into "images/". 
Download MSCOCO from [mscoco](http://mscoco.org/dataset/#overview)

Add "saiapr_tc-12" into "images/". I only extracted the related images as a subset of the original [imageCLEF](http://imageclef.org/SIAPRdata), i.e., 19997 images. Please download the subset from here (http://bvisionweb1.cs.unc.edu/licheng/referit/data/images/saiapr_tc-12.zip).
