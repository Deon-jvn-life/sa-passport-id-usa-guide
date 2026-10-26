"""Shared helpers: page shell, robots.txt, sitemap.xml, checks. Copied per site so each folder is self-contained."""
import os,html as H,shutil,re,sys,json,struct,zlib
from urllib.parse import urljoin
D="26 Oct 2026"
def esc(s): return H.escape(s,quote=True)
def a(url,text='source'): return f'<a href="{esc(url)}" rel="noopener">{text}</a>'
def page_base(page_path):
    if page_path.endswith("index.html"): base="/"+page_path[:-len("index.html")]
    else:
        d=os.path.dirname(page_path)
        base="/"+ (d+"/" if d else "")
    if not base.endswith("/"): base+="/"
    return base
def clean_href(page_path,href):
    if re.match(r'^[a-z][a-z0-9+.-]*:',href) or href.startswith('#'): return href
    base=page_base(page_path)
    joined=urljoin(base,href)
    if joined.endswith('index.html'): joined=joined[:-len('index.html')]
    path=joined.split('?')[0]
    if not path.endswith('/') and not re.search(r'\.[A-Za-z0-9]+$',path): joined+='/'
    return joined
def rewrite_hrefs(page_path,html):
    def repl(m): return 'href="'+esc(clean_href(page_path,H.unescape(m.group(1))))+'"'
    return re.sub(r'href="([^"]*)"',repl,html)
def html_text(fragment):
    fragment=re.sub(r'<span class="src">.*?</span>','',fragment,flags=re.S)
    fragment=re.sub(r'<[^>]+>',' ',fragment)
    fragment=re.sub(r'\s+',' ',H.unescape(fragment)).strip()
    return re.sub(r'\s+([.,;:!?])',r'\1',fragment)
def warn_meta(path,title,desc):
    if not 50<=len(title)<=60: print(f'WARNING: title length {len(title)} outside 50-60 for {path}: {title}',file=sys.stderr)
    if not 120<=len(desc)<=160: print(f'WARNING: description length {len(desc)} outside 120-160 for {path}: {desc}',file=sys.stderr)
def ld(nodes):
    raw=json.dumps({"@context":"https://schema.org","@graph":nodes},ensure_ascii=False,separators=(',',':'))
    return '<script type="application/ld+json">'+raw.replace('<','\\u003c')+'</script>'
def crumbs(nav,base,path,canon,crumb,link_last):
    items=[]
    def add(name,url=None):
        el={"@type":"ListItem","position":len(items)+1,"name":name}
        if url: el["item"]=url
        items.append(el)
    add("Home",base+"/")
    if path=="index.html": return items
    parts=path.split("/")
    if len(parts)==3 and parts[0]=="centres" and parts[-1]=="index.html":
        add("VFS centres",base+"/centres/")
        add(crumb or parts[1], canon if link_last else None)
        return items
    label=crumb
    if not label:
        for p,t in nav:
            if p==path: label=t; break
    add(label or "Page", canon if link_last else None)
    return items
