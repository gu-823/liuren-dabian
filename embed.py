import base64

files = {
    'img-miaopu.jpg': './assets/img-miaopu.jpg',
    'img-build1.jpg': './assets/img-build1.jpg',
    'img-build2.jpg': './assets/img-build2.jpg',
}

with open('c:/Users/29557/Downloads/留任答辩/ppt/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for filename, path in files.items():
    with open(f'c:/Users/29557/Downloads/留任答辩/ppt/assets/{filename}', 'rb') as img:
        b64 = base64.b64encode(img.read()).decode('ascii')
        data_uri = f'data:image/jpeg;base64,{b64}'
    old = f'src="./assets/{filename}"'
    html = html.replace(old, f'src="{data_uri}"')
    print(f'{filename}: {len(b64)} chars')

with open('c:/Users/29557/Downloads/留任答辩/ppt/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('done')
