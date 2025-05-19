import streamlit as st
import openai
import requests
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Configurações das APIs
OPENAI_API_KEY = "sua_openai_key"
PEXELS_API_KEY = "sua_pexels_key"
openai.api_key = OPENAI_API_KEY

# Função para gerar roteiro com OpenAI
def gerar_roteiro(prompt):
    resposta = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

# Função para baixar vídeos do Pexels
def baixar_videos_pexels(query, max_videos=5):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": max_videos}
    response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
    results = response.json().get("videos", [])
    paths = []

    os.makedirs("videos", exist_ok=True)
    for i, video in enumerate(results):
        url = video["video_files"][

Perfeito. Aqui está o conteúdo completo e atualizado do `app.py`, com interface em Streamlit e usando as suas chaves da OpenAI e do Pexels para gerar roteiro, buscar vídeos e montar tudo automaticamente:

```python
import streamlit as st
import openai
import requests
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Suas chaves de API
openai.api_key = "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"
PEXELS_API_KEY = "60YiN7CjogbeWT3JyW9GSdNzvYe8O9DkovWFvjYlvytygQVjFJ1iYzab"

def gerar_roteiro(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def baixar_videos_pexels(query, total=5):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": total}
    response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
    videos = response.json()["videos"]
    
    caminhos = []
    for i, video in enumerate(videos):
        url = video["video_files"][0]["link"]
        video_bytes = requests.get(url).content
        caminho = f"video_{i}.mp4"
        with open(caminho, "wb") as f:
            f.write(video_bytes)
        caminhos.append(caminho)
    return caminhos

def criar_thumbnail(texto):
    largura, altura = 1280, 720
    imagem = Image.new("RGB", (largura, altura), color=(30, 30, 30))
    draw = ImageDraw.Draw(imagem)
    fonte = ImageFont.load_default()

    draw.text((50, 300), texto, font=fonte, fill="white")
    caminho_thumb = "thumbnail_automatica.jpg"
    imagem.save(caminho_thumb)
    return caminho_thumb

def montar_video(roteiro, videos):
    clipes = [VideoFileClip(v).subclip(0, min(5, VideoFileClip(v).duration)) for v in videos]
    video_final = concatenate_videoclips(clipes)
    video_final.write_videofile("video_base.mp4")
    return "video_base.mp4"

st.title("Gerador de Vídeos Automáticos")
st.write("Crie vídeos completos com roteiro, vídeos e thumbnail com um clique!")

if st.button("Gerar Vídeo"):
    with st.spinner("Gerando roteiro..."):
        prompt = "Liste as 10 cidades mais bonitas da América do Sul em formato enumerado, com 2-3 frases explicativas para cada cidade."
        roteiro = gerar_roteiro(prompt)
        with open("roteiro.txt", "w", encoding="utf-8") as f:
            f.write(roteiro)

    st.success("Roteiro gerado!")
    st.text_area("Roteiro:", roteiro, height=300)

    with st.spinner("Baixando vídeos..."):
        cidades = [linha.split(". ")[1].split(":")[0] for linha in roteiro.split("\n") if ". " in linha]
        caminhos_videos = []
        for cidade in cidades[:5]:
            caminhos_videos += baixar_videos_pexels(cidade, total=1)

    st.success("Vídeos baixados!")

    with st.spinner("Criando thumbnail..."):
        thumb_path = criar_thumbnail("Top 10 Cidades da América do Sul")
        st.image(thumb_path, caption="Thumbnail gerada")

    with st.spinner("Montando vídeo final..."):
        video_path = montar_video(roteiro, caminhos_videos)
        st.success("Vídeo pronto!")
        video_file = open(video_path, "rb")
        st.video(video_file.read())