# 5x7 uppercase glyphs, left bit is the high bit of each row.
FONT={
" ": [0,0,0,0,0,0,0],
"A":[0b01110,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001],
"B":[0b11110,0b10001,0b10001,0b11110,0b10001,0b10001,0b11110],
"C":[0b01110,0b10001,0b10000,0b10000,0b10000,0b10001,0b01110],
"D":[0b11110,0b10001,0b10001,0b10001,0b10001,0b10001,0b11110],
"E":[0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b11111],
"F":[0b11111,0b10000,0b10000,0b11110,0b10000,0b10000,0b10000],
"G":[0b01110,0b10001,0b10000,0b10111,0b10001,0b10001,0b01111],
"H":[0b10001,0b10001,0b10001,0b11111,0b10001,0b10001,0b10001],
"I":[0b11111,0b00100,0b00100,0b00100,0b00100,0b00100,0b11111],
"J":[0b00111,0b00010,0b00010,0b00010,0b10010,0b10010,0b01100],
"K":[0b10001,0b10010,0b10100,0b11000,0b10100,0b10010,0b10001],
"L":[0b10000,0b10000,0b10000,0b10000,0b10000,0b10000,0b11111],
"M":[0b10001,0b11011,0b10101,0b10101,0b10001,0b10001,0b10001],
"N":[0b10001,0b11001,0b10101,0b10011,0b10001,0b10001,0b10001],
"O":[0b01110,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
"P":[0b11110,0b10001,0b10001,0b11110,0b10000,0b10000,0b10000],
"Q":[0b01110,0b10001,0b10001,0b10001,0b10101,0b10010,0b01101],
"R":[0b11110,0b10001,0b10001,0b11110,0b10100,0b10010,0b10001],
"S":[0b01111,0b10000,0b10000,0b01110,0b00001,0b00001,0b11110],
"T":[0b11111,0b00100,0b00100,0b00100,0b00100,0b00100,0b00100],
"U":[0b10001,0b10001,0b10001,0b10001,0b10001,0b10001,0b01110],
"V":[0b10001,0b10001,0b10001,0b10001,0b10001,0b01010,0b00100],
"W":[0b10001,0b10001,0b10001,0b10101,0b10101,0b10101,0b01010],
"X":[0b10001,0b10001,0b01010,0b00100,0b01010,0b10001,0b10001],
"Y":[0b10001,0b10001,0b01010,0b00100,0b00100,0b00100,0b00100],
"Z":[0b11111,0b00001,0b00010,0b00100,0b01000,0b10000,0b11111],
}
def blank(w,h,color): return bytearray(bytes(color)*(w*h))
def fill(buf,w,h,x0,y0,x1,y1,color):
    x0=max(0,x0); y0=max(0,y0); x1=min(w,x1); y1=min(h,y1)
    if x0>=x1 or y0>=y1: return
    pix=bytes(color); span=pix*(x1-x0)
    for y in range(y0,y1):
        i=(y*w+x0)*3; buf[i:i+len(span)]=span
def text_width(text,scale):
    if not text: return 0
    return (len(text)-1)*(6*scale)+5*scale
def draw_text(buf,w,h,text,scale,x,y,color):
    for ch in text:
        glyph=FONT.get(ch,FONT[" "])
        for gy,bits in enumerate(glyph):
            for gx in range(5):
                if bits&(1<<(4-gx)):
                    fill(buf,w,h,x+gx*scale,y+gy*scale,x+(gx+1)*scale,y+(gy+1)*scale,color)
        x+=6*scale
def write_png(path,w,h,buf):
    raw=bytearray()
    stride=w*3
    for y in range(h):
        raw.append(0); raw.extend(buf[y*stride:(y+1)*stride])
    def chunk(tag,data):
        return struct.pack(">I",len(data))+tag+data+struct.pack(">I",zlib.crc32(tag+data)&0xffffffff)
    png=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(bytes(raw),9))+chunk(b"IEND",b"")
    open(path,"wb").write(png)
