import requests
from tqdm import tqdm
from .api import URL
from .logger import create_logger, log_exception


__all__ = [
    'getUlkeList',
    'getGumrukList',
    'getDisTemsilcilikList',
    'getIlList',
    'getIlceList',
    'getSecimSandikSonucList',
    'getSandikSecimSonucBaslikList',
    'getYurtIciSonuc',
    'getYurtDisiSonuc',
]

logger = create_logger()


def getData(url):
    logger.info(f"GET {url}")

    data = None

    try:
        response = requests.get(url)
        logger.info(f"Status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
    except BaseException as e:
        log_exception(logger, e)
    finally:
        return data
    

def getUlkeList(secimId):
    name = 'getUlkeList'
    url = f"{URL}/{name}?secimId={secimId}"

    return getData(url)


def getGumrukList(secimId):
    name = 'getGumrukList'
    url = f"{URL}/{name}?secimId={secimId}"

    return getData(url)


def getDisTemsilcilikList(secimId, ulkeId):
    name = 'getDisTemsilcilikList'
    url = f"{URL}/{name}?secimId={secimId}&ulkeId={ulkeId}"

    return getData(url)
    

def getIlList(secimId, secimTuru, sandikTuru, yurtIciDisi):
    name = 'getIlList'
    url = f"{URL}/{name}?secimId={secimId}&secimTuru={secimTuru}&sandikTuru={sandikTuru}&yurtIciDisi={yurtIciDisi}"

    return getData(url)
    

def getIlceList(secimId, secimTuru, ilId, secimCevresiId, sandikTuru, yurtIciDisi):
    name = 'getIlceList'
    url = f"{URL}/{name}?secimId={secimId}&secimTuru={secimTuru}&ilId={ilId}&secimCevresiId={secimCevresiId}&sandikTuru={sandikTuru}&yurtIciDisi={yurtIciDisi}"

    return getData(url)


def getSecimSandikSonucList(secimId, secimTuru, yurtIciDisi, ilId='', ilceId='', beldeId='', birimId='', secimCevresiId='', ulkeId='', disTemsilcilikId='', gumrukId=''):
    name = 'getSecimSandikSonucList'
    url = f"{URL}/{name}?secimId={secimId}&secimTuru={secimTuru}&ilId={ilId}&ilceId={ilceId}&beldeId={beldeId}&birimId={birimId}&muhtarlikId=&cezaeviId=&sandikTuru=&sandikNoIlk=&sandikNoSon=&ulkeId={ulkeId}&disTemsilcilikId={disTemsilcilikId}&gumrukId={gumrukId}&yurtIciDisi={yurtIciDisi}&sandikRumuzIlk=&sandikRumuzSon=&secimCevresiId={secimCevresiId}&sandikId=&sorguTuru=2"

    return getData(url)


def getSandikSecimSonucBaslikList(secimId, secimTuru, yurtIciDisi, ilId='', secimCevresiId=''):
    name = 'getSandikSecimSonucBaslikList'
    url = f"{URL}/{name}?secimId={secimId}&secimCevresiId={secimCevresiId}&ilId={ilId}&bagimsiz=1&secimTuru={secimTuru}&yurtIciDisi={yurtIciDisi}"

    return getData(url)


def getYurtIciSonuc(secimId, secimTuru, sandikTuru):
    yurtIciSonuc = []
    baslikList = []

    yurtIciDisi = 1

    ilList = getIlList(secimId=secimId, secimTuru=secimTuru, sandikTuru=sandikTuru, yurtIciDisi=yurtIciDisi)
    for il in tqdm(ilList, desc='Yurt ici sandik sonuclari'):
        ilceList = getIlceList(secimId=secimId, secimTuru=secimTuru, ilId=il['il_ID'], secimCevresiId=il['secim_CEVRESI_ID'], sandikTuru=sandikTuru, yurtIciDisi=yurtIciDisi)
        for ilce in ilceList:
            data = getSecimSandikSonucList(secimId=secimId, secimTuru=secimTuru, ilId=il['il_ID'], ilceId=ilce['ilce_ID'], beldeId=ilce['belde_ID'], birimId=ilce['birim_ID'], yurtIciDisi=yurtIciDisi, secimCevresiId=il['secim_CEVRESI_ID'])
            yurtIciSonuc += data

            baslik = getSandikSecimSonucBaslikList(secimId=secimId, secimCevresiId=il['secim_CEVRESI_ID'], ilId=il['il_ID'], secimTuru=secimTuru, yurtIciDisi=yurtIciDisi)
            baslikList += baslik

    return yurtIciSonuc, baslikList


def getYurtDisiSonuc(secimId, secimTuru):
    temsilcilikSonuc, gumrukSonuc = [], []
    temsilcilikBaslikList, gumrukBaslikList = [], []

    yurtIciDisi = 2

    ulkeList = getUlkeList(secimId=secimId)
    for ulke in tqdm(ulkeList, desc='Dis temsilcilik sandik sonuclari'):
        disTemsilcilikList = getDisTemsilcilikList(secimId=secimId, ulkeId=ulke['ulke_ID'])
        for disTemsilcilik in disTemsilcilikList:
            data = getSecimSandikSonucList(secimId=secimId, secimTuru=secimTuru, ulkeId=ulke['ulke_ID'], disTemsilcilikId=disTemsilcilik['dis_TEMSILCILIK_ID'], yurtIciDisi=yurtIciDisi)
            temsilcilikSonuc += data

            baslik = getSandikSecimSonucBaslikList(secimId=secimId, secimTuru=secimTuru, yurtIciDisi=yurtIciDisi)
            temsilcilikBaslikList += baslik

    gumrukList = getGumrukList(secimId=secimId)
    for gumruk in tqdm(gumrukList, desc='Gumruk sandik sonuclari'):
        data = getSecimSandikSonucList(secimId=secimId, secimTuru=secimTuru, gumrukId=gumruk['gumruk_ID'], yurtIciDisi=yurtIciDisi)
        gumrukSonuc += data

        baslik = getSandikSecimSonucBaslikList(secimId=secimId, secimTuru=secimTuru, yurtIciDisi=yurtIciDisi)
        gumrukBaslikList += baslik

    return temsilcilikSonuc, gumrukSonuc, temsilcilikBaslikList, gumrukBaslikList
