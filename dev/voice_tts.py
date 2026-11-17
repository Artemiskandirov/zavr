import sys,os,asyncio,certifi
certifi.where=lambda:'/root/.ccr/ca-bundle.crt'
import edge_tts
async def main(text,out,voice='ru-RU-DmitryNeural',pitch='-12Hz',rate='+5%'):
    c=edge_tts.Communicate(text,voice,pitch=pitch,rate=rate,proxy=os.environ.get('HTTPS_PROXY'))
    await c.save(out)
asyncio.run(main(*sys.argv[1:]))
