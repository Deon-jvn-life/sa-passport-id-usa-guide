"""Shared helpers: page shell, topic menu, breadcrumbs, read next, search, robots.txt, sitemap.xml, checks."""
import os,html as H,shutil,re,sys,json,struct,zlib
from urllib.parse import urljoin
D="26 Oct 2026"
ISO="2026-10-26"
HEADER_PHRASE="Independent guide. Not a government website."
UNOFFICIAL="Unofficial and independent guide. Not a government website."
def esc(s): return H.escape(s,quote=True)
def a(url,text='source'): return f'<a href="{esc(url)}" rel="noopener">{text}</a>'
def slug(t):
    t=H.unescape(re.sub(r'<[^>]+>','',t))
    return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-') or 'section'
def href(path):
    if path in ('index.html','/'): return '/'
    if path.endswith('/index.html'): return '/'+path[:-len('index.html')]
    if path.endswith('.html'): return '/'+path
    return '/'+path
def canon_url(base, path):
    return base.rstrip('/')+href(path)
def page_base(page_path):
    if page_path.endswith("index.html"): base="/"+page_path[:-len("index.html")]
    else:
        d=os.path.dirname(page_path)
        base="/"+ (d+"/" if d else "")
    if not base.endswith("/"): base+="/"
    return base
def clean_href(page_path,href_v):
    if re.match(r'^[a-z][a-z0-9+.-]*:',href_v) or href_v.startswith('#') or href_v.startswith('/'): return href_v
    base=page_base(page_path)
    joined=urljoin(base,href_v)
    if joined.endswith('index.html'): joined=joined[:-len('index.html')]
    path=joined.split('?')[0].split('#')[0]
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
def _star(cx,cy,r):
    import math
    pts=[]
    for i in range(10):
        ang=-math.pi/2+i*math.pi/5
        rad=r if i%2==0 else r*0.381966
        pts.append(f'{cx+rad*math.cos(ang):.2f},{cy+rad*math.sin(ang):.2f}')
    return ' '.join(pts)
def _us_flag_inner():
    stripes=[]
    sh=100/13
    for i in range(13):
        if i%2==0:
            stripes.append(f'<rect y="{i*sh:.3f}" width="190" height="{sh+0.15:.3f}" fill="#B22234"/>')
    ch=7*sh
    E=76/12
    F=ch/10
    stars=[]
    for row in range(9):
        y=F*(row+1)
        xs=[E*(1+2*k) for k in range(6)] if row%2==0 else [E*(2+2*k) for k in range(5)]
        for x in xs:
            stars.append(f'<polygon fill="#fff" points="{_star(x,y,E*0.42)}"/>')
    return ('<rect width="190" height="100" fill="#fff"/>'+''.join(stripes)+
            f'<rect width="76" height="{ch:.3f}" fill="#3C3B6E"/>'+''.join(stars))
