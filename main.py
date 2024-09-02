from httpx import Client
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    """Main endpoint of the api."""

    return "Hello fellow Developer. Please don't use this api, it's private btw."

@app.get("/from-video")
def scrape(url: str):
    """Get Data from video using his url."""

    data = extract_from_embed(url)
    return data

@app.get("/from-slideshow")
def scrape_slideshow(url: str):
    """Get Data from slideshow using his url."""

    data = get_from_slideshow(url)
    return data

def extract_sound(link):
    """Get Data from video using his url."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6a Build/TQ3A.230805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 MicroAdBot/1.1 (https://www.microad.co.jp/contact/)"
    }

    cookies = {
        "cf_clearance": "zl5NTyZrxt2UYkMqlzyxacBbYdAhhaFrMnqwfQBtyhg-1725188085-1.2.1.1-.kPvg7wdzPFSqHuTzP2vWZgS5C_pHRfhfxoLUDEre5Z.yx8aaK5lxcUzMSHaSBuAdMz_EhAvUYFYG6nFUGOzEBWRkTC42IZCaU6E1YTLWdsxUIWTKnULFBEoNEqLBrwwR56p0gzBQ2mck.kysL275PiLppDPGN82P8P7RQq2w47xtGKh6DxsfTFIXSn1BCELnkFpL4XyBUL9TitdeccPnsLd_gPtqKDTdiK2G3blwlN9UB.BNUBjsMiwTsuCP3mFWVn5QYNRYFzCiACfjxvrpH_QGUl0ES2o3abKfhuWrcCjN4DLoCkA.bRp.hy5dgYNhQPfkd5_D0pav7uXnbg7cDdN6TIe8n.7xR9JpHcTFknpFaxCJkVoVhfdjXRZs03mUE9O2U.PQs1_0ooGcI1mhQ",
    }
    
    url = "https://ttsave.app/download"

    data = {"query": link,"language_id":"1"}

    session = Client()

    resp = session.post(url, json=data, timeout=60, headers=headers, cookies=cookies)
    html = resp.text
    page = BeautifulSoup(html, 'html.parser')
    error_element = page.find("p")

    if error_element.text == "Error unknown":
        return "", "", ""
    else:
        span_list = [elem.text for elem in page.find_all('span')]
        audio_url = page.find('a', {'type': 'audio'}).get('href')

        return audio_url, span_list[4].split('-')[1].strip(), span_list[4].split('-')[0].strip()




def extract_from_slideshow(link):
    """Get Data from slideshow using his url."""

    url = "https://ttsave.app/download"

    data = {"query": link,"language_id":"1"}
    session = Client()

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6a Build/TQ3A.230805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 MicroAdBot/1.1 (https://www.microad.co.jp/contact/)"
    }

    cookies = {
        "cf_clearance": "zl5NTyZrxt2UYkMqlzyxacBbYdAhhaFrMnqwfQBtyhg-1725188085-1.2.1.1-.kPvg7wdzPFSqHuTzP2vWZgS5C_pHRfhfxoLUDEre5Z.yx8aaK5lxcUzMSHaSBuAdMz_EhAvUYFYG6nFUGOzEBWRkTC42IZCaU6E1YTLWdsxUIWTKnULFBEoNEqLBrwwR56p0gzBQ2mck.kysL275PiLppDPGN82P8P7RQq2w47xtGKh6DxsfTFIXSn1BCELnkFpL4XyBUL9TitdeccPnsLd_gPtqKDTdiK2G3blwlN9UB.BNUBjsMiwTsuCP3mFWVn5QYNRYFzCiACfjxvrpH_QGUl0ES2o3abKfhuWrcCjN4DLoCkA.bRp.hy5dgYNhQPfkd5_D0pav7uXnbg7cDdN6TIe8n.7xR9JpHcTFknpFaxCJkVoVhfdjXRZs03mUE9O2U.PQs1_0ooGcI1mhQ",
    }

    resp = session.post(url, json=data, timeout=60, headers=headers, cookies=cookies)
    html = BeautifulSoup(resp.text, 'html.parser')
    error_element = html.find("p")
    
    if error_element.text == "Error unknown":
        return "", "", "", "", ""
    else:
        url_list = [elem["href"] for elem in html.find_all('a')]
        span_list = [elem.string for elem in html.find_all('span')]
        h2_list = [elem.string for elem in html.find_all('h2')]
        audio_url = html.find("a", {"type": "audio"}).get("href")

        return url_list[2], audio_url, span_list[4].split('-')[1].strip(), span_list[4].split('-')[0].strip(), h2_list[0]

def get_from_slideshow(url):
    """Return scraped data of slideshow."""

    thumb_url, music_url, song_name, music_author, author_name = extract_from_slideshow(url)

    song_data = {
        'music_url': music_url,
        'video_author': author_name,
        'song_name': song_name,
        'audio_filename': f'{music_author} - {song_name} (Audio).mp3',
        'video_filename': f'{music_author} - {song_name} (Video).mp4',
        'cover_url': thumb_url,
        'music_author': music_author
    }

    return song_data if music_url != "" else "Not Found"

def extract_from_embed(url):
    """Return scraped data."""

    embed_url = f'https://www.tiktok.com/oembed?url={url}'
    client = Client()
    data = client.get(embed_url, timeout=60.0)
    data = data.json()

    if data and not data["html"]:
        return "Not Found"
    else:
        music_url, song_name, music_author = extract_sound(url)

        song_data = {
            'music_url': music_url,
            'video_author': data['author_name'],
            'song_name': song_name,
            'audio_filename': f'{music_author} - {song_name} (Audio).mp3',
            'video_filename': f'{music_author} - {song_name} (Video).mp4',
            'cover_url': data['thumbnail_url'],
            'music_author': music_author
        }

        return song_data if music_url != "" else "Not Found"

if __name__ == "___main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)