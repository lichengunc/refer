## Note
We are doing some further cleaning on refcoco+, thus this dataset may change in the future.

## Cite
If you used the following three datasets RefClef, RefCOCO and RefCOCO+, please consider cite our EMNLP2014 paper; if you want to compare with our recent results, please check our ECCV2016 paper.
```bash
Kazemzadeh, Sahar, et al. "ReferItGame: Referring to Objects in Photographs of Natural Scenes." EMNLP 2014.
Yu, Licheng, et al. "Modeling Context in Referring Expressions." ECCV 2016.
```
## Setup
Run "make" before using the code.
It will generate ``_mask.c`` and ``_mask.so`` in ``external/`` folder.
These mask-related codes are copied from mscoco [API](https://github.com/pdollar/coco).

## Download
Download the cleaned data and extract them into "data" folder
- 1) http://tlberg.cs.unc.edu/licheng/referit/data/refclef.zip
- 2) http://tlberg.cs.unc.edu/licheng/referit/data/refcoco.zip
- 3) http://tlberg.cs.unc.edu/licheng/referit/data/refcoco+.zip 
- 4) http://tlberg.cs.unc.edu/licheng/referit/data/refcocog.zip 

<table width="100%">
<tr>
<td><img src="http://tlberg.cs.unc.edu/licheng/referit/refer_example.jpg", alt="Mountain View" width="95%"></td>
</tr>
</table>


## Prepare Images:
Besides we add "mscoco" into the "data/images" folder. 
Download it from [mscoco](http://mscoco.org/dataset/#overview)
This dataset is for refcoco, refcoco+ and refgoogle.
For refclef, we add "saiapr_tc-12" into 'data/images' folder. I only extracted the related images as a subset of the original [imageCLEF](http://imageclef.org/SIAPRdata), i.e., 19997 images. Please download the subset from here (http://tlberg.cs.unc.edu/licheng/referit/data/images/saiapr_tc-12.zip).
The "refer.py" is able to load all 4 datasets with different kinds of data split by UNC, Google and UC Berkeley.

## How to use
```bash
# locate your own data_root, and choose the dataset_splitBy you want to use
refer = REFER(data_root, dataset='refclef',  splitBy='unc')
refer = REFER(data_root, dataset='refclef',  splitBy='berkeley') -- we miss 1 training and 2 testing images.
refer = REFER(data_root, dataset='refcoco',  splitBy='unc')
refer = REFER(data_root, dataset='refcoco',  splitBy='google')
refer = REFER(data_root, dataset='refcoco+', splitBy='unc')
refer = REFER(data_root, dataset='refcocog', splitBy='google')
```


<!-- refs(dataset).p contains list of refs, where each ref is
{ref_id, ann_id, category_id, file_name, image_id, sent_ids, sentences}
ignore filename

Each sentences is a list of sent
{arw, sent, sent_id, tokens}
 -->
