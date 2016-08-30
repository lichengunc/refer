## Note
This API is able to load all 4 referring expression datasets, i.e., RefClef, RefCOCO, RefCOCO+ and RefCOCOg. 
They are with different train/val/test split by UNC, Google and UC Berkeley respectively. We provide all kinds of splits here.
Note, RefCOCO+ may change in the future as we are still cleaning it. 
Notification will be announced if we made changes.
<table width="100%">
<tr>
<td><img src="http://tlberg.cs.unc.edu/licheng/referit/refer_example.jpg", alt="Mountain View" width="95%"></td>
</tr>
</table>

## Citation
If you used the following three datasets RefClef, RefCOCO and RefCOCO+ that were collected by UNC, please consider cite our EMNLP2014 paper; if you want to compare with our recent results, please check our ECCV2016 paper.
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

## Prepare Images:
Besides, add "mscoco" into the ``data/images`` folder, which can be from [mscoco](http://mscoco.org/dataset/#overview)
COCO's images are used for RefCOCO, RefCOCO+ and refCOCOg.
For RefCLEF, please add ``saiapr_tc-12`` into ``data/images`` folder. We extracted the related 19997 images to our cleaned RefCLEF dataset, which is a subset of the original [imageCLEF](http://imageclef.org/SIAPRdata). Download the [subset](http://tlberg.cs.unc.edu/licheng/referit/data/images/saiapr_tc-12.zip) and unzip it to ``data/images/saiapr_tc-12``.

## How to use
The "refer.py" is able to load all 4 datasets with different kinds of data split by UNC, Google and UC Berkeley.
```bash
# locate your own data_root, and choose the dataset_splitBy you want to use
refer = REFER(data_root, dataset='refclef',  splitBy='unc')
refer = REFER(data_root, dataset='refclef',  splitBy='berkeley')  # 2 training and 1 testing images missed
refer = REFER(data_root, dataset='refcoco',  splitBy='unc')
refer = REFER(data_root, dataset='refcoco',  splitBy='google')
refer = REFER(data_root, dataset='refcoco+', splitBy='unc')
refer = REFER(data_root, dataset='refcocog', splitBy='google')  # testing data haven't been released yet
```


<!-- refs(dataset).p contains list of refs, where each ref is
{ref_id, ann_id, category_id, file_name, image_id, sent_ids, sentences}
ignore filename

Each sentences is a list of sent
{arw, sent, sent_id, tokens}
 -->
