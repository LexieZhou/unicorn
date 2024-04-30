import os
with open('../../datasets/NMR_Dataset/03001627/softras_test_intersection.lst', 'r') as f:
    names = f.read().split('\n')
    names = list(filter(lambda x: len(x) > 0, names))
print(len(names))
valid_lst_contents = []
for name in names:
    absolute_path = os.path.join('../../datasets/NMR_Dataset/03001627', name)
    if os.path.exists(absolute_path):
        valid_lst_contents.append(name)
print(len(valid_lst_contents))
lst_file_path = '../../datasets/NMR_Dataset/03001627/softras1_test_intersection.lst'
with open(lst_file_path, 'w') as f:
    f.write('\n'.join(valid_lst_contents))