
## Download
Download the cleaned data and extract them into "data" folder
- 1) http://tlberg.cs.unc.edu/licheng/referit/data/refclef.zip
- 2) http://tlberg.cs.unc.edu/licheng/referit/data/refcoco.zip
- 3) http://tlberg.cs.unc.edu/licheng/referit/data/refcoco+.zip 
- 4) http://tlberg.cs.unc.edu/licheng/referit/data/refcocog.zip 

## Prepare Images:
Besides we add "mscoco" into the "data/images" folder. 
Download it from [mscoco](http://mscoco.org/dataset/#overview)
This dataset is for refcoco, refcoco+ and refgoogle.
For refclef, we add "saiapr_tc-12" into 'data/images' folder. I only extracted the related images as a subset of the original [imageCLEF](http://imageclef.org/SIAPRdata), i.e., 19997 images. Please download the subset from here (http://tlberg.cs.unc.edu/licheng/referit/data/images/saiapr_tc-12.zip).
Our dataset API "pyutils/datasets/refer.py" is able to load all 4 datasets.

## How to use
```bash
refer = REFER('refclef',  splitBy='unc')
refer = REFER('refcoco',  splitBy='unc')
refer = REFER('refcoco',  splitBy='google')
refer = REFER('refcoco+', splitBy='unc')
refer = REFER('refcocog', splitBy='google')
```


<!-- refs(dataset).p contains list of refs, where each ref is
{ref_id, ann_id, category_id, file_name, image_id, sent_ids, sentences}
ignore filename

Each sentences is a list of sent
{arw, sent, sent_id, tokens}
 -->