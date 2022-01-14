import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

import json
import random
import math
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

EPOCH_NUM = 50
BATCH_SIZE = 32
PRINT_ITER = 100

edu_lookup = {
    '國小': 0,
    '國中': 1,
    '高中職': 2,
    '專科': 3,
    '大學': 4,
    '碩士': 5,
    '博士': 6
}
city_idx = None
edu_idx = None
exp_idx = None
major_idx = None
coding_idx = None
software_idx = None
category_idx = None
feature_len = None
feature_lookup = None

device = "cuda:0" if torch.cuda.is_available() else "cpu"

def build_index():
    global city_idx, edu_idx, exp_idx, major_idx, coding_idx, software_idx, category_idx, feature_len, feature_lookup
    infile = open("all.json", 'r')
    data = json.load(infile)

    city_idx = {key:value for value, key in enumerate(set([item['companyCity'] for item in data]))}
    feature_lookup = {value:key for value, key in enumerate(set([item['companyCity'] for item in data]))}
    prefix = len(city_idx)
    edu_idx = prefix
    feature_lookup.update({edu_idx:'教育程度'})
    prefix += 1
    exp_idx = prefix
    feature_lookup.update({exp_idx:'工作經驗'})
    prefix += 1
    # identity_idx = {key:(value + prefix) for value, key in enumerate(set([item2 for item in data for item2 in item['acceptIdentity']]))}
    # feature_lookup.update({(value + prefix):key for value, key in enumerate(set([item2 for item in data for item2 in item['acceptIdentity']]))})
    # prefix += len(identity_idx)
    major_idx = {key:(value + prefix) for value, key in enumerate(set([item2 for item in data for item2 in item['acceptMajor']]))}
    feature_lookup.update({(value + prefix):key for value, key in enumerate(set([item2 for item in data for item2 in item['acceptMajor']]))})
    prefix += len(major_idx)
    # lang_idx = {key:(value + prefix) for value, key in enumerate(set([item2 for item in data for item2 in item['language']]))}
    # feature_lookup.update({(value + prefix):key for value, key in enumerate(set([item2 for item in data for item2 in item['language']]))})
    # prefix += len(lang_idx)
    coding_idx = {key:(value + prefix) for value, key in enumerate(set([item2 for item in data for item2 in item['codingLanguage']]))}
    feature_lookup.update({(value + prefix):key for value, key in enumerate(set([item2 for item in data for item2 in item['codingLanguage']]))})
    prefix += len(coding_idx)
    # cer_idx = {key:(value + prefix) for value, key in enumerate(set([item2 for item in data for item2 in item['certificate']]))}
    # feature_lookup.update({(value + prefix):key for value, key in enumerate(set([item2 for item in data for item2 in item['certificate']]))})
    # prefix += len(cer_idx)
    software_idx = {key:(value + prefix) for value, key in enumerate(set([item2 for item in data for item2 in item['software']]))}
    feature_lookup.update({(value + prefix):key for value, key in enumerate(set([item2 for item in data for item2 in item['software']]))})
    prefix += len(software_idx)
    feature_len = prefix
    category_idx = {key:value for value, key in enumerate(set([item2 for item in data for item2 in item['jobCategory']]))}

class JobDataset(Dataset):
    def __init__(self, mode, filt_salary=False):
        self.mode = mode
        infile = open("{0}.json".format(mode), 'r')
        self.data = json.load(infile)

        if filt_salary:
            rm_index = []
            for i in range(len(self.data)):
                if self.data[i]['jobSalary'] == 0:
                    rm_index.append(i)
            for index in reversed(rm_index):
                self.data.pop(index)

        print("[INFO] {0}: {1} samples found".format(mode, len(self.data)))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        global city_idx, edu_idx, exp_idx, major_idx, coding_idx, software_idx, category_idx, feature_len, device
        feature = torch.zeros(feature_len)
        data = self.data[index]
        feature[city_idx[data['companyCity']]] = 1
        min_edu = len(edu_lookup)
        for edu in data['eduLevel']:
            if edu_lookup[edu] < min_edu:
                min_edu = edu_lookup[edu]
        feature[edu_idx] = min_edu
        feature[exp_idx] = data['workingExp']
        # if len(data['acceptMajor']) != 0:
        #     feature[major_idx[random.choice(data['acceptMajor'])]] = 1
        # if len(data['codingLanguage']) != 0:
        #     choices = random.sample(data['codingLanguage'], random.randint(len(data['codingLanguage']) // 2, len(data['codingLanguage'])))
        #     for choice in choices:
        #         feature[coding_idx[choice]] = 1
        # if len(data['software']) != 0:
        #     choices = random.sample(data['software'], random.randint(len(data['software']) // 2, len(data['software'])))
        #     for choice in choices:
        #         feature[software_idx[choice]] = 1
        if len(data['acceptMajor']) != 0:
            for major in data['acceptMajor']:
                feature[major_idx[major]] = 1
        if len(data['codingLanguage']) != 0:
            for coding in data['codingLanguage']:
                feature[coding_idx[coding]] = 1
        if len(data['software']) != 0:
            for software in data['software']:
                feature[software_idx[software]] = 1

        cate_label = torch.zeros(len(category_idx))
        for cate in data['jobCategory']:
            cate_label[category_idx[cate]] = 1

        # return feature, cate_label, data['jobSalary']
        return feature, cate_label, data['jobSalary']

