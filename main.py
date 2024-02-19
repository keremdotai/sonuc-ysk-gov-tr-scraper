import argparse
import json
from pathlib import Path
import os
from utils import *


logger = create_logger()

datadir = Path(__file__).parent / 'data'
os.umask(0)
os.makedirs(datadir, exist_ok=True, mode=0o777)


def scrapeYsk(date):
    logger.info(f"Date: {date}")

    try:
        with open(f"meta/{date}.json", 'r') as f:
            election_meta = json.load(f)
    except:
        logger.error(f"Meta file for {date} not found or corrupted.")
        return
    
    electiondir = datadir / date
    os.makedirs(electiondir, exist_ok=True, mode=0o777)
    
    for meta in election_meta:
        secimId = meta['secimId']
        secimTuru = meta['secimTuru']
        sandikTuru = meta['sandikTuru']

        logger.info('Meta Information:')
        logger.info(f"- secimId: {secimId}")
        logger.info(f"- secimTuru: {secimTuru}")
        logger.info(f"- sandikTuru: {sandikTuru}")

        yurtIciSonuc, baslikList = getYurtIciSonuc(secimId, secimTuru, sandikTuru)

        if secimTuru in [7, 8, 9]:
            temsilcilikSonuc, gumrukSonuc, temsilcilikBaslikList, gumrukBaslikList = getYurtDisiSonuc(secimId, secimTuru)
        else:
            temsilcilikSonuc, gumrukSonuc, temsilcilikBaslikList, gumrukBaslikList = [], [], [], []

        data = {
            'yurtIciSonuc': yurtIciSonuc,
            'baslikList': baslikList,
            'temsilcilikSonuc': temsilcilikSonuc,
            'gumrukSonuc': gumrukSonuc,
            'temsilcilikBaslikList': temsilcilikBaslikList,
            'gumrukBaslikList': gumrukBaslikList,
        }

        logger.info('Writing data to files...')
        with open(electiondir / f'{secimId}_{secimTuru}.json', 'w') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', help='Date of election', required=False, type=str, default=None)
    parser.add_argument('-a', '--all', help='Get all elections', action=argparse.BooleanOptionalAction)
    kwargs = vars(parser.parse_args())
    date = kwargs.pop('date')
    all_elections = kwargs.pop('all')

    if all_elections:
        date_list = [path.split('.')[0] for path in os.listdir('meta') if path.endswith('.json')]
        for date in date_list:
            scrapeYsk(date)
    else:
        if date is None:
            logger.error("Date must be specified.")
            return
        scrapeYsk(date)

    
if __name__ == '__main__':
    main()
