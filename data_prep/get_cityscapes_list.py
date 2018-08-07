import os
import glob
import argparse

def get_cityscapes_list_augmented(root, image_path, label_path, lst_path, is_fine=True, sample_rate=1):
    index = 0
    train_lst = []
    label_prefix = 'gtFine_labelIds' if is_fine else 'gtCoarse_labelIds'

    # images
    all_images = glob.glob(os.path.join(root, image_path, '*/*.png'))
    all_images.sort()
    for p in all_images:
        l = p.replace(image_path, label_path).replace('leftImg8bit', label_prefix)
        if os.path.isfile(l):
            index += 1
            if index % 100 == 0:
                print("%d out of %d done." % (index, len(all_images)))
            if index % sample_rate != 0:
                continue
            for i in range(1, 8):
                train_lst.append([str(index), p, l, "512", str(256 * i)])
        else:
            print("dismiss %s" % (p))

    train_out = open(lst_path, "w")
    for line in train_lst:
#        print >> train_out, '\t'.join(line)
        train_out.write('\t'.join(line)+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--root",
                        help="root path for cityscapes",
                        required=True,
                        default=None)
    
    args=parser.parse_args()
    root=args.root
    image_path=os.path.join(root,'leftImg8bit_trainvaltest','leftImg8bit')
    label_path=os.path.join(root,'gtFine_trainvaltest','gtFine')
    
    for split in ['train','val']:
        lst_path=split+'.txt'
        split_image_path=os.path.join(image_path,split)
        split_label_path=os.path.join(label_path,split)
        
        get_cityscapes_list_augmented(root=root,
                                      image_path=split_image_path,
                                      label_path=split_label_path,
                                      lst_path=lst_path)