class JobClassifier(nn.Module):
    def __init__(self):
        global feature_len
        super(JobClassifier, self).__init__()
        self.fc1 = nn.Sequential (
            nn.Linear(feature_len, 80),
            nn.ReLU(),
            #nn.Dropout()
        )
        self.fc2 = nn.Sequential (
            nn.Linear(80, 60),
            nn.ReLU(),
            #nn.Dropout()
        )
        self.fc3 = nn.Linear(60, len(category_idx))

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x

def take_second(t):
    return t[1]

def main():
    build_index()
    training_set = JobDataset('train')
    #'''
    ITER_NUM = int(math.ceil(len(training_set) / BATCH_SIZE))
    classifier_model = JobClassifier().to(device=device).train()
    classifier_optim = optim.SGD(classifier_model.parameters(), lr=0.001, momentum=0.9, weight_decay=5e-3)
    classifier_scheduler = optim.lr_scheduler.CosineAnnealingLR(classifier_optim, T_max=EPOCH_NUM * ITER_NUM, eta_min = 0)
    for epoch in range(EPOCH_NUM):
        training_loader = DataLoader(training_set, batch_size=BATCH_SIZE)
        for i, data in enumerate(training_loader):
            input_feature, label, salary = data
            input_feature = input_feature.to(device=device)
            label = label.to(device=device)
            salary = salary.to(device=device)
            classifier_optim.zero_grad()
            output = classifier_model(input_feature)
            loss = F.binary_cross_entropy_with_logits(output, label)
            #print(output)
            #print(label)
            loss.backward()
            classifier_optim.step()
            classifier_scheduler.step()
            if (epoch * ITER_NUM + i) % PRINT_ITER == 0:
                print("Epoch: {0}, iter: {1}, lr = {2}, loss = {3}".format(epoch, i, classifier_scheduler.get_lr(), loss))
                sigmoid = (F.sigmoid(output) > 0.3)
                for j in range(len(label)):
                    print("Target: ", label[j].int().tolist())
                    print("Output: ", sigmoid[j].tolist())
                    print("")
                print("Training micro F1 score: {0}\n".format(f1_score(label.cpu(), sigmoid.cpu(), average='micro')))
    
    for i in range(len(category_idx)):
        for key, value in category_idx.items():
            if value == i:
                print(key, end=', ')
                break
    print()
    '''
    training_loader = DataLoader(training_set, batch_size=len(training_set), shuffle=True)
    classifier = RandomForestClassifier(n_estimators=100)
    inputs, labels, salaries = [data for data in training_loader][0]
    classifier.fit(inputs.tolist(), labels.tolist())
    sample_idx = random.sample(range(len(inputs)), 10)
    result = classifier.predict(inputs[sample_idx])

    #prob = [[] for i in range(len(result[0]))]
    #for i in range(len(result)):
    #    for j in range(len(result[i])):
    #        prob[j].append(result[i][j].tolist())
    for i in range(len(sample_idx)):
        print("Target: ", labels[sample_idx[i]].int().tolist())
        print("Output: ", result[i].astype(int).tolist())
        print("")

    print("Feature importance: ")
    imp = classifier.feature_importances_.tolist()
    imp = list(enumerate(imp))
    imp.sort(key=take_second, reverse=True)
    for i, value in imp:
        print("{0}: {1}".format(feature_lookup[i], value))
    
    result = classifier.predict(inputs)
    print("\nTraining micro F1 score: {0}\n".format(f1_score(labels, result, average='micro')))
    
    testing_set = JobDataset('test')
    testing_loader = DataLoader(testing_set, batch_size=len(testing_set), shuffle=True)
    inputs, labels, salaries = [data for data in testing_loader][0]
    result = classifier.predict(inputs)
    print("Testing micro F1 score: {0}\n".format(f1_score(labels, result, average='micro')))
    for i in range(len(sample_idx)):
        print("Target: ", labels[i].int().tolist())
        print("Output: ", result[i].astype(int).tolist())
        print("")

    for i in range(feature_len):
        print(feature_lookup[i], end=', ')
    print()
    '''

if __name__ == '__main__':
    main()