SA_FLAG='''<svg class="flag" role="img" aria-label="South African flag" viewBox="0 0 90 60" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="za-t"><path d="m0 0 45 30L0 60z"/></clipPath><clipPath id="za-f"><path d="m0 0h90v60H0z"/></clipPath></defs><path fill="#E03C31" d="m0 0h90v30H45z"/><path fill="#001489" d="m0 60h90V30H45z"/><g clip-path="url(#za-f)" fill="none"><path stroke="#FFF" stroke-width="20" d="m90 30H45L0 0v60l45-30"/><path fill="#000" stroke="#ffb81c" stroke-width="20" clip-path="url(#za-t)" d="m0 0 45 30L0 60"/><path stroke="#007749" stroke-width="12" d="m0 0 45 30h45M0 60l45-30"/></g></svg>'''
US_FLAG='<svg class="flag" role="img" aria-label="United States flag" viewBox="0 0 190 100" xmlns="http://www.w3.org/2000/svg">'+_us_flag_inner()+'</svg>'
FLAGS=f'<span class="flags">{SA_FLAG}{US_FLAG}</span>'
def write_assets(out):
    svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#014233"/><rect x="9" y="5" width="14" height="22" rx="1.5" fill="#ffffff"/><rect x="12" y="9" width="8" height="2" fill="#007749"/><rect x="12" y="13" width="8" height="2" fill="#E6C35C"/><rect x="12" y="17" width="5" height="2" fill="#7A1A28"/></svg>'''
    open(os.path.join(out,"favicon.svg"),"w").write(svg)
    icon=blank(180,180,(1,66,51))
    fill(icon,180,180,46,28,134,154,(255,255,255))
    fill(icon,180,180,60,48,120,62,(0,119,73))
    fill(icon,180,180,60,72,120,86,(230,195,92))
    fill(icon,180,180,60,96,102,110,(122,26,40))
    write_png(os.path.join(out,"apple-touch-icon.png"),180,180,icon)
    og=blank(1200,630,(1,66,51))
    fill(og,1200,630,0,0,1200,18,(230,195,92))
    fill(og,1200,630,0,612,1200,630,(122,26,40))
    title,sub="SA PASSPORT AND ID GUIDE","SOUTH AFRICANS IN THE USA"
    draw_text(og,1200,630,title,8,(1200-text_width(title,8))//2,230,(255,255,255))
    draw_text(og,1200,630,sub,5,(1200-text_width(sub,5))//2,360,(255,224,138))
    write_png(os.path.join(out,"og.png"),1200,630,og)

SEARCH_JS=r'''(function(){
  var el=document.getElementById("search-data");
  var input=document.getElementById("q");
  var box=document.getElementById("search-results");
  if(!el||!input||!box) return;
  var pages=[];
  try { pages=JSON.parse(el.textContent); } catch(e){ return; }
  function escHtml(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c];
    });
  }
  function activeWords(q){
    var t=String(q||"").trim().toLowerCase();
    if(t.length<2) return [];
    return t.split(/\s+/).filter(function(w){ return w; });
  }
  function match(blob, ws){
    if(!ws.length) return true;
    blob=String(blob).toLowerCase();
    for(var i=0;i<ws.length;i++) if(blob.indexOf(ws[i])<0) return false;
    return true;
  }
  function filterIndex(q){
    var root=document.getElementById("page-index");
    if(!root) return;
    var ws=activeWords(q);
    var items=root.querySelectorAll("li");
    var shown=0;
    for(var i=0;i<items.length;i++){
      var li=items[i];
      var blob=li.textContent+" "+(li.getAttribute("data-keywords")||"");
      var ok=match(blob, ws);
      li.hidden=!ok;
      if(ok) shown++;
    }
    var sections=root.querySelectorAll("section");
    for(var s=0;s<sections.length;s++){
      var sec=sections[s];
      var lis=sec.querySelectorAll("li");
      var any=false;
      for(var k=0;k<lis.length;k++) if(!lis[k].hidden) any=true;
      sec.hidden=!any;
    }
    var status=document.getElementById("index-status");
    if(status){
      if(!ws.length) status.textContent="Showing every page.";
      else if(!shown) status.textContent="No page matches. Try a different word, or clear the search.";
      else status.textContent="Showing "+shown+" of "+items.length+" pages.";
    }
  }
  function show(q){
    var ws=activeWords(q);
    if(!ws.length){
      box.hidden=true;
      box.innerHTML="";
    } else {
      var hits=[];
      for(var i=0;i<pages.length;i++){
        var p=pages[i];
        var blob=p.t+" "+p.s+" "+p.g+" "+(p.k||"");
        if(match(blob, ws)) hits.push(p);
        if(hits.length===8) break;
      }
      if(!hits.length){
        box.innerHTML="<p class=\"search-empty\">No matching page. Open the <a href=\"/find/\">full page list</a>.</p>";
      } else {
        var html="<ul>";
        for(var j=0;j<hits.length;j++){
          var hit=hits[j];
          html+="<li><a href=\""+escHtml(hit.u)+"\"><strong>"+escHtml(hit.t)+"</strong><span>"+escHtml(hit.s)+"</span></a></li>";
        }
        html+="</ul>";
        box.innerHTML=html;
      }
      box.hidden=false;
    }
    filterIndex(q);
  }
  input.addEventListener("input", function(){ show(input.value); });
  input.addEventListener("keydown", function(e){
    if(e.key==="Escape"){ box.hidden=true; box.innerHTML=""; }
  });
  document.addEventListener("click", function(e){
    if(!box.contains(e.target) && e.target!==input){ box.hidden=true; }
  });
  var initial="";
  try { initial=new URLSearchParams(window.location.search).get("q")||""; } catch(err){ initial=""; }
  if(initial){ input.value=initial; show(initial); }
  else filterIndex("");
})();'''
DOCK_JS=r'''(function(){
  var header=document.getElementById("site-header");
  var slot=document.getElementById("head-slot");
  var toggle=document.querySelector(".search-toggle");
  var search=document.getElementById("site-search");
  var nav=document.getElementById("site-nav");
  if(!header||!slot) return;
  var docked=false;
  var fullH=0;
  function compactPx(){
    var raw=getComputedStyle(document.documentElement).getPropertyValue("--header-compact")||"124px";
    var n=parseFloat(raw);
    if(String(raw).indexOf("rem")>=0){
      n=n*parseFloat(getComputedStyle(document.documentElement).fontSize||"16");
    }
    return n||124;
  }
  function place(){
    var b=header.getBoundingClientRect().bottom;
    if(b<0) b=0;
    document.documentElement.style.setProperty("--header-bottom", b+"px");
  }
  function setSearchOpen(open){
    if(!search||!toggle) return;
    if(open && !document.body.classList.contains("is-docked")) open=false;
    search.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open?"true":"false");
    if(open) closeGroups();
    if(open){
      var input=document.getElementById("q");
      if(input) input.focus();
    }
    place();
  }
  function closeGroups(){
    var open=document.querySelectorAll(".grp[open]");
    for(var i=0;i<open.length;i++) open[i].removeAttribute("open");
  }
  function measure(){
    if(docked) return;
    fullH=header.offsetHeight;
    place();
  }
  function updateHint(){
    if(!nav) return;
    var more=nav.scrollWidth>nav.clientWidth+8;
    var atEnd=nav.scrollLeft+nav.clientWidth>=nav.scrollWidth-8;
    var atStart=nav.scrollLeft<=8;
    document.body.classList.toggle("nav-more-right", !!(more && !atEnd));
    document.body.classList.toggle("nav-more-left", !!(more && !atStart));
  }
  function revealCurrent(){
    if(!nav) return;
    var cur=nav.querySelector(".grp.has-current")||nav.querySelector(".grp");
    if(!cur || nav.scrollWidth<=nav.clientWidth+8){ updateHint(); return; }
    var left=cur.offsetLeft-(nav.clientWidth-cur.offsetWidth)/2;
    nav.scrollLeft=left<0?0:left;
    updateHint();
  }
  function dock(){
    if(docked) return;
    closeGroups();
    setSearchOpen(false);
    measure();
    if(!fullH) fullH=header.offsetHeight;
    slot.style.height=fullH+"px";
    document.body.classList.add("is-docked");
    docked=true;
    place();
    revealCurrent();
  }
  function undock(){
    if(!docked) return;
    setSearchOpen(false);
    closeGroups();
    document.body.classList.remove("is-docked");
    document.body.classList.remove("nav-more-right");
    document.body.classList.remove("nav-more-left");
    slot.style.height="";
    docked=false;
    measure();
  }
  function onScroll(){
    var y=window.scrollY||document.documentElement.scrollTop||0;
    if(!fullH) measure();
    var line=fullH-compactPx();
    if(!docked){
      measure();
      if(fullH>compactPx() && y>fullH-compactPx()) dock();
    } else if(y<line-24){
      undock();
    }
    place();
  }
  if(toggle){
    toggle.addEventListener("click", function(){
      var open=toggle.getAttribute("aria-expanded")==="true";
      setSearchOpen(!open);
    });
  }
  document.addEventListener("keydown", function(e){
    if(e.key!=="Escape") return;
    setSearchOpen(false);
    closeGroups();
    var box=document.getElementById("search-results");
    if(box){ box.hidden=true; box.innerHTML=""; }
  });
  document.addEventListener("click", function(e){
    if(header.contains(e.target)) return;
    setSearchOpen(false);
    closeGroups();
  });
  if(nav){
    nav.addEventListener("scroll", updateHint, {passive:true});
    var topicSums=nav.querySelectorAll(".grp>summary");
    for(var s=0;s<topicSums.length;s++){
      topicSums[s].addEventListener("pointerdown", place);
      topicSums[s].addEventListener("click", function(){
        setSearchOpen(false);
        place();
        var self=this.parentNode;
        var open=document.querySelectorAll(".grp[open]");
        for(var i=0;i<open.length;i++) if(open[i]!==self) open[i].removeAttribute("open");
      });
    }
  }
  document.addEventListener("focusin", function(e){
    var t=e.target;
    if(!t||!docked) return;
    if(nav && nav.contains(t) && nav.scrollWidth>nav.clientWidth+8 && t.closest){
      var grp=t.closest(".grp");
      if(grp){
        var pad=16;
        var left=grp.offsetLeft-pad;
        var right=grp.offsetLeft+grp.offsetWidth+pad;
        if(left<nav.scrollLeft) nav.scrollLeft=Math.max(0,left);
        else if(right>nav.scrollLeft+nav.clientWidth) nav.scrollLeft=right-nav.clientWidth;
        updateHint();
      }
    }
    if(header.contains(t)||(t.classList&&t.classList.contains("skip"))) return;
    var edge=compactPx()+12;
    var r=t.getBoundingClientRect();
    if(r.bottom>edge && r.top>=edge) return;
    var y=(window.scrollY||0)+r.top-edge;
    window.scrollTo(0, y<0?0:y);
  });
  window.addEventListener("scroll", onScroll, {passive:true});
  window.addEventListener("resize", function(){
    if(docked) undock();
    measure();
    onScroll();
  });
  measure();
  onScroll();
})();'''
TOC_BOOT='<script>if(window.matchMedia("(min-width:960px)").matches){var d=document.currentScript.previousElementSibling;if(d&&d.tagName==="DETAILS")d.open=true;}</script>'

class Site:
    def __init__(s,root,base,brand,groups,order,footer,css,related=None,disclaimer="",verify=None):
        s.out=os.path.join(root,"site"); s.base=base.rstrip("/"); s.brand=brand; s.groups=groups; s.order=order
        s.footer=footer; s.css=css; s.pages=[]; s.indexable=[]; s.related=related or []; s.disclaimer=disclaimer or ""; s.verify=verify or {}
        s.titles={p:t for g,items in groups for p,t in items}
        s.titles['index.html']='Home'
        s.summaries={}; s.read_next={}; s.aliases={}; s.long_pages=set(); s.flow_toc=set(); s._search_cache=None
        s.stage={p:g for g,items in groups for p,t in items}
        if os.path.exists(s.out): shutil.rmtree(s.out)
        os.makedirs(s.out)
    def _search_json(s):
        if s._search_cache is not None: return s._search_cache
        rows=[{"u":"/","t":"Home","s":"Start here, top tasks, and every topic.","g":"Home","k":"guide home passport identity"}]
        for g,items in s.groups:
            for p,t in items:
                rows.append({"u":href(p),"t":t,"s":s.summaries.get(p,""),"g":g,"k":s.aliases.get(p,"")})
        s._search_cache=json.dumps(rows,ensure_ascii=False).replace("<","\\u003c")
        return s._search_cache
    def _crumbs(s,path,crumb,canon,link_last):
        if path=="index.html":
            html='<nav class="crumbs" aria-label="Breadcrumb"><ol><li><span aria-current="page">Home</span></li></ol></nav>'
            ld_items=[{"@type":"ListItem","position":1,"name":"Home","item":s.base+"/"}]
            return html, ld_items
        label=crumb or s.titles.get(path) or "Page"
        stage=s.stage.get(path)
        html_items=['<li><a href="/">Home</a></li>']
        ld_items=[{"@type":"ListItem","position":1,"name":"Home","item":s.base+"/"}]
        pos=2
        if stage:
            html_items.append(f'<li><a href="/#{slug(stage)}">{esc(stage)}</a></li>')
            ld_items.append({"@type":"ListItem","position":pos,"name":stage,"item":s.base+"/#"+slug(stage)})
            pos+=1
        if path.startswith("centres/") and path!="centres/index.html":
            html_items.append('<li><a href="/centres/">All centres</a></li>')
            ld_items.append({"@type":"ListItem","position":pos,"name":"All centres","item":s.base+"/centres/"})
            pos+=1
        html_items.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
        last={"@type":"ListItem","position":pos,"name":label}
        if link_last: last["item"]=canon
        ld_items.append(last)
        html='<nav class="crumbs" aria-label="Breadcrumb"><ol>'+''.join(html_items)+'</ol></nav>'
        return html, ld_items
    def page(s,path,title,desc,body,checked=None,lastmod=ISO,faq=None,crumb=None,sitemap=True,article=None,robots=None):
        warn_meta(path,title,desc)
        when=checked or D
        iso=lastmod or ISO
        if '<h1>' in body:
            body=body.replace('<h1>','<h1 id="page-title">',1)
        summary=s.summaries.get(path,'')
        if summary and path in s.long_pages and '<h1' in body:
            body=body.replace('</h1>','</h1><div class="inshort"><p><strong>In short.</strong> '+esc(summary)+'</p></div>',1)
        seen={}
        h2_items=[]
        def addid(m):
            inner=m.group(1)
            base=slug(inner)
            n=seen.get(base,0)+1
            seen[base]=n
            id_=base if n==1 else f"{base}-{n}"
            h2_items.append((id_, inner))
            return f'<h2 id="{id_}">{inner}</h2>'
        body=re.sub(r'<h2>(.*?)</h2>',addid,body,flags=re.S)
        h2pos=body.find('<h2')
        if h2pos==-1:
            head, rest = body, ''
        else:
            head, rest = body[:h2pos], body[h2pos:]
        toc=''
        if len(h2_items)>=3:
            opened=' open' if len(h2_items)<=8 else ''
            lis=''.join(f'<li><a href="#{id_}">{esc(H.unescape(re.sub("<[^>]+>","",inner)))}</a></li>' for id_,inner in h2_items)
            toc=f'<nav class="toc" aria-label="On this page"><details class="toc-details"{opened}><summary>On this page</summary><ul>{lis}</ul></details>{TOC_BOOT}</nav>'
        nav_bits=[]
        for g,items in s.groups:
            links=[]
            here=False
            for p,t in items:
                cur=' aria-current="page"' if p==path else ''
                cls=' class="is-current"' if p==path else ''
                if p==path: here=True
                links.append(f'<a href="{href(p)}"{cls}{cur}>{esc(t)}</a>')
            mark=' aria-current="true"' if here else ''
            nav_bits.append(f'<details class="grp{" has-current" if here else ""}"><summary{mark}>{esc(g)}</summary><div class="glinks">'+''.join(links)+'</div></details>')
        nav=''.join(nav_bits)
        canon=canon_url(s.base, path)
        link_last=path!="404.html"
        if article is None: article=path not in ("index.html","404.html")
        kind='error' if path=='404.html' else ('home' if path=='index.html' else 'article')
        crumbs_html, crumbs_ld=s._crumbs(path, crumb, canon, link_last)
        h1m=re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        headline=H.unescape(re.sub(r'<[^>]+>','', h1m.group(1))) if h1m else title
        nodes=[{"@type":"BreadcrumbList","itemListElement":crumbs_ld}]
        org={"@type":"Organization","name":s.brand,"url":s.base+"/","logo":s.base+"/apple-touch-icon.png"}
        if kind=='home':
            nodes.append({"@type":"WebSite","name":s.brand,"url":s.base+"/","description":desc,"inLanguage":"en-US"})
            nodes.append({**org,"description":desc})
        if article:
            nodes.append({"@type":"Article","headline":title,"description":desc,"datePublished":iso,"dateModified":iso,"inLanguage":"en-US","mainEntityOfPage":{"@type":"WebPage","@id":canon},"author":{"@type":"Organization","name":s.brand,"url":s.base+"/"},"publisher":{"@type":"Organization","name":s.brand,"url":s.base+"/","logo":{"@type":"ImageObject","url":s.base+"/apple-touch-icon.png"}}})
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
        bits.append('<meta property="og:locale" content="en_US">')
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
        foot=s.footer if s.footer.strip().startswith("<") else f'<p>{s.footer}</p>'
        plain=s.titles.get(path, headline)
        def step_link(target, kind_):
            label=s.titles.get(target)
            if not label: return ''
            word='Previous' if kind_=='prev' else 'Next'
            return f'<a class="{kind_}" href="{href(target)}"><span class="pn-k">{word}</span><span class="pn-t">{esc(label)}</span></a>'
        pn=''
        if path in s.order:
            i=s.order.index(path)
            prev=step_link(s.order[i-1],'prev') if i>0 else ''
            nxt=step_link(s.order[i+1],'next') if i+1<len(s.order) else ''
            if prev or nxt:
                pn='<nav class="pn" aria-label="Previous and next page">'+prev+nxt+'</nav>'
        rn_items=[]
        for dest in s.read_next.get(path) or []:
            label=s.titles.get(dest) or ('Home' if dest=='index.html' else None)
            if not label: continue
            blurb=s.summaries.get(dest,'')
            blurb_html=f'<span class="ls">{esc(blurb)}</span>' if blurb else ''
            rn_items.append(f'<li><a class="jump" href="{href(dest)}"><span class="lt">{esc(label)}</span>{blurb_html}</a></li>')
        readnext='<aside class="readnext" aria-labelledby="read-next"><h2 id="read-next">Read next</h2><ul>'+''.join(rn_items)+'</ul></aside>' if rn_items else ''
        layout_cls='layout' if (not toc or path in s.flow_toc) else 'layout has-toc'
        if toc and path in s.flow_toc:
            layout_cls='layout'
        elif toc:
            layout_cls='layout has-toc'
        else:
            layout_cls='layout'
        book='<a class="book" href="https://services.vfsglobal.com/usa/en/zap/" rel="noopener"><span class="book-long">Book an appointment</span><span class="book-short">Book</span></a>'
        h=f'''<!doctype html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#014233"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{''.join(bits)}<style>{s.css}</style><script defer src="/_vercel/insights/script.js"></script></head><body>
<a class="skip" href="#content">Skip to content</a>
<div id="head-slot"><header id="site-header"><div class="shell">
<a class="brand" href="/">{FLAGS}<span class="name"><span class="name-main">South African passport and identity guide</span><span class="name-compact">Passport guide</span></span></a>
<p class="name-sub">{HEADER_PHRASE}</p>
<button type="button" class="search-toggle" aria-expanded="false" aria-controls="site-search"><svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 15.5 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><span class="search-toggle-text">Search</span></button>
<a class="headlink" href="/find/">All pages</a>
<span class="headcta">{book}</span>
<div class="search-wrap" id="site-search"><form class="sitesearch" role="search" action="/find/" method="get"><label for="q">Search this guide</label><input id="q" name="q" type="search" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"><button type="submit">Search</button></form><div id="search-results" class="search-results" hidden role="region" aria-live="polite" aria-label="Matching pages"></div></div>
<nav id="site-nav" class="top" aria-label="Topics">{nav}</nav>
<span class="nav-fade nav-fade-left" aria-hidden="true"></span><span class="nav-fade nav-fade-right" aria-hidden="true"></span><span class="nav-hint" aria-hidden="true"></span>
</div></header></div>
<main id="content" tabindex="-1"><div class="notice" role="note"><div class="shell"><p class="unofficial"><strong>{UNOFFICIAL}</strong></p><p>{esc(s.disclaimer)}</p></div></div><div class="shell">{crumbs_html}<article class="content" aria-labelledby="page-title"><p class="meta"><span class="checked">Last checked: {when}</span></p><div class="head-block">{head}</div><div class="{layout_cls}">{toc}<div class="rest">{rest}{pn}{readnext}</div></div></article></div></main>
<footer><div class="shell"><nav class="footnav" aria-label="About this guide"><a href="/find/">All pages</a><a href="/faq/">Common questions</a><a href="/disclaimer/">Disclaimer</a></nav>{foot}{disc}{rel}<p>Last checked: {when}.</p></div></footer>
<script type="application/json" id="search-data">{s._search_json()}</script><script>{SEARCH_JS}</script><script>{DOCK_JS}</script></body></html>'''
        h=rewrite_hrefs(path,h)
        for bad in ("\u2014","\u2013","&mdash;","&ndash;"): assert bad not in h,(path,bad)
        p=os.path.join(s.out,path); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w").write(h)
        s.pages.append(path)
        if sitemap: s.indexable.append((path,iso))
    def finish(s):
        write_assets(s.out)
        ratios=_contrast_report(s.css)
        bots=["GPTBot","OAI-SearchBot","ChatGPT-User","PerplexityBot","Bingbot","Googlebot","ClaudeBot","*"]
        open(os.path.join(s.out,"robots.txt"),"w").write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+f"Sitemap: {s.base}/sitemap.xml\n")
        open(os.path.join(s.out,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{canon_url(s.base,p)}</loc><lastmod>{mod}</lastmod></url>\n" for p,mod in sorted(s.indexable))+"</urlset>\n")
        gsc=s.verify.get("google-site-verification","")
        needles=(HEADER_PHRASE,UNOFFICIAL,s.disclaimer,"Last checked:","/_vercel/insights/script.js","system-ui,-apple-system,\"Segoe UI\",Roboto,sans-serif")
        for path in s.pages:
            html=open(os.path.join(s.out,path),encoding="utf-8").read()
            for needle in needles:
                if needle and needle not in html:
                    raise SystemExit(f"Missing {needle} on {path}")
            if gsc and gsc not in html:
                raise SystemExit("Missing Google verification on "+path)
            if "Read next" not in html:
                raise SystemExit("Missing Read next on "+path)
            if path!="404.html":
                if f'rel="canonical" href="{s.base}/' not in html and f'rel="canonical" href="{s.base}"' not in html:
                    raise SystemExit("Missing canonical on "+path)
                if "noindex" in html:
                    raise SystemExit("Unexpected noindex on "+path)
            elif "noindex" not in html:
                raise SystemExit("404 should be noindex")
        missing=_check_links(s.out, s.pages)
        if missing: raise SystemExit("Broken internal links:\n"+"\n".join(missing[:40]))
        print("Header contrast, white text, worst stop and midpoint", f"{ratios['worst_white']:.2f}:1")
        for row in ratios["rows"]:
            print(f"  {row}")

def _lin(c):
    c=c/255
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def _lum(hexv):
    h=hexv.lstrip("#")
    r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return 0.2126*_lin(r)+0.7152*_lin(g)+0.0722*_lin(b)
def _contrast(a,b):
    L1,L2=_lum(a),_lum(b)
    hi,lo=max(L1,L2),min(L1,L2)
    return (hi+0.05)/(lo+0.05)
def _rgb(hexv):
    h=hexv.lstrip("#")
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def _hex(rgb):
    return "#"+"".join(f"{max(0,min(255,round(c*255))):02X}" for c in rgb)
def _lerp(a,b,t):
    A,B=_rgb(a),_rgb(b)
    return _hex(tuple(A[i]+(B[i]-A[i])*t for i in range(3)))
def _srgb_to_oklab(hexv):
    r,g,b=_rgb(hexv)
    def f(c):
        return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    r,g,b=f(r),f(g),f(b)
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b
    m=0.2119034982*r+0.6806995451*g+0.1073969566*b
    s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=l**(1/3),m**(1/3),s**(1/3)
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s,
            1.9779984951*l-2.4285922050*m+0.4505937099*s,
            0.0259040371*l+0.7827717662*m-0.8086757660*s)
def _oklab_to_srgb(L,a,b):
    l=L+0.3963377774*a+0.2158037573*b
    m=L-0.1055613458*a-0.0638541728*b
    s=L-0.0894841775*a-1.2914855480*b
    l,m,s=l**3,m**3,s**3
    r=+4.0767416621*l-3.3077115913*m+0.2309699292*s
    g=-1.2684380046*l+2.6097574011*m-0.3413193965*s
    bl=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    def enc(c):
        if c<=0: c=0
        if c>=1: c=1
        return 12.92*c if c<=0.0031308 else 1.055*(c**(1/2.4))-0.055
    return _hex((enc(r),enc(g),enc(bl)))
def _oklab_lerp(a,b,t):
    A,B=_srgb_to_oklab(a),_srgb_to_oklab(b)
    return _oklab_to_srgb(*(A[i]+(B[i]-A[i])*t for i in range(3)))
def _contrast_report(css):
    stops=re.findall(r'--head-(\d):\s*(#[0-9A-Fa-f]{6})', css)
    if len(stops)<3:
        raise SystemExit("Header colour stops were not found in CSS")
    colors=[c for _n,c in stops]
    white,gold="#FFFFFF","#FFE08A"
    rows=[]
    worst_white=99
    worst_gold=99
    samples=[]
    for i,c in enumerate(colors):
        samples.append((f"stop {i+1} {c}", c))
    pairs=[(colors[0],colors[1]),(colors[1],colors[2])]
    for a,b in pairs:
        for t in (0.25,0.5,0.75):
            samples.append((f"srgb {a}-{b} {t:.2f} {_lerp(a,b,t)}", _lerp(a,b,t)))
            samples.append((f"oklab {a}-{b} {t:.2f} {_oklab_lerp(a,b,t)}", _oklab_lerp(a,b,t)))
    for label,col in samples:
        cw,cg=_contrast(white,col),_contrast(gold,col)
        worst_white=min(worst_white,cw)
        worst_gold=min(worst_gold,cg)
        rows.append(f"{label}: white {cw:.2f}:1, gold mark {cg:.2f}:1")
        if cw<4.5 or cg<3:
            raise SystemExit(f"Header contrast failed at {label}: white {cw:.2f}, gold {cg:.2f}")
    ink_gold=_contrast("#1A1814","#FFE08A")
    if ink_gold<4.5:
        raise SystemExit(f"Book button contrast failed: {ink_gold:.2f}")
    rows.append(f"book button ink on gold: {ink_gold:.2f}:1")
    return {"worst_white":worst_white,"worst_gold":worst_gold,"rows":rows}

def _check_links(out, pages):
    missing=[]
    for path in pages:
        html=open(os.path.join(out, path), encoding="utf-8").read()
        ids=set(re.findall(r'\bid="([^"]*)"', html))
        for href_v in re.findall(r'\bhref="([^"]*)"', html):
            if href_v.startswith(("http://","https://","mailto:","tel:")): continue
            url, _, frag = href_v.partition("#")
            if url=="":
                if frag and frag not in ids: missing.append(f"{path} -> {href_v}")
                continue
            if url.startswith("/"):
                rel=url.lstrip("/")
                target="index.html" if rel=="" else (rel+"index.html" if rel.endswith("/") else rel)
            else:
                target=os.path.normpath(os.path.join(os.path.dirname(path), url)).replace("\\","/")
            dest=os.path.join(out, target)
            if not os.path.isfile(dest):
                missing.append(f"{path} -> {href_v} (missing {target})"); continue
            if frag:
                tids=set(re.findall(r'\bid="([^"]*)"', open(dest, encoding="utf-8").read()))
                if frag not in tids: missing.append(f"{path} -> {href_v} (missing #{frag})")
    return missing

CSS=r''':root{--s12:12px;--s16:16px;--s24:24px;--s32:32px;--s40:40px;--header-compact:176px;--scroll-pad:188px;--header-bottom:176px;--ink:#1a1814;--paper:#f4f1ea;--link:#0a3d66;--visited:#3d2a6b;--line:#d9d3c7;--gold:#ffe08a;--head-1:#014233;--head-2:#7A1A28;--head-3:#10244F;--head-bg:linear-gradient(90deg,var(--head-1) 0%,var(--head-2) 52%,var(--head-3) 100%)}
@media(min-width:900px){:root{--header-compact:124px;--scroll-pad:136px}}
*,*::before,*::after{box-sizing:border-box}
html{color-scheme:light}
body{margin:0;color:var(--ink);background:var(--paper);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:1.125rem;line-height:1.6}
h1,h2,h3,h4,h5,h6,button,input,textarea,select,summary,label{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
h1,h2,h3,h4,h5,h6,strong,b,summary{font-weight:700}
[hidden]{display:none!important}
img,svg{max-width:100%}
h1,h2,h3,h4,h5,h6,.topic,section[id]{scroll-margin-top:var(--scroll-pad)}
.flag{height:22px;width:auto;max-width:none;display:block;border-radius:2px;box-shadow:0 0 0 1px rgba(255,255,255,.45)}
.shell{max-width:76rem;margin:0 auto;padding:0 var(--s16);min-width:0}
.skip{position:fixed;left:var(--s12);top:var(--s12);transform:translateY(-160%);background:#fff;color:var(--ink);padding:var(--s12) var(--s16);z-index:80;min-height:44px;font-weight:700;border-radius:8px}
.skip:focus,.skip:focus-visible{transform:none}
#head-slot{min-width:0}
#site-header{background-color:var(--head-1);background-image:var(--head-bg);color:#fff;position:relative;z-index:30}
#site-header a{color:#fff}
#site-header .shell{display:grid;grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"brand cta" "sub sub" "links links" "search search" "nav nav";align-items:center;column-gap:var(--s16);row-gap:var(--s12);padding-top:var(--s24);padding-bottom:var(--s24);position:relative}
.brand{grid-area:brand;display:flex;align-items:center;gap:var(--s12);min-width:0;color:#fff;text-decoration:none;font-weight:700;min-height:44px}
.flags{display:inline-flex;gap:8px;flex:none;align-items:center}
.name{display:flex;flex-direction:column;min-width:0}
.name-main{font-size:1.25rem;line-height:1.3;font-weight:700}
.name-compact{display:none}
.name-sub{grid-area:sub;margin:0;font-size:1rem;font-weight:700;color:#fff;line-height:1.35}
.headlink{grid-area:links;display:inline-flex;align-items:center;min-height:44px;padding:var(--s12) 0;font-weight:700;text-decoration:underline;text-underline-offset:.15em}
.headcta{grid-area:cta;display:flex;align-items:center;justify-self:end}
.book-short{display:none}
#site-header a.book,#site-header a.book:visited{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;background:var(--gold);color:#1a1814;font-weight:700;text-decoration:none;border:2px solid var(--gold);border-radius:8px;padding:var(--s12) var(--s16);line-height:1.2;text-align:center}
#site-header a.book:hover{background:#ffe8a3;color:#1a1814}
.search-toggle{grid-area:searchbtn;display:none;align-items:center;justify-content:center;gap:var(--s12);min-height:44px;min-width:44px;padding:var(--s12) var(--s16);font:inherit;font-size:1rem;font-weight:700;line-height:1.2;color:#fff;background:transparent;border:2px solid rgba(255,255,255,.85);border-radius:8px;cursor:pointer;position:relative}
.search-icon{width:1.15rem;height:1.15rem;display:block;flex:none}
.search-wrap{grid-area:search;position:relative}
.sitesearch{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s12)}
.sitesearch label{flex:1 1 100%;color:#fff;font-weight:700}
.sitesearch input[type="search"]{flex:1 1 12rem;min-width:0;min-height:44px;font:inherit;color:var(--ink);background:#fff;border:2px solid #fff;border-radius:8px;padding:var(--s12) var(--s16)}
.sitesearch button{min-height:44px;min-width:44px;padding:var(--s12) var(--s16);font:inherit;font-weight:700;color:#1a1814;background:var(--gold);border:2px solid var(--gold);border-radius:8px;cursor:pointer}
.search-results{position:absolute;z-index:35;left:0;right:0;top:100%;margin-top:var(--s12);background:#fff;color:var(--ink);border:2px solid var(--ink);border-radius:8px;max-height:70vh;overflow:auto}
.search-results ul{list-style:none;margin:0;padding:0}
#site-header .search-results a,#site-header .search-results a:visited,#site-header .search-empty a,#site-header .search-empty a:visited{display:flex;flex-direction:column;gap:8px;min-height:44px;justify-content:center;padding:var(--s12) var(--s16);color:var(--link);text-decoration:underline;text-underline-offset:.12em;background:#fff}
#site-header .search-results a span{color:var(--ink);font-weight:400;text-decoration:none}
.search-empty{margin:0;padding:var(--s12);color:var(--ink)}
nav.top{grid-area:nav;display:flex;flex-wrap:nowrap;align-items:stretch;gap:var(--s12);margin:0;padding-top:var(--s12);border-top:1px solid rgba(255,255,255,.28);overflow-x:auto;scroll-snap-type:x proximity;scrollbar-width:thin}
.grp{position:relative;flex:0 0 auto}
.grp>summary{display:flex;align-items:center;justify-content:space-between;gap:var(--s12);min-height:44px;padding:var(--s12) var(--s16);color:#fff;font-weight:700;cursor:pointer;list-style:none;white-space:nowrap;border:1px solid rgba(255,255,255,.8);border-radius:999px;background:rgba(0,0,0,.18);scroll-snap-align:start}
.grp>summary::-webkit-details-marker{display:none}
.grp>summary::marker{content:""}
.grp>summary::after{content:"";border:solid #fff;border-width:0 2px 2px 0;width:.45rem;height:.45rem;transform:rotate(45deg);flex:none;margin-top:-.15rem}
.grp[open]>summary::after{transform:rotate(-135deg);margin-top:.2rem}
.grp.has-current>summary{box-shadow:inset 0 -3px 0 var(--gold);background:rgba(255,255,255,.16)}
.glinks{display:flex;flex-direction:column;min-width:16rem}
.glinks a{display:flex;align-items:center;min-height:44px;padding:var(--s12) var(--s16);color:#fff;text-decoration:underline;text-underline-offset:.15em}
.glinks a.is-current{font-weight:700;background:rgba(255,255,255,.16);border-radius:8px}
@media(max-width:1099px){
.grp[open] .glinks{position:fixed;z-index:46;top:var(--header-bottom);left:0;right:0;max-width:none;background:#10244F;border:2px solid #fff;border-radius:0 0 12px 12px;padding:var(--s12);box-shadow:0 12px 24px rgba(0,0,0,.35);max-height:min(60vh,24rem);overflow:auto}
}
@media(min-width:720px){
#site-header .shell{grid-template-columns:minmax(0,1fr) auto auto;grid-template-areas:"brand links cta" "sub sub sub" "search search search" "nav nav nav"}
.sitesearch{flex-wrap:nowrap}
.sitesearch label{flex:0 0 auto}
}
@media(min-width:1100px){
#site-header .shell{grid-template-areas:"brand links cta" "sub sub sub" "search search search" "nav nav nav"}
nav.top{overflow:visible;scroll-snap-type:none;justify-content:flex-start;gap:8px;padding-top:var(--s16)}
.grp>summary{border-radius:8px;background:transparent;font-size:1rem;padding:8px var(--s12)}
.grp[open] .glinks{position:absolute;z-index:34;top:100%;left:0;right:auto;background:#10244F;border:2px solid #fff;border-radius:8px;padding:var(--s12);box-shadow:0 8px 24px rgba(0,0,0,.28);max-height:min(70vh,28rem);overflow:auto}
.grp:nth-last-child(-n+2)[open] .glinks{left:auto;right:0}
}
.nav-fade,.nav-hint{display:none}
.nav-hint::before{content:"";display:block;width:.5rem;height:.5rem;border:solid var(--gold);border-width:0 3px 3px 0;transform:rotate(-45deg)}
body.is-docked #site-header{position:fixed;top:0;left:0;right:0;height:var(--header-compact);z-index:40;box-shadow:0 2px 12px rgba(0,0,0,.28);overflow:visible}
body.is-docked #site-header .shell{height:100%;padding:var(--s12) var(--s16);row-gap:var(--s12);grid-template-columns:minmax(0,1fr) auto auto;grid-template-rows:44px 40px 44px;grid-template-areas:"brand searchbtn cta" "sub sub sub" "nav nav nav";align-items:center}
body.is-docked .brand{min-height:44px;min-width:0}
body.is-docked .name-main,body.is-docked .headlink{display:none}
body.is-docked .name-compact{display:block;font-size:1rem;line-height:1.2;font-weight:700;white-space:nowrap}
body.is-docked .name-sub{font-size:.9375rem;line-height:1.3}
body.is-docked .headcta{margin:0}
body.is-docked a.book{min-height:44px;padding:8px var(--s12)}
body.is-docked .book-long{display:none}
body.is-docked .book-short{display:inline}
body.is-docked .search-toggle{display:inline-flex}
body.is-docked .search-wrap{display:none;margin:0;position:absolute;top:100%;left:0;right:0;z-index:36;background-color:var(--head-1);background-image:var(--head-bg);padding:var(--s16) 0 var(--s24);box-shadow:0 12px 24px rgba(0,0,0,.28)}
body.is-docked .search-wrap.is-open{display:block}
body.is-docked nav.top{display:flex;margin:0;padding:0;border:0;background:transparent;flex-direction:row;flex-wrap:nowrap;align-items:center;gap:8px;min-width:0;overflow-x:auto}
body.is-docked .grp>summary{min-height:44px;padding:8px var(--s12)}
body.is-docked .grp.has-current>summary{background:rgba(255,255,255,.16);box-shadow:inset 0 -3px 0 var(--gold)}
body.is-docked.nav-more-right .nav-fade-right,body.is-docked.nav-more-left .nav-fade-left{display:block;position:absolute;bottom:var(--s12);height:44px;width:var(--s32);pointer-events:none;z-index:4}
body.is-docked.nav-more-right .nav-fade-right{right:0;background:linear-gradient(90deg,rgba(16,36,79,0),#10244F 72%)}
body.is-docked.nav-more-left .nav-fade-left{left:0;background:linear-gradient(90deg,#014233 28%,rgba(1,66,51,0))}
body.is-docked.nav-more-right .nav-hint{display:flex;align-items:center;justify-content:flex-end;position:absolute;right:8px;bottom:var(--s12);width:var(--s24);height:44px;pointer-events:none;z-index:5}
@media(min-width:900px){
body.is-docked #site-header .shell{grid-template-columns:auto minmax(0,1fr) auto auto;grid-template-rows:44px 44px;grid-template-areas:"brand sub searchbtn cta" "nav nav nav nav";padding-top:var(--s12);padding-bottom:var(--s12)}
body.is-docked .name-sub{align-self:center}
}
@media(max-width:719px){
body.is-docked .search-toggle{padding:0;width:44px}
body.is-docked .search-toggle-text{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
body.is-docked .flag{height:16px}
}
@media(min-width:1100px){
body.is-docked nav.top{overflow:visible}
body.is-docked .grp>summary{border-radius:8px}
}
.notice{background:#fff6db;color:var(--ink);border-bottom:3px solid #8a5a00}
.notice .shell{padding-top:var(--s16);padding-bottom:var(--s16)}
.notice p{margin:0 0 var(--s12);max-width:66ch}
.notice p:last-child{margin-bottom:0}
main{min-width:0}
main>.shell{padding-top:var(--s24);padding-bottom:var(--s40)}
main:focus{outline:none}
main:focus-visible{outline:3px solid var(--ink);outline-offset:-3px}
.crumbs ol{display:flex;flex-wrap:wrap;list-style:none;padding:0;margin:0 0 var(--s12);gap:0}
.crumbs li{display:flex;align-items:center;min-height:44px}
.crumbs li+li::before{content:"/";margin:0 var(--s12);color:#3e3a34}
.crumbs a{display:inline-flex;align-items:center;min-height:44px}
.meta{display:flex;flex-wrap:wrap;gap:var(--s12);align-items:center;margin:0 0 var(--s24)}
.checked{display:inline-flex;align-items:center;min-height:44px;background:#e5f2ea;color:#143024;border:1px solid #1d4f3e;border-radius:8px;padding:var(--s12) var(--s16);font-size:1rem}
article.content{min-width:0}
.head-block{margin:0}
.head-block p{margin:0 0 var(--s16)}
h1,h2,h3{line-height:1.25}
h1{font-size:clamp(1.85rem,1.2rem + 2vw,2.5rem);margin:0 0 var(--s16)}
h2{font-size:1.5rem;margin:var(--s40) 0 var(--s16)}
h3{font-size:1.25rem;margin:var(--s24) 0 var(--s12)}
.content p{max-width:66ch}
.inshort{background:#eef4f1;border-left:6px solid #1d4f3e;border-radius:12px;padding:var(--s16) var(--s24);margin:0 0 var(--s24)}
.inshort p{margin:0;max-width:66ch}
.layout{display:flex;flex-direction:column;gap:var(--s24);min-width:0;margin-top:var(--s24)}
.toc{order:-1}
.rest{order:0;min-width:0}
.rest>h2:first-child,.rest>h3:first-child{margin-top:0}
@media(min-width:960px){
.layout.has-toc{display:grid;grid-template-columns:minmax(0,1fr) 18rem;column-gap:var(--s32);align-items:start}
.layout.has-toc .rest{grid-column:1;grid-row:1;order:0}
.layout.has-toc .toc{grid-column:2;grid-row:1;order:0;position:sticky;top:var(--scroll-pad);max-height:calc(100vh - var(--scroll-pad) - var(--s16));overflow:auto}
}
.toc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:var(--s12) var(--s24) var(--s16);margin:0}
.toc summary{min-height:44px;display:flex;align-items:center;font-weight:700;cursor:pointer}
.toc ul{list-style:none;margin:0;padding:0 0 var(--s12)}
.toc a{display:flex;align-items:center;min-height:44px;padding:8px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:var(--s24);margin:0 0 var(--s16)}
h2+.card,h3+.card{margin-top:0}
.card>:first-child{margin-top:0}
.card>:last-child{margin-bottom:0}
.card p{margin:0 0 var(--s16)}
.card ul,.card ol{margin:var(--s12) 0 0;padding-left:1.25rem}
.card li+li{margin-top:var(--s12)}
.warn{border-left:6px solid #9b2c2c;background:#fdeeee}
.note{border-left:6px solid #8a5a00;background:#fff8ec}
.conf{border-left:6px solid #5c3d78;background:#f6f1fa}
.wrap{overflow-x:auto;max-width:100%;margin:var(--s16) 0}
table{border-collapse:collapse;width:100%;background:#fff;font-size:1rem}
th,td{border:1px solid var(--line);padding:var(--s12) var(--s16);text-align:left;vertical-align:top}
th{background:#e7efe9;color:var(--ink)}
.src{color:#3e3a34;font-size:1rem}
.src,.card,td,th{overflow-wrap:anywhere}
.tag{display:inline-block;font-size:.875rem;padding:0 var(--s12);border-radius:4px;background:#eee;margin-right:8px}
.tag.ok{background:#d8f0de}
.tag.no{background:#f8d7d7}
.tag.mix{background:#fdebc8}
.content ul,.content ol{margin:var(--s12) 0 var(--s16);padding-left:1.25rem}
.content li+li{margin-top:var(--s12)}
.content li{max-width:66ch}
.tasks,.link-grid,.readnext ul,.index-list{list-style:none;padding:0;margin:var(--s16) 0 0;display:grid;gap:var(--s16);grid-template-columns:1fr}
.tasks li,.link-grid li,.index-list li,.readnext li,.toc li,.crumbs li,.pn{max-width:none}
@media(min-width:720px){.tasks,.link-grid,.readnext ul,.index-list{grid-template-columns:1fr 1fr}}
.topic{margin:0 0 var(--s32)}
.topic>h3{margin-top:0}
.jump{display:flex;flex-direction:column;justify-content:center;gap:8px;min-height:44px;padding:var(--s16) var(--s24);background:#fff;color:var(--ink);border:1px solid var(--line);border-radius:12px;text-decoration:none}
.jump:hover{border-color:var(--link)}
.jump .lt{color:var(--link);font-weight:700;text-decoration:underline;text-underline-offset:.12em}
.jump .ls{color:var(--ink);font-weight:400;text-decoration:none}
a.jump:visited .lt{color:var(--visited)}
.pn{display:grid;gap:var(--s16);margin-top:var(--s40);max-width:none}
.pn a{display:flex;flex-direction:column;justify-content:center;gap:8px;min-height:44px;padding:var(--s16) var(--s24);background:#fff;border:1px solid var(--line);border-radius:12px;text-decoration:none}
.pn .pn-k{color:#3e3a34;font-size:1rem;font-weight:700}
.pn .pn-t{color:var(--link);font-weight:700;text-decoration:underline;text-underline-offset:.12em}
.pn a:visited .pn-t{color:var(--visited)}
@media(min-width:720px){.pn:has(a.prev):has(a.next){grid-template-columns:1fr 1fr}.pn a.next{align-items:flex-end;text-align:right}}
.readnext{margin-top:var(--s40)}
.readnext h2{margin-top:0}
.index-status{font-weight:700;margin:0 0 var(--s16)}
a{color:var(--link)}
a:visited{color:var(--visited)}
.content a,.crumbs a,footer a,.notice a,.search-empty a{text-decoration:underline;text-underline-offset:.12em}
footer{border-top:1px solid var(--line);color:var(--ink);margin-top:var(--s32)}
footer .shell{padding-top:var(--s32);padding-bottom:var(--s40)}
footer p{max-width:66ch}
.footnav{display:flex;flex-wrap:wrap;gap:var(--s12) var(--s24);margin:0 0 var(--s16)}
.footnav a{display:inline-flex;align-items:center;min-height:44px;font-weight:700}
:focus{outline:3px solid var(--ink);outline-offset:2px}
:focus:not(:focus-visible){outline:none}
:focus-visible{outline:3px solid var(--ink);outline-offset:2px}
#site-header a:focus-visible,#site-header button:focus-visible,#site-header input:focus-visible,#site-header summary:focus-visible{outline-color:var(--gold);outline-offset:2px}
#site-header a.book:focus-visible,#site-header .sitesearch button:focus-visible{outline-color:#fff}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media(forced-colors:active){
.card,.inshort,.notice,.jump,.toc,.pn a,a.book,.search-toggle,.grp>summary{border:1px solid CanvasText}
a.book{background:ButtonFace;color:ButtonText}
}
'''
