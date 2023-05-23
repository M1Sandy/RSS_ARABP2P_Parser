from sys import flags
import feedparser
import time
import subprocess
from sympy import false, true
from qbittorrent import Client
import arabic_reshaper
import schedule
import threading

def fixArabic(txt):
    fixed = arabic_reshaper.reshape(txt)
    fixed = fixed[::-1]
    return fixed

config = open("C:\\Users\\M1Sandy\\Documents\\code\\My_RSS_Parser\\config.txt",encoding='utf-8') # edit this to ur path
lines = config.readlines()

qb = Client('http://127.0.0.1:8080/')
qb.login()
fParser = false
fMover = false

def Parser():
    print("[*] Parser Started.")
    # Lookup and Download
    rss = feedparser.parse("[rss url]") # add ur own RSS url
    for line in lines:
        for entry in rss.entries:
            arEntryTitle = arabic_reshaper.reshape(entry.title)
            arEntryTitle = arEntryTitle[::-1]
            if fixArabic(line).replace("\n","") not in arEntryTitle:
                continue
            print("[*] Found: " + arEntryTitle)
            torrent_file = entry.link
            qb.download_from_link(torrent_file, category='ArabicSeries')
            print("[+] Downlading Attempt: " + arEntryTitle)
            fParser = true

def Mover():
    print("[*] Mover Started.")
    tors = qb.torrents(category='ArabicSeries')
    for tor in tors:
        if tor['state'] != "downloading" or tor['state'] != "stalledDown" and tor['amount_left'] == 0:      # filter check too
            fixed_file_name = fixArabic(tor['name'])
            print("[*] Downloaded: " + fixed_file_name + " State: " + tor['state'])
            dstFolder = "Z:\\Plex\\TV Shows Arabic\\"
            last_filename = ""
            srcFolder = tor['save_path']+'\\'+ tor['name'] + "\\"
            for tmp in lines:
                fixline = tmp.replace("\n","")
                if fixArabic(fixline) not in fixed_file_name:
                    continue
                else:
                    last_filename=fixline
                    break
            dstFolder = dstFolder + last_filename
            cmd = "echo N | xcopy /I \"" + srcFolder + "\" \"" + dstFolder + "\" "
            subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL)
            time.sleep(30)
            print("[+] Copied: " + fixed_file_name)
            cmd = '"C:\\Program Files (x86)\\Plex\\Plex Media Server\\Plex Media Scanner.exe" --scan --refresh --force --section 11'
            subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL)
            print("[+] Plex arabic library scanned!.")

            qb.set_category(tor['infohash_v1'],category="MovedArabicSeries")
            fMover = true

def Reseter():
    fParser = false
    fMover = false


def run_thread(func):
    job = threading.Thread(target=func)
    job.start()

schedule.every().day.at("03:28").do(Parser)
schedule.every().day.at("03:30").do(Mover)

schedule.every().day.at("04:00").do(Parser)
schedule.every().day.at("04:02").do(Mover)

schedule.every().day.at("04:15").do(Parser)
schedule.every().day.at("04:18").do(Mover)

schedule.every().day.at("04:28").do(Parser)
schedule.every().day.at("04:30").do(Mover)


schedule.every().day.at("04:45").do(Parser)
schedule.every().day.at("04:48").do(Mover)

schedule.every().day.at("05:30").do(Parser)
schedule.every().day.at("05:35").do(Mover)



while True:
    schedule.run_pending()

        
    print("[*] Waiting for scheduled task . . ." )
    time.sleep(60) 
