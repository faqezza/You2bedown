import os
import multiprocessing
import pyfiglet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
from termcolor import colored

def imprimir_banner(texto, creditos):
    banner = pyfiglet.figlet_format(texto, font="smslant")
    texto_verde = colored(banner, color='green')
    cred = pyfiglet.figlet_format(creditos, font="small")
    texto_cred = colored(cred, color='red')
    print(texto_verde)
    print(texto_cred)


def baixar_playlist_ytmusic(url, playlist_folder):
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    options.headless = True
    driver = webdriver.Edge(options=options)
    #driver.minimize_window() 

    wait = WebDriverWait(driver, 10000)

    driver.get(url)

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.yt-simple-endpoint')))
        links = driver.find_elements(By.CSS_SELECTOR, 'a.yt-simple-endpoint')

        for link in links:
            music_url = link.get_attribute('href')
            if music_url and "watch?v=" in music_url:
                try:
                    yt = YouTube(music_url)
                    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
                    if video:
                        video.download(output_path=playlist_folder)
                        print("Download concluído:", video.title)
                    else:
                        print("Vídeo indisponível ou não encontrado:", music_url)
                except Exception as e:
                    print("\nOcorreu um erro ao baixar o vídeo:", str(e))

    finally:
        driver.quit()

def download_playlist(playlists):
    try:
        escritorio_path = "C:\\Users\\" # Mudar para o diretorio de preferência

        max_processes = 20 
        pool = multiprocessing.Pool(processes=max_processes)

        for url, folder_name in playlists:
            playlist_path = os.path.join(escritorio_path, folder_name)

            if not os.path.exists(playlist_path):
                os.makedirs(playlist_path)

            pool.apply_async(baixar_playlist_ytmusic, args=(url, playlist_path))

        pool.close()
        pool.join()
    except Exception as error:
        print(f"\nTivemos um problema Willis {error}\n")

def processar_urls_from_txt(txt_file):
    try:
        playlists = []
        with open(txt_file, 'r') as file:
            for line in file:
                parts = line.strip().split('--', 1)
                if len(parts) == 2:
                    url = parts[0].strip()
                    folder_name = parts[1].strip()
                    playlists.append((url, folder_name))
                else:
                    url = parts[0].strip()
                    folder_name = '--'.join(parts[1:]).strip()
                    playlists.append((url, folder_name))
        return playlists
    except Exception as error:
        print(f"\nTivemos um problema Willis {error}\n")
def usage():
    print('\n----> Programa feito para baixar playlists de Youtube Music no formato .MP4\n----> Você vai precisar do navegador Edge\n----> Path default onde serão salvos os arquivos C:\\Users\\\n----> O formato da lista com as URLS playlist.txt deve ser assim:\n          https://music.youtube.com/playlist1 --NOME_DA_PASTA1\n          https://music.youtube.com/playlist2 --NOME_DA_PASTA2')


if __name__ == "__main__":
    try:
        texto = "YOU   2   BE   DOWN"
        creditos = "By  --->  Faqez"
        imprimir_banner(texto, creditos)
        usage()
        usar_arquivo = input("\nDeseja passar um arquivo.txt com as URLs das playlists? (y/n): ").lower() == 'y'

        if usar_arquivo:
            txt_file = input("Insira o caminho do arquivo .txt: ")
            playlists = processar_urls_from_txt(txt_file)
        else:
            num_playlists = int(input("Quantas playlists você deseja baixar? "))
            playlists = []
            for i in range(num_playlists):
                url = input(f"Insira a URL da {i+1}ª playlist do YouTube Music: ")
                folder_name = input(f"Insira o nome da pasta para a {i+1}ª playlist: ")
                playlists.append((url, folder_name))

        download_playlist(playlists)
        print('\n\nOBRIGADO, TUDO DE BOM!!!!\n')

    except Exception as error:
        print(f'\nOuve um problema ao tentar baixar os videos :(  {error}\n')

