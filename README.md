<div align="center">
  <h3>Instagram Bot for Repost</h3>
  <img src="https://img.shields.io/github/issues/MatheusGatti/Instagram-Bot-for-Repost"/>
  <img src="https://img.shields.io/github/forks/MatheusGatti/Instagram-Bot-for-Repost"/>
  <img src="https://img.shields.io/github/stars/MatheusGatti/Instagram-Bot-for-Repost?color=yellow"/>
  <img src="https://img.shields.io/github/license/MatheusGatti/Instagram-Bot-for-Repost"/>
  <p><small>Este é um robô desenvolvido em Python que acompanha 24h/dia alguns perfis do Instagram que será selecionado por você para detectar novas postagens como imagens, vídeos e reels e repostar em um único Instagram seu.</small></p>
</div>

<hr>

### Tecnologias utilizadas
* Python

<br>

### Bibliotecas utilizadas e necessárias para o funcionamento do robô
* [instagrapi](https://github.com/adw0rd/instagrapi)
* m3u8

<br>

### Configurações
- Na **linha 109** você poderá inserir o seu usuário e senha do Instagram que deseja realizar as repostagens.
~~~python
cl.login('seu usuário no instagram', 'sua senha')
~~~


- Na **linha 117** você poderá inserir os perfis que deseja acompanhar/monitorar.
~~~python
# usuariosFofoca = {'nome usuario': id usuario}
# Pegue o ID aqui: https://commentpicker.com/instagram-user-id.php
usuariosFofoca = {
    'alfinetei': 975864059
}
~~~


- [Se deseja implementar mais alguma coisa no código utilize as referências da API](https://adw0rd.github.io/instagrapi/usage-guide/interactions.html)
- [Para pegar o ID de um usuário do Instagram](https://commentpicker.com/instagram-user-id.php)


#### Configuração feita? É só iniciar o robô.

<hr>

### Como funciona?
#### O robô analisa perfil por perfil a cada 10 minutos detectando se há uma nova postagem e também verifica se ela já foi repostada por você.
#### Obs: o arquivo posts.json salva o ID das postagens que já foram repostadas para realizar 2 verificações: se há uma nova postagem e se ela já foi postada por você.
##### Obs 2: algumas variáveis tem o nome de 'fofoca' pois o primeiro objetivo do projeto era desenvolver um robô que juntasse todas as fofocas de todos os perfis de fofocas em um só perfil.

<br>

> O código está todo documentado e bem fácil de entender.
> 
> **Não apagar** a pasta **media_temp** pois é nela que as mídias temporárias ficaram.
> 
> **Atenção: não abuse de colocar muitos perfis porque o Instagram bloqueia de fazer postagens, tem um limite entre 100 postagens/dia para não levar bloqueio.**
