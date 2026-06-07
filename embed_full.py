import base64
import urllib.request
import os

ASSETS = 'c:/Users/29557/Downloads/留任答辩/ppt/assets'
HTML = 'c:/Users/29557/Downloads/留任答辩/ppt/index.html'

# 1) 下载 lucide 到 assets
lucide_path = os.path.join(ASSETS, 'lucide.min.js')
if not os.path.exists(lucide_path):
    url = 'https://unpkg.com/lucide@latest/dist/umd/lucide.min.js'
    print(f'downloading {url} ...')
    urllib.request.urlretrieve(url, lucide_path)
    print(f'  -> {lucide_path} ({os.path.getsize(lucide_path)} bytes)')

# 2) 读取两个文件，转 base64
def to_data_uri(path, mime):
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    return f'data:{mime};base64,{b64}'

motion_uri = to_data_uri(os.path.join(ASSETS, 'motion.min.js'), 'application/javascript')
lucide_uri = to_data_uri(lucide_path, 'application/javascript')
print(f'motion: {len(motion_uri)} chars')
print(f'lucide: {len(lucide_uri)} chars')

# 3) 改 HTML
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# 替换 lucide 引用
html = html.replace(
    '<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>',
    f'<script src="{lucide_uri}"></script>'
)

# 替换 motion 引用，移除 CDN fallback
old_motion_block = """try {
  motion = await import('./assets/motion.min.js');
} catch(e1) {
  try {
    motion = await import('https://cdn.jsdelivr.net/npm/motion@11.11.17/+esm');
  } catch(e2) {
    console.warn('[motion] local + CDN both failed, disabling animations', e1, e2);
    document.querySelectorAll('[data-anim]').forEach(el=>{el.style.opacity='1';el.style.transform='none'});
    document.querySelectorAll('[data-animate="pipeline"] [data-anim]').forEach(el=>el.style.opacity='1');
  }
}"""
new_motion_block = f"motion = await import('{motion_uri}');"
html = html.replace(old_motion_block, new_motion_block)

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html)
print('done')
