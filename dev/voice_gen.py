import csv,subprocess,os,sys
src=sys.argv[1]; raw='vo/raw'; out='vo/final'
os.makedirs(raw,exist_ok=True); os.makedirs(out,exist_ok=True)
FAST={'chest','chest_lost','tap1','miss1','miss2','timeout','combo','phase2','phase3','hit1','hit2','hit4','quest_hit'}
SLOW={'quest_hit2','all_done','win','hit3'}
rows=list(csv.reader(open(src,encoding='utf-8'),delimiter=';'))[1:]
for f,text,emo in rows:
    i=f[:-4]; r='+30%' if i in FAST else '+8%' if i in SLOW else '+20%'
    rp=f'{raw}/{f}'
    if not os.path.exists(rp) or os.path.getsize(rp)==0:
        import time
        parrot=i.startswith('parrot')
        for att in range(6):
            if subprocess.run(['timeout','60','python3','votool/tts.py',text,rp,'ru-RU-SvetlanaNeural' if parrot else 'ru-RU-DmitryNeural','+25Hz' if parrot else '-10Hz','+25%' if parrot else r],capture_output=True).returncode==0 and os.path.getsize(rp)>0: break
            time.sleep(3+att*3)
        else: raise SystemExit('failed '+i)
    k=1.3 if i.startswith('parrot') else 0.84
    SPEED=1.2
    af=(f"asetrate=24000*{k},aresample=44100,atempo={min(2,SPEED/k):.4f},"
        "highpass=f=70,equalizer=f=140:t=q:w=1:g=5,equalizer=f=2600:t=q:w=1.5:g=3,lowpass=f=9000,"
        "aeval='tanh(1.8*val(0))/tanh(1.8)':c=same,"
        "aecho=0.8:0.5:35|70:0.18|0.08,"
        "acompressor=threshold=-18dB:ratio=3:attack=5:release=80,loudnorm=I=-16:TP=-1.5")
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',rp,'-af',af,'-ac','1','-b:a','64k',f'{out}/{f}'],check=True)
    print(i, os.path.getsize(f'{out}/{f}'))
