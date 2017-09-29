## Note
This API is able to load all 4 referring expression datasets, i.e., RefClef, RefCOCO, RefCOCO+ and RefCOCOg. 
They are with different train/val/test split by UNC, Google and UC Berkeley respectively. We provide all kinds of splits here.
Note, RefCOCO+ may change in the future as we are still cleaning it. 
Notification will be announced if we made changes.
<table width="100%">
<tr>
<td><img src="http://bvisionweb1.cs.unc.edu/licheng/referit/refer_example.jpg", alt="Mountain View" width="95%"></td>
</tr>
</table>

## Citation
If you used the following three datasets RefClef, RefCOCO and RefCOCO+ that were collected by UNC, please consider cite our EMNLP2014 paper; if you want to compare with our recent results, please check our ECCV2016 paper.
```bash
Kazemzadeh, Sahar, et al. "ReferItGame: Referring to Objects in Photographs of Natural Scenes." EMNLP 2014.
Yu, Licheng, et al. "Modeling Context in Referring Expressions." ECCV 2016.
```

## Setup
To install this package, along its dependencies, you can execute:
```bash
pip install -U .
```
This package depends on numpy, matplotlib, scikit-image and Cython, it also depends on the mscoco API mask routines, which are compiled during setup. These mask-related codes are copied from mscoco [API](https://github.com/pdollar/coco).

## Download
Download the cleaned data and extract them into "data" folder
- 1) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refclef.zip
- 2) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refcoco.zip
- 3) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refcoco+.zip
- 4) http://bvisionweb1.cs.unc.edu/licheng/referit/data/refcocog.zip

## Prepare Images:
Besides, add "mscoco" into the ``data/images`` folder, which can be from [mscoco](http://mscoco.org/dataset/#overview)
COCO's images are used for RefCOCO, RefCOCO+ and refCOCOg.
For RefCLEF, please add ``saiapr_tc-12`` into ``data/images`` folder. We extracted the related 19997 images to our cleaned RefCLEF dataset, which is a subset of the original [imageCLEF](http://imageclef.org/SIAPRdata). Download the [subset](http://bvisionweb1.cs.unc.edu/licheng/referit/data/images/saiapr_tc-12.zip) and unzip it to ``data/images/saiapr_tc-12``.

## How to use
The refer module (``referit/refer.py``) is able to load all 4 datasets with different kinds of data split by UNC, Google and UC Berkeley.
```python
from referit import REFER

# locate your own data_root, and choose the dataset_splitBy you want to use
refer = REFER(data_root, dataset='refclef',  split_by='unc')
refer = REFER(data_root, dataset='refclef',  split_by='berkeley')  # 2 training and 1 testing images missed
refer = REFER(data_root, dataset='refcoco',  split_by='unc')
refer = REFER(data_root, dataset='refcoco',  split_by='google')
refer = REFER(data_root, dataset='refcoco+', split_by='unc')
refer = REFER(data_root, dataset='refcocog', split_by='google')  # testing data haven't been released yet
refer = REFER(data_root, dataset='refcocog', split_by='umd') # train/val/test split provided by UMD (recommended)
```


<!-- refs(dataset).p contains list of refs, where each ref is
{ref_id, ann_id, category_id, file_name, image_id, sent_ids, sentences}
ignore filename

Each sentences is a list of sent
{arw, sent, sent_id, tokens}
 -->
