import base64,re,os,shutil,zipfile,json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src=open('src/quests.html').read()
A={'FONT_R':'ds/Factor_A-Regular.ttf','FONT_B':'ds/Factor_A-Bold.ttf','EGG':'ds/egg.png','DINO_FALLBACK':'crops/dino.jpg'}
for k in ['math','russian','english','nature','programming']: A['S_'+k.upper()]='ds/s_%s.png'%k
for k in ['fox','chess','banner','chest100','bolt_big','bolt_sm','dino_hi','dino_girl','target','tab_home','tab_chat','tab_target','tab_trophy','tab_me']: A['Q_'+k.upper()]='q/%s.png'%k
MIME={'.jpg':'image/jpeg','.png':'image/png','.ttf':'font/ttf'}
s=src
for k,p in A.items(): s=s.replace('__%s__'%k,'data:%s;base64,'%MIME[os.path.splitext(p)[1]]+base64.b64encode(open(p,'rb').read()).decode())
s=s.replace('__THREE__','https://cdnjs.cloudflare.com/ajax/libs/three.js/0.149.0/three.min.js')
VO={f[:-4]:'data:audio/mpeg;base64,'+base64.b64encode(open('vo/final/'+f,'rb').read()).decode() for f in sorted(os.listdir('vo/final'))}
s=s.replace('__VOICE_MAP__',json.dumps(VO))
left=re.findall(r'__[A-Z0-9_]+__',s); assert not left,left
open('zavr-quests.html','w').write(s)
# local
root='localq'; out=root+'/zavr-quests'; shutil.rmtree(root,ignore_errors=True); os.makedirs(out+'/assets'); os.makedirs(out+'/voice')
s=src
for k,p in A.items():
    n=os.path.basename(p); shutil.copy(p,out+'/assets/'+n); s=s.replace('__%s__'%k,'assets/'+n)
shutil.copy('ds/three149.min.js',out+'/assets/three.min.js'); s=s.replace('__THREE__','assets/three.min.js')
s=s.replace('__VOICE_MAP__','null')
for f in os.listdir('vo/final'): shutil.copy('vo/final/'+f,out+'/voice/'+f)
e=s.index('</style>')+8
s='<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'+s[:e]+'\n</head>\n<body>\n'+s[e:]+'\n</body>\n</html>\n'
open(out+'/index.html','w').write(s)
# voice lines from the page source
lines=re.search(r'const LINES=\{(.*?)\};',src,re.S).group(1)
pairs=re.findall(r"(\w+):'((?:[^'\\]|\\.)*)'",lines)
EMO={'greet':'бодро, хвастливо','tap1':'возмущённо','tap2':'насмешливо','tap3':'жадно, прижимая сундук','tap4':'нетерпеливо',
 'quest_hit':'вскрик боли','quest_hit2':'задумчиво, с опаской','quest_hit3':'сердито','all_done':'ослабленно, но упрямо',
 'duel_start':'азартно','hit1':'короткий вскрик','hit2':'выдох от удара','hit3':'нехотя признаёт','hit4':'причитает',
 'miss1':'злорадно','miss2':'злорадно, замахиваясь','miss3':'смеётся','timeout':'дразнит','combo':'в шоке',
 'phase2':'злится','phase3':'в ярости, рычит','win':'проигравший, обиженно','lose':'победно смеётся','dizzy':'кружится, растерянно','tickle':'хихикает','hat':'возмущённо','tail':'вскрикивает','count':'довольно, хитро','key':'хвастливо','angry':'рычит','heal':'чавкая, довольно','shield':'злорадно','sneaky':'шёпотом, хитро','quest_watch':'подозрительно','fast':'удивлённо','parrot1':'попугай, пронзительно','parrot2':'попугай, дразнит','parrot3':'попугай, подсказывает','flee':'насмешливо вслед','chest':'сердито, захлопывая сундук','chest_lost':'горестно, в отчаянии'}
with open(out+'/voice/voice-lines.csv','w',encoding='utf-8') as f:
    f.write('file;text;emotion\n')
    for k,v in pairs: f.write(f'{k}.mp3;{v};{EMO.get(k,"")}\n')
shutil.copy('README.quests.md',out+'/README.md')
z=zipfile.ZipFile('zavr-quests.zip','w',zipfile.ZIP_DEFLATED)
for r,_,fs in os.walk(root):
    for fn in fs: fp=os.path.join(r,fn); z.write(fp,os.path.relpath(fp,root))
z.close(); print('ok',os.path.getsize('zavr-quests.html')//1024,'KB html,',os.path.getsize('zavr-quests.zip')//1024,'KB zip,',len(pairs),'lines')
