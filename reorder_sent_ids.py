def reorder_sent_ids(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    blocks = content.split("\n\n")
    block_list = []
    
    for block in blocks:
        lines = block.splitlines()
        sent_id_val = None
        
        for line in lines:
            if line.startswith("# sent_id"):
                try:
                    sent_id_val = int(line.split('=')[1].strip())
                except ValueError:
                    sent_id_val = float('inf')
                break
        
        if sent_id_val is None:
            sent_id_val = float('inf')
        
        block_list.append((sent_id_val, lines))
    
    block_list.sort(key=lambda x: x[0])
    
    new_blocks = []
    
    for i, (_, lines) in enumerate(block_list, start=1):
        new_id = format(i, '06d')
        new_lines = []
        sent_id_found = False
        
        for line in lines:
            if line.startswith("# sent_id"):
                new_lines.append(f"# sent_id = {new_id}")
                sent_id_found = True
            else:
                new_lines.append(line)
        
        if not sent_id_found:
            new_lines.insert(0, f"# sent_id = {new_id}")
        
        new_blocks.append("\n".join(new_lines))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(new_blocks))
        f.write("\n")

if __name__ == '__main__':

    input_file = 'data/all_regplans_test.conllu'             
    output_file = f'data/all_regplans_test.conllu'     
    reorder_sent_ids(input_file, output_file)
