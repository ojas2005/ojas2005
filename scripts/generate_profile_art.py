"""Render a supplied portrait as ASCII and rasterize original terminal animations.
Usage: python scripts/generate_profile_art.py /path/to/Subject.png
Requires Pillow. The source photograph is intentionally not stored in the repository.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse, html
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
BG = '#10141d'; PANEL = '#181e2b'; INK = '#dbe4f3'; MUTED = '#9aa8c0'
BLUE = '#7aa2f7'; GREEN = '#9ece6a'; PEACH = '#ffb98b'; PURPLE = '#bb9af7'
FONT_PATH = '/System/Library/Fonts/Menlo.ttc'
@lru_cache(maxsize=12)
def font(size): return ImageFont.truetype(FONT_PATH, size)
def text(d,xy,s,size=18,fill=INK): d.text(xy,s,font=font(size),fill=fill)
def frame(w,h,title):
 im=Image.new('RGB',(w,h),BG); d=ImageDraw.Draw(im)
 d.rounded_rectangle((1,1,w-2,h-2),18,fill=BG,outline='#344059',width=2)
 d.line((1,47,w-2,47),fill='#344059',width=1)
 for x,c in [(22,'#f7768e'),(43,'#e0af68'),(64,'#9ece6a')]: d.ellipse((x,18,x+10,28),fill=c)
 text(d,(94,15),title,14,MUTED)
 return im,d

def save_gif(frames,name,durations):
 # Fixed shared palette prevents colour shimmer. Finite animation avoids constant motion.
 palette=frames[0].quantize(colors=128)
 indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
 indexed[0].save(OUT/name,save_all=True,append_images=indexed[1:],duration=durations,loop=1,optimize=True,disposal=2)

def portrait(source):
 im=Image.open(source).convert('RGBA')
 # Relative crop keeps face, hair, glasses and shoulders; no face synthesis.
 w,h=im.size; im=im.crop((int(w*.23),0,w,int(h*.83)))
 cols,rows=84,52
 pixels=im.resize((cols,rows),Image.Resampling.LANCZOS)
 chars=[]; colors=[]; ramp=' .,:;irsXA253hMHGS#9B&@'
 for y in range(rows):
  row=[]; col=[]
  for x in range(cols):
   r,g,b,a=pixels.getpixel((x,y)); lum=(.2126*r+.7152*g+.0722*b)/255
   if a<45: row.append(' ');col.append((0,0,0));continue
   v=lum**.64
   row.append(ramp[max(1,min(len(ramp)-1,round(v*(len(ramp)-1))))])
   # Lift dark photographic pixels so hair remains visible against the terminal.
   col.append(tuple(min(255,int(channel*.73+75)) for channel in (r,g,b)))
  chars.append(''.join(row));colors.append(col)
 (OUT/'ojas-portrait.txt').write_text('\n'.join(chars)+'\n')
 frames=[]; cw,ch=5.8,9; x0,y0=577,65
 for i in range(24):
  canvas,d=frame(1100,580,'ojas@github:~ / whoami')
  text(d,(36,84),'HELLO, INTERNET.',16,BLUE)
  text(d,(34,120),'Ojas Tiwari',42)
  text(d,(36,185),'Analyst @ Capgemini',20,PEACH)
  text(d,(36,222),'Full-Stack .NET Developer',19)
  text(d,(36,256),'Microservices / Cloud / Agentic AI',16,MUTED)
  text(d,(36,318),'$ dotnet run --project life',17,GREEN)
  for j,line in enumerate(['[OK] curiosity initialized','[OK] coffee dependency resolved','[??] work-life balance: compiling']):
   if i>=j*2: text(d,(36,355+j*31),line,16,MUTED if j<2 else PEACH)
  text(d,(36,494),'I turn coffee into distributed problems.',14,PURPLE)
  text(d,(36,521),'Then I give them health checks.',14,PURPLE)
  for y,row in enumerate(chars):
   for x,c in enumerate(row):
    if c==' ':continue
    color=colors[y][x]
    if i<18 and abs(y-(i/17)*rows)<2: color=(170,225,237)
    d.text((x0+x*cw,y0+y*ch),c,font=font(9),fill=color)
  if i%6<3 and i<20: text(d,(442,419),'_',16,PEACH)
  text(d,(788,551),'PHOTO -> ASCII // HUMAN, MOSTLY',10,MUTED)
  frames.append(canvas)
 save_gif(frames,'ojas-terminal.gif',[160]*23+[3000])
 frames[-1].save(OUT/'ojas-terminal-static.png',optimize=True)
 # Text-native, accessible static alternative.
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="520" height="510" viewBox="0 0 520 510" role="img" aria-label="ASCII portrait of Ojas Tiwari from the supplied photo"><title>Ojas Tiwari — ASCII portrait</title><rect width="520" height="510" fill="#10141d"/>']
 for y,row in enumerate(chars):
  for x,c in enumerate(row):
   if c!=' ': svg.append(f'<text x="{16+x*cw:.1f}" y="{18+y*ch:.1f}" font-family="monospace" font-size="9" fill="rgb{colors[y][x]}">{html.escape(c)}</text>')
 svg.append('</svg>');(OUT/'ojas-portrait-static.svg').write_text('\n'.join(svg))

def jokes():
 frames=[]
 for i in range(24):
  im,d=frame(660,230,'deployment.log // a documentary')
  text(d,(25,68),'LOCAL',15,GREEN);text(d,(365,68),'PRODUCTION',15,PEACH)
  text(d,(24,101),'(•_•)  all tests passed',15,INK)
  stage=min(i//6,3)
  lines=['ship it.','works on my machine.','which machine?','the one in my heart.']
  text(d,(25,162),'> '+lines[stage],17,PURPLE)
  face=['(o_o)','(O_O)','(x_x)','(o_o)'][stage]
  text(d,(375,102),face+'  '+['...','hmm','404','retry'][stage],18,PEACH)
  d.line((330,64,330,142),fill='#344059')
  frames.append(im)
 save_gif(frames,'works-on-my-machine.gif',[180]*23+[2000])
 frames=[]
 for i in range(24):
  im,d=frame(660,230,'rubber-duck debugger // senior consultant')
  stage=min(i//6,3)
  duck=['   __','<(o )___',' ( ._> /','  `---\'']
  for j,line in enumerate(duck):text(d,(26,66+j*26),line,22,PEACH)
  lines=[['Have you checked','the logs?'],['Have you checked','the OTHER logs?'],['Have you tried','reading the error?'],['That will be','one bread, please.']][stage]
  for j,line in enumerate(lines): text(d,(225,93+j*33),line,20,INK)
  text(d,(225,176),'0 tokens used. devastating accuracy.',13,GREEN)
  frames.append(im)
 save_gif(frames,'duck-debugger.gif',[180]*23+[2000])

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('photo',type=Path);p.add_argument('--font',default=FONT_PATH);a=p.parse_args();FONT_PATH=a.font;OUT.mkdir(exist_ok=True);portrait(a.photo);jokes()
