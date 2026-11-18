import json,subprocess,re
sc=json.load(open('scenes.json'));total=sc[-1]['start']+sc[-1]['dur']
inp=[];flt=[];labels=[];n=len(sc)
for i,s in enumerate(sc):
    d=int((s['start']+(0.25 if i==0 else 0.1))*1000)
    inp+=['-i',f'voice/{i+1}.wav'];flt.append(f'[{i}:a]aresample=44100,volume=1.6,adelay={d}|{d}[v{i}]');labels.append(f'[v{i}]')
a=sc[2]['start'];b=sc[7]['start']
for k in range(6):
    d=int((a+(b-a)*k/5)*1000)
    inp+=['-f','lavfi','-i','sine=frequency=1800:duration=0.05']
    flt.append(f'[{n+k}:a]volume=0.35,aresample=44100,adelay={d}|{d}[t{k}]');labels.append(f'[t{k}]')
inp+=['-f','lavfi','-i',f'anoisesrc=color=brown:duration={total}:amplitude=0.04']
flt.append(f'[{n+6}:a]lowpass=f=300,aresample=44100[amb]');labels.append('[amb]')
flt.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{total},alimiter=limit=0.95[out]')
fc=re.sub(r'\[(\d+):a\]',lambda m:f'[{int(m.group(1))+1}:a]',';'.join(flt))
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','24','-i','frames/%05d.png']+inp+['-filter_complex',fc,'-map','0:v','-map','[out]','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-c:a','aac','-b:a','160k','-movflags','+faststart','masatsu.mp4'],check=True)
