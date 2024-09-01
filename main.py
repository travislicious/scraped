from httpx import Client
from bs4 import BeautifulSoup
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def scrape(url: str):
    data = main(url)
    return data


def get_page(client: Client, url: str, tiktok_url: str):
    """Get the HTML content of a webpage using the provided client and URL."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6a Build/TQ3A.230805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.188 Mobile Safari/537.36 MicroAdBot/1.1 (https://www.microad.co.jp/contact/)"
    }
    query = {
        'language_id': "1",
        'query': tiktok_url
    }
    cookies = {
        "cf_clearance": "zl5NTyZrxt2UYkMqlzyxacBbYdAhhaFrMnqwfQBtyhg-1725188085-1.2.1.1-.kPvg7wdzPFSqHuTzP2vWZgS5C_pHRfhfxoLUDEre5Z.yx8aaK5lxcUzMSHaSBuAdMz_EhAvUYFYG6nFUGOzEBWRkTC42IZCaU6E1YTLWdsxUIWTKnULFBEoNEqLBrwwR56p0gzBQ2mck.kysL275PiLppDPGN82P8P7RQq2w47xtGKh6DxsfTFIXSn1BCELnkFpL4XyBUL9TitdeccPnsLd_gPtqKDTdiK2G3blwlN9UB.BNUBjsMiwTsuCP3mFWVn5QYNRYFzCiACfjxvrpH_QGUl0ES2o3abKfhuWrcCjN4DLoCkA.bRp.hy5dgYNhQPfkd5_D0pav7uXnbg7cDdN6TIe8n.7xR9JpHcTFknpFaxCJkVoVhfdjXRZs03mUE9O2U.PQs1_0ooGcI1mhQ",
    }

    response = client.post(url, json=query, headers=headers, cookies=cookies, timeout=60.0)
    return response.text

def main(link):
    url = "https://ttsave.app/download"
    tiktok_url = link
    client = Client()
    html = get_page(client, url, tiktok_url)
    return parse_html(html)

def parse_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    print(soup.prettify())
    title = soup.find_all('h2')[0].get_text()
    audio_url = soup.find('a', {'type': 'audio'}).get('href')
    # Now you can use the tree object to navigate and search the HTML content
    print(title)
    print(audio_url)
    return {'title': title, 'audio_url': audio_url}

if __name__ == "___main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)