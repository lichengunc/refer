# -*- coding: utf-8 -*-

"""
This interface provides access to four datasets:
1) refclef
2) refcoco
3) refcoco+
4) refcocog
split by unc and google

The following API functions are defined:
REFER      - REFER api class
get_ref_ids  - get ref ids that satisfy given filter conditions.
get_ann_ids  - get ann ids that satisfy given filter conditions.
get_img_ids  - get image ids that satisfy given filter conditions.
get_cat_ids  - get category ids that satisfy given filter conditions.
load_refs   - load refs with the specified ref ids.
load_anns   - load anns with the specified ann ids.
load_imgs   - load images with the specified image ids.
load_cats   - load category names with the specified category ids.
get_ref_box  - get ref's bounding box [x, y, w, h] given the ref_id
show_ref    - show image, segmentation or box of the referred object
             with the ref
get_mask    - get mask and area of the referred object given ref
show_mask   - show mask of the referred object given ref
"""

import sys
import json
import time
import pickle
import itertools
import numpy as np
import os.path as osp
import skimage.io as io
from pprint import pprint
from referit.external import mask
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon, Rectangle


class REFER:
    """ReferIt split loader utillity wrapper class."""

    def __init__(self, data_root, dataset='refcoco', split_by='unc'):
        """
        Main instance constructor.
        Provide data_root folder which contains refclef, refcoco,
        refcoco+ and refcocog
        also provide dataset name and split_by information
        e.g., dataset = 'refcoco', split_by = 'unc'
        """
        print('loading dataset %s into memory...' % dataset)
        self.ROOT_DIR = osp.abspath(osp.dirname(__file__))
        self.DATA_DIR = osp.join(data_root, dataset)
        if dataset in ['refcoco', 'refcoco+', 'refcocog']:
            self.IMAGE_DIR = osp.join(
                data_root, 'images/mscoco/images/train2014')
        elif dataset == 'refclef':
            self.IMAGE_DIR = osp.join(data_root, 'images/saiapr_tc-12')
        else:
            print('No refer dataset is called [%s]' % dataset)
            sys.exit()

        # load refs from data/dataset/refs(dataset).json
        tic = time.time()
        ref_file = osp.join(self.DATA_DIR, 'refs({0}).p'.format(split_by))
        self.data = {}
        self.data['dataset'] = dataset
        self.data['refs'] = pickle.load(open(ref_file, 'r'))

        # load annotations from data/dataset/instances.json
        instances_file = osp.join(self.DATA_DIR, 'instances.json')
        instances = json.load(open(instances_file, 'r'))
        self.data['images'] = instances['images']
        self.data['annotations'] = instances['annotations']
        self.data['categories'] = instances['categories']

        # create index
        self.create_index()
        print('DONE (t=%.2fs)' % (time.time() - tic))

    def create_index(self):
        """
        Create sets of mapping.

        Setup Attributes
        -----------------------------------------------
        1)  refs:          {ref_id: ref}
        2)  anns:          {ann_id: ann}
        3)  imgs:             {image_id: image}
        4)  cats:          {category_id: category_name}
        5)  sents:         {sent_id: sent}
        6)  img_to_refs:     {image_id: refs}
        7)  img_to_anns:     {image_id: anns}
        8)  ref_to_ann:      {ref_id: ann}
        9)  ann_to_ref:      {ann_id: ref}
        10) cat_to_refs:     {category_id: refs}
        11) sent_to_ref:     {sent_id: ref}
        12) sent_to_tokens: {sent_id: tokens}
        """
        print('creating index...')
        # fetch info from instances
        anns, imgs, cats, img_to_anns = {}, {}, {}, {}
        for ann in self.data['annotations']:
            anns[ann['id']] = ann
            img_to_anns[ann['image_id']] = img_to_anns.get(
                ann['image_id'], []) + [ann]
        for img in self.data['images']:
            imgs[img['id']] = img
        for cat in self.data['categories']:
            cats[cat['id']] = cat['name']

        # fetch info from refs
        (refs, img_to_refs, ref_to_ann,
         ann_to_ref, cat_to_refs) = {}, {}, {}, {}, {}
        sents, sent_to_ref, sent_to_tokens = {}, {}, {}
        for ref in self.data['refs']:
            # ids
            ref_id = ref['ref_id']
            ann_id = ref['ann_id']
            category_id = ref['category_id']
            image_id = ref['image_id']

            # add mapping related to ref
            refs[ref_id] = ref
            img_to_refs[image_id] = img_to_refs.get(image_id, []) + [ref]
            cat_to_refs[category_id] = cat_to_refs.get(category_id, []) + [ref]
            ref_to_ann[ref_id] = anns[ann_id]
            ann_to_ref[ann_id] = ref

            # add mapping of sent
            for sent in ref['sentences']:
                sents[sent['sent_id']] = sent
                sent_to_ref[sent['sent_id']] = ref
                sent_to_tokens[sent['sent_id']] = sent['tokens']

        # create class members
        self.refs = refs
        self.anns = anns
        self.imgs = imgs
        self.cats = cats
        self.sents = sents
        self.img_to_refs = img_to_refs
        self.img_to_anns = img_to_anns
        self.ref_to_ann = ref_to_ann
        self.ann_to_ref = ann_to_ref
        self.cat_to_refs = cat_to_refs
        self.sent_to_ref = sent_to_ref
        self.sent_to_tokens = sent_to_tokens
        print('index created.')

    def get_ref_ids(self, image_ids=[], cat_ids=[], ref_ids=[], split=''):
        image_ids = image_ids if type(image_ids) == list else [image_ids]
        cat_ids = cat_ids if type(cat_ids) == list else [cat_ids]
        ref_ids = ref_ids if type(ref_ids) == list else [ref_ids]

        if sum([len(x) for x in (image_ids, cat_ids, ref_ids, split)]) == 0:
            refs = self.data['refs']
        else:
            if not len(image_ids) == 0:
                refs = [self.img_to_refs[image_id] for image_id in image_ids]
            else:
                refs = self.data['refs']
            if not len(cat_ids) == 0:
                refs = [ref for ref in refs if ref['category_id'] in cat_ids]
            if not len(ref_ids) == 0:
                refs = [ref for ref in refs if ref['ref_id'] in ref_ids]
            if not len(split) == 0:
                if split in ['testA', 'testB', 'testC']:
                    refs = [ref for ref in refs
                            if split[-1] in ref['split']]
                elif split in ['testAB', 'testBC', 'testAC']:
                    # we also consider testAB, testBC, ...
                    # rarely used I guess...
                    refs = [ref for ref in refs if ref['split'] == split]
                elif split == 'test':
                    refs = [ref for ref in refs if 'test' in ref['split']]
                elif split == 'train' or split == 'val':
                    refs = [ref for ref in refs if ref['split'] == split]
                else:
                    print('No such split [%s]' % split)
                    sys.exit()
        ref_ids = [ref['ref_id'] for ref in refs]
        return ref_ids

    def get_ann_ids(self, image_ids=[], cat_ids=[], ref_ids=[]):
        image_ids = image_ids if type(image_ids) == list else [image_ids]
        cat_ids = cat_ids if type(cat_ids) == list else [cat_ids]
        ref_ids = ref_ids if type(ref_ids) == list else [ref_ids]

        if len(image_ids) == len(cat_ids) == len(ref_ids) == 0:
            ann_ids = [ann['id'] for ann in self.data['annotations']]
        else:
            if not len(image_ids) == 0:
                lists = [self.img_to_anns[image_id] for image_id in image_ids
                         if image_id in self.img_to_anns]  # list of [anns]
                anns = list(itertools.chain.from_iterable(lists))
            else:
                anns = self.data['annotations']
            if not len(cat_ids) == 0:
                anns = [ann for ann in anns if ann['category_id'] in cat_ids]
            ann_ids = [ann['id'] for ann in anns]
            if not len(ref_ids) == 0:
                ann_ids = set(ann_ids).intersection(
                    set([self.refs[ref_id]['ann_id'] for ref_id in ref_ids]))
        return ann_ids

    def get_img_ids(self, ref_ids=[]):
        ref_ids = ref_ids if type(ref_ids) == list else [ref_ids]

        if not len(ref_ids) == 0:
            image_ids = list(set(
                [self.refs[ref_id]['image_id'] for ref_id in ref_ids]))
        else:
            image_ids = self.imgs.keys()
        return image_ids

    def get_cat_ids(self):
        return self.cats.keys()

    def load_refs(self, ref_ids=[]):
        if isinstance(ref_ids, list):
            return [self.refs[ref_id] for ref_id in ref_ids]
        elif isinstance(ref_ids, int):
            return [self.refs[ref_ids]]

    def load_anns(self, ann_ids=[]):
        if isinstance(ann_ids, list):
            return [self.anns[ann_id] for ann_id in ann_ids]
        else:
            return [self.anns[ann_ids]]

    def load_imgs(self, image_ids=[]):
        if isinstance(image_ids, list):
            return [self.imgs[image_id] for image_id in image_ids]
        elif isinstance(image_ids, int):
            return [self.imgs[image_ids]]

    def load_cats(self, cat_ids=[]):
        if isinstance(cat_ids, list):
            return [self.cats[cat_id] for cat_id in cat_ids]
        elif isinstance(cat_ids, int):
            return [self.cats[cat_ids]]

    def get_ref_box(self, ref_id):
        ann = self.ref_to_ann[ref_id]
        return ann['bbox']  # [x, y, w, h]

    def show_ref(self, ref, seg_box='seg'):
        ax = plt.gca()
        # show image
        image = self.imgs[ref['image_id']]
        img = io.imread(osp.join(self.IMAGE_DIR, image['file_name']))
        ax.imshow(img)
        # show refer expression
        for sid, sent in enumerate(ref['sentences']):
            print('%s. %s' % (sid + 1, sent['sent']))
        # show segmentations
        if seg_box == 'seg':
            ann_id = ref['ann_id']
            ann = self.anns[ann_id]
            polygons = []
            color = []
            c = 'none'
            if type(ann['segmentation'][0]) == list:
                # polygon used for refcoco*
                for seg in ann['segmentation']:
                    poly = np.array(seg).reshape((len(seg) / 2, 2))
                    polygons.append(Polygon(poly, True, alpha=0.4))
                    color.append(c)
                p = PatchCollection(
                    polygons, facecolors=color, edgecolors=(1, 1, 0, 0),
                    linewidths=3, alpha=1)
                ax.add_collection(p)  # thick yellow polygon
                p = PatchCollection(
                    polygons, facecolors=color, edgecolors=(1, 0, 0, 0),
                    linewidths=1, alpha=1)
                ax.add_collection(p)  # thin red polygon
            else:
                # mask used for refclef
                rle = ann['segmentation']
                m = mask.decode(rle)
                img = np.ones((m.shape[0], m.shape[1], 3))
                color_mask = np.array([2.0, 166.0, 101.0]) / 255
                for i in range(3):
                    img[:, :, i] = color_mask[i]
                ax.imshow(np.dstack((img, m * 0.5)))
        # show bounding-box
        elif seg_box == 'box':
            ann_id = ref['ann_id']
            ann = self.anns[ann_id]
            bbox = self.get_ref_box(ref['ref_id'])
            box_plot = Rectangle(
                (bbox[0], bbox[1]), bbox[2], bbox[3],
                fill=False, edgecolor='green', linewidth=3)
            ax.add_patch(box_plot)

    def get_mask(self, ref):
        # return mask, area and mask-center
        ann = self.ref_to_ann[ref['ref_id']]
        image = self.imgs[ref['image_id']]
        if isinstance(ann['segmentation'][0], list):  # polygon
            rle = mask.frPyObjects(
                ann['segmentation'], image['height'], image['width'])
        else:
            rle = ann['segmentation']
        m = mask.decode(rle)
        """
        Sometimes there are multiple binary map
        (corresponding to multiple segs)
        """
        m = np.sum(m, axis=2)
        m = m.astype(np.uint8)  # convert to np.uint8
        # compute area
        area = sum(mask.area(rle))  # should be close to ann['area']
        return {'mask': m, 'area': area}

    def show_mask(self, ref):
        M = self.get_mask(ref)
        msk = M['mask']
        ax = plt.gca()
        ax.imshow(msk)


if __name__ == '__main__':
    refer = REFER(dataset='refcocog', split_by='google')
    ref_ids = refer.get_ref_ids()
    print(len(ref_ids))

    print(len(refer.imgs))
    print(len(refer.img_to_refs))

    ref_ids = refer.get_ref_ids(split='train')
    print('There are %s training referred objects.' % len(ref_ids))

    for ref_id in ref_ids:
        ref = refer.load_refs(ref_id)[0]
        if len(ref['sentences']) < 2:
            continue

        pprint(ref)
        print('The label is %s.' % refer.cats[ref['category_id']])
        plt.figure()
        refer.show_ref(ref, seg_box='box')
        plt.show()
