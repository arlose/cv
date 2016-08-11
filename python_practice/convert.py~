#coding=utf-8
import argparse;
import os;
import re;

# 解析参数
parser = argparse.ArgumentParser(description = 'the notebook to be converted to markdown');
parser.add_argument('nb');
args = parser.parse_args();
f = os.path.split(args.nb);

# 路径处理
file_dir = f[0];
file_name = f[1];
file_name_no_suffix = os.path.splitext(file_name)[0];

if not file_name.endswith('.ipynb'):
    file_name = file_name + '.ipynb';

if file_dir.startswith('../'):
    file_dir = file_dir[file_dir.find('/')+1: len(file_dir)]

if not os.path.exists(file_dir):
    os.makedirs(file_dir);

## 源文件路径
src_path = os.path.join('..',file_dir, file_name);

## 目标路径
target_path = os.path.join(file_dir, file_name_no_suffix+'.md');

#执行生成命令
cmd = 'jupyter nbconvert {0} --to markdown --output {1}'.format(src_path, target_path);
print cmd;
os.system(cmd);

#修改图片的url
with open(target_path, 'r') as f:
    lines = f.readlines();
    for line_no in xrange(len(lines)):
        line = lines[line_no];
        m = re.match('\!\[png\]', line);
        if m is not None:
            full = line.find('https://') + line.find('http://');
            if full < 0:
                print line
                line = list(line);
                loc = line.index('(') + 1;
                url_prefix = 'https://raw.githubusercontent.com/dengdan/deep-learning-with-mxnet/master/markdowns/';
                line.insert(loc, url_prefix);
                line = ''.join(line);
                print line;
                lines[line_no] = line;
endLine = '<hr>github: https://github.com/dengdan/deep-learning-with-mxnet/tree/master/'+ os.path.join(file_dir, file_name);
print endLine;
lines.append(endLine);
with open(target_path, 'w') as f:
    f.writelines(lines);

#将markdown内容复制到剪贴板
os.system('xclip -selection c {0}'.format(target_path));
print('the content of markdown file is in your clipboard now')
