import random

def split_conllu_train_dev_test(input_file, train_file, dev_file, test_file, train_ratio=0.7, dev_ratio=0.15, seed=42):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    blocks = [block for block in content.split("\n\n") if block.strip()]
    
    pos_blocks = []
    neg_blocks = []
    
    for block in blocks:
        if "name=B-FELT" in block:
            pos_blocks.append(block)
        else:
            neg_blocks.append(block)
    
    random.seed(seed)
    random.shuffle(pos_blocks)
    random.shuffle(neg_blocks)
    
    pos_train_idx = int(len(pos_blocks) * train_ratio)
    pos_dev_idx = pos_train_idx + int(len(pos_blocks) * dev_ratio)
    
    neg_train_idx = int(len(neg_blocks) * train_ratio)
    neg_dev_idx = neg_train_idx + int(len(neg_blocks) * dev_ratio)
    
    pos_train = pos_blocks[:pos_train_idx]
    pos_dev = pos_blocks[pos_train_idx:pos_dev_idx]
    pos_test = pos_blocks[pos_dev_idx:]
    
    neg_train = neg_blocks[:neg_train_idx]
    neg_dev = neg_blocks[neg_train_idx:neg_dev_idx]
    neg_test = neg_blocks[neg_dev_idx:]
    
    train_blocks = pos_train + neg_train
    dev_blocks = pos_dev + neg_dev
    test_blocks = pos_test + neg_test
    
    with open(train_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(train_blocks) + "\n")
    
    with open(dev_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(dev_blocks) + "\n")
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(test_blocks) + "\n")
    
    print(f"Total sentences: {len(blocks)}")
    print(f"Sentences with B-FELT: {len(pos_blocks)}")
    print(f"Sentences without B-FELT: {len(neg_blocks)}")
    print(f"Training set: {len(train_blocks)} sentences")
    print(f"Dev set: {len(dev_blocks)} sentences")
    print(f"Test set: {len(test_blocks)} sentences")
    
input_file = 'data/all_regplans.conllu'  
train_file = 'data/regplans-train.conllu'  
dev_file = 'data/regplans-dev.conllu'  
test_file = 'data/regplans-test.conllu'  

train_ratio = 0.7
dev_ratio = 0.15
    
split_conllu_train_dev_test(input_file, train_file, dev_file, test_file, train_ratio, dev_ratio)
