from multiprocessing.spawn import _main
from instagrapi import Client
import time
import json
import os
import shutil

from m3u8 import MediaList


def apagarMediaTemp():
    for arquivoNome in os.listdir('media_temp'):
        arquivoPath = os.path.join('media_temp', arquivoNome)
        try:
            if os.path.isfile(arquivoPath) or os.path.islink(arquivoPath):
                os.unlink(arquivoPath)
            elif os.path.isdir(arquivoPath):
                shutil.rmtree(arquivoPath)
        except Exception as e:
            print('[X] Erro ao deletar %s.\nErro: %s' % (arquivoPath, e))


def cadastrarPostagem(media_pk):
    listaPostagens = json.loads(open('posts.json', 'r').read())
    listaPostagens.append(media_pk)
    salvarLista = open('posts.json', 'w').write(json.dumps(listaPostagens))


def verificarPostagem(media_pk):
    listaPostagens = json.loads(open('posts.json', 'r').read())
    if media_pk in listaPostagens:
        return True
    else:
        return False


def identificarTipoMidia(objMedia):
    # Verificar o tipo de media (foto, carrosel, vídeo etc)
    if objPostagem.media_type == 1:
        # Foto
        mediaTipo = 'foto'
    elif objPostagem.media_type == 2:
        if objPostagem.product_type == 'feed':
            # Vídeo no feed
            mediaTipo = 'video'
        elif objPostagem.product_type == 'igtv':
            # Vídeo IGTV
            mediaTipo = 'igtv'
        elif objPostagem.product_type == 'clips':
            # Vídeo Reels
            mediaTipo = 'reels'
    elif objPostagem.media_type == 8:
        # Carrossel
        mediaTipo = 'carrossel'
    return mediaTipo


def salvarMedia(cl: Client, mediaTipo, media_pk):
    # Verificar o tipo de media (foto, carrosel, vídeo etc)
    if mediaTipo == 'foto':
        mediaPath = cl.photo_download(media_pk, 'media_temp')
    elif mediaTipo == 'video':
        mediaPath = cl.video_download(media_pk, 'media_temp')
    elif mediaTipo == 'igtv':
        mediaPath = cl.igtv_download(media_pk, 'media_temp')
    elif mediaTipo == 'reels':
        mediaPath = cl.clip_download(media_pk, 'media_temp')
    elif mediaTipo == 'carrossel':
        mediaPath = cl.album_download(media_pk, 'media_temp')
    return mediaPath


def postarMedia(cl: Client, mediaTipo, mediaPath, mediaLegenda):
    # Verificar o tipo de media (foto, carrosel, vídeo etc)
    try:
        if mediaTipo == 'foto':
            mediaPostada = cl.photo_upload(
                path=mediaPath, caption=mediaLegenda)
        elif mediaTipo == 'video':
            mediaPostada = cl.video_upload(
                path=mediaPath, caption=mediaLegenda)
        elif mediaTipo == 'igtv':
            mediaPostada = cl.igtv_upload(path=mediaPath, caption=mediaLegenda)
        elif mediaTipo == 'reels':
            mediaPostada = cl.clip_upload(path=mediaPath, caption=mediaLegenda)
        elif mediaTipo == 'carrossel':
            mediaPostada = cl.album_upload(
                paths=mediaPath, caption=mediaLegenda)
        return mediaPostada
    except Exception as e:
        # Se dá erro no vídeo é porque é reels
        if mediaTipo == 'video':
            try:
                mediaPostada = cl.clip_upload(
                    path=mediaPath, caption=mediaLegenda)
                return mediaPostada
            except Exception as e:
                print(mediaTipo, e)
        else:
            print(mediaTipo, e)
        pass


if __name__ == '__main__':
    # API https://github.com/adw0rd/instagrapi
    # API https://adw0rd.github.io/instagrapi/usage-guide/interactions.html
    # Entrar na conta do Instagram
    cl = Client()
    cl.login('seu usuário no instagram', 'sua senha')

    print('Entrando no Instagram...')

    # Listagem de perfis para procurar fofocas
    # usuário: id do usuário
    # usuariosFofoca = {'nome usuario': id usuario}
    # Pegue o ID aqui: https://commentpicker.com/instagram-user-id.php
    usuariosFofoca = {
        'alfinetei': 975864059
    }

    print('Perfis cadastrados: ' + str(len(usuariosFofoca)))

    # Procurar novas publicações nos perfis indicados para fazer a postagem a cada 30 minutos
    while True:

        print('Timer zerado, procurando novas postagens...')

        # Percorrer todos perfis de fofocas
        for usuarioNome, usuarioId in usuariosFofoca.items():

            print('Procurando no perfil @' + usuarioNome)

            # Pegar a última postagem desse usuário
            # Retorna a última postagem como objeto Media https://adw0rd.github.io/instagrapi/usage-guide/media.html
            objPostagem = cl.user_medias(usuarioId, 1)

            # Verificar se tem postagem
            if len(objPostagem) <= 0:
                print('Perfil sem nenhuma postagem, próximo...')
                continue
            else:
                objPostagem = objPostagem[0]

            # Verificar se já não foi postado pelo media_pk
            if verificarPostagem(objPostagem.pk):
                print('Postagem já repostada... procurando no próximo perfil...')
                continue

            # Identificar o tipo de media
            mediaTipo = identificarTipoMidia(objPostagem)

            print('Tipo de mídia identificada: ' + mediaTipo)

            # # Se for vídeo pular porque está dando erro no upload
            # if mediaTipo == 'video':
            #     print('Postagem é um vídeo, procurando próximo perfil...')
            #     continue

            # Salvar a postagem
            mediaPath = salvarMedia(cl, mediaTipo, objPostagem.pk)

            print('Salvando a mídia...')

            # Criar legenda
            mediaLegenda = '''Créditos: @{} • {}'''.format(
                usuarioNome, objPostagem.caption_text)

            print('Legenda criada...')

            # Realizar a postagem no Instagram dando créditos ao criador
            mediaPostada = postarMedia(cl, mediaTipo, mediaPath, mediaLegenda)

            print('Postagem realizada com sucesso...')

            # Cadastrar postagem para não repetir
            cadastrarPostagem(objPostagem.pk)

            print('Postagem cadastrada no banco de dados...')

            # Apagar pasta temporária de mídias
            apagarMediaTemp()

            print('Pasta temporária apagada...')

            # Esperar 5 segundos para procurar no próximo perfil
            print('Esperando 5 segundos...')
            time.sleep(5)

        print('Procura finalizada, esperando tempo determinado...')

        time.sleep(60*10)