def write_assets(out):
    svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#123b5c"/><rect x="9" y="5" width="14" height="22" rx="1.5" fill="#ffffff"/><rect x="12" y="9" width="8" height="2" fill="#1f7a4d"/><rect x="12" y="13" width="8" height="2" fill="#e0b040"/><rect x="12" y="17" width="5" height="2" fill="#c43228"/></svg>'''
    open(os.path.join(out,"favicon.svg"),"w").write(svg)
    icon=blank(180,180,(18,59,92))
    fill(icon,180,180,46,28,134,154,(255,255,255))
    fill(icon,180,180,60,48,120,62,(31,122,77))
    fill(icon,180,180,60,72,120,86,(224,176,64))
    fill(icon,180,180,60,96,102,110,(196,50,40))
    write_png(os.path.join(out,"apple-touch-icon.png"),180,180,icon)
    og=blank(1200,630,(18,59,92))
    fill(og,1200,630,0,0,1200,18,(224,176,64))
    fill(og,1200,630,0,612,1200,630,(31,122,77))
    title,sub="SA PASSPORT AND ID GUIDE","SOUTH AFRICANS IN THE USA"
    draw_text(og,1200,630,title,8,(1200-text_width(title,8))//2,230,(255,255,255))
    draw_text(og,1200,630,sub,5,(1200-text_width(sub,5))//2,360,(240,226,176))
    write_png(os.path.join(out,"og.png"),1200,630,og)
class Site:
    def __init__(s,root,base,brand,nav,footer,css,related=None,disclaimer="",verify=None):
        s.out=os.path.join(root,"site"); s.base=base.rstrip("/"); s.brand=brand; s.nav=nav; s.footer=footer; s.css=css; s.pages=[]
        s.related=related or []; s.disclaimer=disclaimer or ""; s.verify=verify or {}
        if os.path.exists(s.out): shutil.rmtree(s.out)
        os.makedirs(s.out)
    def page(s,path,title,desc,body,checked=None,lastmod="2026-10-26",faq=None,crumb=None,sitemap=True,article=None,robots=None):
        warn_meta(path,title,desc)
        when=checked or D
        r="../"*path.count("/")
        nav="".join(f'<a href="{r}{p}">{t}</a>' for p,t in s.nav)
        canon=s.base+"/"+path.replace("index.html","")
        link_last=path!="404.html"
        if article is None: article=path not in ("index.html","404.html")
        nodes=[{"@type":"BreadcrumbList","itemListElement":crumbs(s.nav,s.base,path,canon,crumb,link_last)}]
        org={"@type":"Organization","name":s.brand,"url":s.base+"/","logo":s.base+"/apple-touch-icon.png"}
        if path=="index.html":
            nodes.append({"@type":"WebSite","name":s.brand,"url":s.base+"/","description":desc,"inLanguage":"en-US"})
            nodes.append({**org,"description":desc})
        if article:
            nodes.append({"@type":"Article","headline":title,"description":desc,"datePublished":lastmod,"dateModified":lastmod,"inLanguage":"en-US","mainEntityOfPage":{"@type":"WebPage","@id":canon},"author":{"@type":"Organization","name":s.brand,"url":s.base+"/"},"publisher":{"@type":"Organization","name":s.brand,"url":s.base+"/","logo":{"@type":"ImageObject","url":s.base+"/apple-touch-icon.png"}}})
        if faq:
            nodes.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":html_text(ans)}} for q,ans in faq]})
        bits=[]
        if link_last: bits.append(f'<link rel="canonical" href="{canon}">')
        if robots: bits.append(f'<meta name="robots" content="{esc(robots)}">')
        for name,value in s.verify.items():
            if value: bits.append(f'<meta name="{esc(name)}" content="{esc(value)}" />')
        bits.append('<link rel="icon" href="/favicon.svg" type="image/svg+xml">')
        bits.append('<link rel="apple-touch-icon" href="/apple-touch-icon.png">')
        og_type="article" if article else "website"
        img=s.base+"/og.png"
        bits.append(f'<meta property="og:title" content="{esc(title)}">')
        bits.append(f'<meta property="og:description" content="{esc(desc)}">')
        bits.append(f'<meta property="og:type" content="{og_type}">')
        bits.append(f'<meta property="og:site_name" content="{esc(s.brand)}">')
        bits.append(f'<meta property="og:locale" content="en_US">')
        if link_last: bits.append(f'<meta property="og:url" content="{canon}">')
        bits.append(f'<meta property="og:image" content="{img}">')
        bits.append('<meta property="og:image:width" content="1200">')
        bits.append('<meta property="og:image:height" content="630">')
        bits.append(f'<meta property="og:image:alt" content="{esc(s.brand)}">')
        bits.append('<meta name="twitter:card" content="summary_large_image">')
        bits.append(f'<meta name="twitter:title" content="{esc(title)}">')
        bits.append(f'<meta name="twitter:description" content="{esc(desc)}">')
        bits.append(f'<meta name="twitter:image" content="{img}">')
        bits.append(ld(nodes))
        rel=""
        if s.related:
            links=[a(url,text) for url,text in s.related]
            joined=links[0] if len(links)==1 else (", ".join(links[:-1])+" and "+links[-1])
            rel=f'<p class="related"><strong>Related guides</strong>: {joined}.</p>'
        disc=f'<p>{esc(s.disclaimer)}</p><p><a href="/disclaimer/">Disclaimer</a></p>' if s.disclaimer else ""
        top=f'<div class="disclaimer">{esc(s.disclaimer)}</div>' if s.disclaimer else ""
        h=f'''<!doctype html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{''.join(bits)}<style>{s.css}</style><script defer src="/_vercel/insights/script.js"></script></head><body>
<header><a class="brand" href="{r}index.html">{esc(s.brand)}</a><nav>{nav}</nav></header>
<div class="unofficial">Unofficial and independent guide. Not a government website.</div>
{top}<main><p class="checked">Last checked: {when}</p>
{body}
</main><footer>{s.footer}{disc}{rel}<p>Last checked: {when}.</p></footer></body></html>'''
        h=rewrite_hrefs(path,h)
        for bad in ("\u2014","\u2013","&mdash;","&ndash;"): assert bad not in h,(path,bad)
        p=os.path.join(s.out,path); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w").write(h)
        if sitemap: s.pages.append((path,lastmod))
    def finish(s):
        write_assets(s.out)
        bots=["GPTBot","OAI-SearchBot","ChatGPT-User","PerplexityBot","Bingbot","Googlebot","ClaudeBot","*"]
        open(os.path.join(s.out,"robots.txt"),"w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"Sitemap: {s.base}/sitemap.xml\n")
        open(os.path.join(s.out,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{s.base}/{p.replace('index.html','')}</loc><lastmod>{mod}</lastmod></url>\n" for p,mod in sorted(s.pages))+"</urlset>\n")
CSS='''body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1a1a1a;line-height:1.55;background:#fafaf7}header{background:#123b5c;color:#fff;padding:.7rem 1rem;display:flex;flex-wrap:wrap;gap:.6rem 1.2rem;align-items:center}header a{color:#fff;text-decoration:none}.brand{font-weight:700}nav{display:flex;flex-wrap:wrap;gap:.3rem .9rem;font-size:.95rem}nav a:hover{text-decoration:underline}.unofficial{background:#fff4d6;border-bottom:1px solid #e6cf8a;padding:.4rem 1rem;font-size:.9rem}.disclaimer{background:#f3efe6;border-bottom:1px solid #e0d8c8;padding:.5rem 1rem;font-size:.88rem;color:#222}main{max-width:1100px;margin:0 auto;padding:1rem}h1{font-size:1.7rem;line-height:1.25}h2{margin-top:1.8rem}.checked{display:inline-block;background:#e6f2ea;border:1px solid #a9d1b5;border-radius:4px;padding:.15rem .5rem;font-size:.9rem}.card{background:#fff;border:1px solid #ddd;border-radius:6px;padding:.8rem 1rem;margin:.8rem 0}.warn{border-left:6px solid #c0392b;background:#fdeeee}.note{border-left:6px solid #d68910;background:#fff8ec}.conf{border-left:6px solid #8e44ad;background:#f6effa}.wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;background:#fff;font-size:.93rem}th,td{border:1px solid #ddd;padding:.45rem;vertical-align:top;text-align:left}th{background:#eef3f7}.src{font-size:.85rem;color:#555}.tag{display:inline-block;font-size:.78rem;padding:0 .35rem;border-radius:3px;background:#eee;margin-right:.2rem}.tag.ok{background:#d8f0de}.tag.no{background:#f8d7d7}.tag.mix{background:#fdebc8}footer{max-width:1100px;margin:2rem auto;padding:1rem;font-size:.88rem;color:#444;border-top:1px solid #ddd}footer .related{margin:.5rem 0}a{color:#0b5394}input#q{width:100%;max-width:420px;padding:.45rem;margin:.5rem 0;font-size:1rem}'''
