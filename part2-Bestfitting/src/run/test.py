# coding: utf-8
import sys
sys.path.insert(0, '..')
import argparse
from tqdm import tqdm
import pandas as pd

import torch
import torch.optim
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SequentialSampler
from torch.nn import DataParallel
import torch.nn.functional as F
from torch.autograd import Variable

from config.config import *
from utils.common_util import *
from networks.imageclsnet import init_network
from datasets.protein_dataset import ProteinDataset
from utils.augment_util import *
from utils.log_util import Logger

datasets_names = ['test', 'val']
split_names = ['random_ext_folds5', 'random_ext_noleak_clean_folds5']
augment_list = ['default', 'flipud', 'fliplr','transpose', 'flipud_lr',
                'flipud_transpose', 'fliplr_transpose', 'flipud_lr_transpose']


def main():
    # initial
    # dataset = ['img_comb1', 'img_comb2', 'img_comb3', 'img_comb4', 'MitoLyso']
    dataset = 'MitoLyso'

    out_dir = dataset
    DATA_DIR = '/home/mqxue/bestfitting/HPA_imgs/Dataset'
    test_split_file = opj(DATA_DIR, dataset + '.csv')
    test_img_dir = opj(DATA_DIR, dataset)
    input_dir = 'model_1024'
    gpu_id = '0'
    arch = 'class_densenet121_dropout'
    num_classes = 28
    in_channels = 4
    img_size = 1024
    crop_size = 1024
    batch_size = 8
    workers = 3

    ###
    log_out_dir = opj(RESULT_DIR, 'logs', out_dir)
    if not ope(log_out_dir):
        os.makedirs(log_out_dir)
    log = Logger()
    log.open(opj(log_out_dir, 'log.submit.txt'), mode='a')

    network_path = opj(TEST_MODELS, input_dir, 'final.pth')

    submit_out_dir = opj(RESULT_DIR, 'submissions', out_dir)
    log.write(">> Creating directory if it does not exist:\n>> '{}'\n".format(submit_out_dir))
    if not ope(submit_out_dir):
        os.makedirs(submit_out_dir)

    # setting up the visible GPU
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_id

    model_params = {}
    model_params['architecture'] = arch
    model_params['num_classes'] = num_classes
    model_params['in_channels'] = 4
    model = init_network(model_params)

    log.write(">> Loading network:\n>>>> '{}'\n".format(network_path))
    checkpoint = torch.load(network_path)
    model.load_state_dict(checkpoint['state_dict'], strict=False)
    log.write(">>>> loaded network:\n>>>> epoch {}\n".format(checkpoint['epoch']))

    # moving network to gpu and eval mode
    model = DataParallel(model)
    model.cuda()
    model.eval()

    # Data loading code
    test_dataset = ProteinDataset(
        test_split_file,
        test_img_dir,
        img_size=img_size,
        is_trainset=False,
        return_label=False,
        in_channels=in_channels,
        transform=None,
        crop_size=crop_size,
        random_crop=False,
    )
    test_loader = DataLoader(
        test_dataset,
        sampler=SequentialSampler(test_dataset),
        batch_size=batch_size,
        drop_last=False,
        num_workers=workers,
        pin_memory=True,
    )
    dataset = 'test'
    # seeds = [args.seed] if args.seeds is None else [int(i) for i in args.seeds.split(',')]
    seeds = [0, 1, 2, 3]
    for seed in seeds:
        test_dataset.random_crop = (seed != 0)
        for augment in augment_list:
            test_loader.dataset.transform = eval('augment_%s' % augment)
            if crop_size > 0:
                sub_submit_out_dir = opj(submit_out_dir, '%s_seed%d' % (augment, seed))
            else:
                sub_submit_out_dir = opj(submit_out_dir, augment)
            if not ope(sub_submit_out_dir):
                os.makedirs(sub_submit_out_dir)
            with torch.no_grad():
                predict(test_loader, model, sub_submit_out_dir, dataset)

def predict(test_loader, model, submit_out_dir, dataset):
    all_probs = []
    all_logits = []
    all_features = []
    img_ids = np.array(test_loader.dataset.img_ids)
    for it, iter_data in tqdm(enumerate(test_loader, 0), total=len(test_loader)):
        images, indices = iter_data
        images = Variable(images.cuda(), volatile=True)
        outputs, features = model(images)
        logits = outputs

        probs = F.sigmoid(logits).data
        all_probs += probs.cpu().numpy().tolist()
        all_logits += logits.cpu().numpy().tolist()
        all_features += features.cpu().numpy().tolist()
    img_ids = img_ids[:len(all_probs)]
    all_probs = np.array(all_probs).reshape(len(img_ids), -1)
    all_logits = np.array(all_logits).reshape(len(img_ids), -1)
    all_features = np.array(all_features).reshape(len(img_ids), -1)

    np.save(opj(submit_out_dir, 'prob_%s.npy' % dataset), all_probs)
    np.save(opj(submit_out_dir, 'logit_%s.npy' % dataset), all_logits)
    np.save(opj(submit_out_dir, 'features_%s.npy' % dataset), all_features)

    result_df = prob_to_result(all_probs, img_ids)
    result_df.to_csv(opj(submit_out_dir, 'results_%s.csv.gz' % dataset), index=False, compression='gzip')

def prob_to_result(probs, img_ids, th=0.5):
    probs = probs.copy()
    probs[np.arange(len(probs)), np.argmax(probs, axis=1)] = 1

    pred_list = []
    for line in probs:
        s = ' '.join(list([str(i) for i in np.nonzero(line > th)[0]]))
        pred_list.append(s)
    result_df = pd.DataFrame({ID: img_ids, PREDICTED: pred_list})
    return result_df

if __name__ == '__main__':
    print('%s: calling main function ... \n' % os.path.basename(__file__))
    main()
    print('\nsuccess!')
