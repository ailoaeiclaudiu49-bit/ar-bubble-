import re

with open('assets/webview.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix conflict 1
content = re.sub(
    r'<<<<<<< HEAD\n    <div class="hdr"><span>🎬</span><span class="hdr-title" id="play-title"></span><span class="hdr-badge">\$\{segs\.length\} Segs</span></div>\n=======\n    <div class="hdr"><span>🎬</span><span class="hdr-title" id="play-title"></span><span class="hdr-badge">\$\{segs\.length\} 段</span></div>\n>>>>>>> origin/main',
    r'    <div class="hdr"><span>🎬</span><span class="hdr-title" id="play-title"></span><span class="hdr-badge">${segs.length} Segs</span></div>',
    content,
    flags=re.DOTALL
)

# Fix conflict 2
content = re.sub(
    r'<<<<<<< HEAD\n    span\.textContent = `Speaker \$\{sp\}`;\n=======\n    span\.textContent = `说话人 \$\{sp\}`;\n>>>>>>> origin/main',
    r'    span.textContent = `Speaker ${sp}`;',
    content,
    flags=re.DOTALL
)

with open('assets/webview.html', 'w', encoding='utf-8') as f:
    f.write(content)
