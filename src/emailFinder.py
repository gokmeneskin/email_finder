import codecs
from bs4 import BeautifulSoup
import datetime
import os
import re
import sys
from urllib.request import Request, urlopen

file_formats = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.gif', '.GIF', '.pdf', '.PDF', '.xls', '.XLS', '.xlsx', '.XLSX', '.doc', '.DOC', '.docx', '.DOCX', '.ppt', '.PPT', '.pptx', '.PPTX']
base_dir = os.path.dirname(os.path.abspath(__file__))
global base_url
base_url = ''
global links
links = []
global links_on_error
links_on_error = []
global total_emails
total_emails = []


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


def clear_data():
    global base_url, links, links_on_error, total_emails
    base_url = ''
    links = []
    links_on_error = []
    total_emails = []

def get_soup(url):
    try:
        headers = {'User-Agent': 'Mozilla'}
        q = Request(url, headers=headers)
        with urlopen(q) as p:
            page = p.read()
        # soup = BeautifulSoup(page, 'lxml')
        # new_soup = soup.encode('utf-8').decode('ascii', 'ignore')
        return BeautifulSoup(page, 'html.parser')
    except Exception as e:
        if url not in links_on_error:
            links_on_error.append(url)
        return 'hata'


def find_fist_links(soup):
    if soup != 'hata':
        for link in soup.find_all('a'):
            url = str(link.get('href'))
            is_file = False
            for file_format in file_formats:
                if file_format in url:
                    is_file = True
                    break
            if is_file:
                pass
            elif base_url in url:
                if url not in links:
                    links.append(url)
            elif base_url.replace('www.', '') in url:
                if url not in links:
                    links.append(url)
            elif base_url.replace('http://', '') in url:
                if url not in links:
                    links.append('http://' + url)
            elif base_url.replace('https://', '') in url:
                if url not in links:
                    links.append('https://' + url)
            elif url[0:4] == 'http':
                pass
            elif url[0:3] == 'www':
                pass
            elif url[0:7] == 'mailto:':
                pass
            elif url == '' or url == '#':
                pass
            elif url[0:1] == '#':
                pass
            elif url[0:1] == '/':
                new_url = base_url + url[1:len(url)+1]
                if new_url not in links:
                    links.append(new_url)
            else:
                new_url = base_url + url
                if new_url not in links:
                    links.append(new_url)


def find_child_links(first_link):
    find_fist_links(get_soup(first_link))


def generate_links():
    print('[i]', base_url, 'adresi kontrol ediliyor...')
    find_fist_links(get_soup(base_url))
    print('[i]', base_url, 'adresinde toplam', len(links), 'adet ana link bulundu.')
    if len(links) == 0:
        stop_or_continue = input('[?] Başka arama yapmak ister misiniz? (e/h): ')
        if stop_or_continue.lower() == 'e':
            clear_data()
            main()
        else:
            sys.exit(0)
    print('[i] Linkler kontrol ediliyor...')
    links_count = len(links)

    first_links = links[:]
    # Initial call to print 0% progress
    printProgressBar(0, len(first_links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    for i, link in enumerate(first_links):
        find_child_links(link)
        printProgressBar(i + 1, len(first_links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    print('[i] Toplam', len(links), 'adet alt link elde edildi.')
    first_links_count = len(links)
    if links_count == first_links_count:
        return
    print('[i] Linkler kontrol ediliyor...')
    

    second_links = links[:]
    # Initial call to print 0% progress
    printProgressBar(0, len(second_links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    for i, link in enumerate(second_links):
        find_child_links(link)
        printProgressBar(i + 1, len(second_links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    print('[i] Toplam', len(links), 'adet alt link elde edildi.')
    second_links_count = len(links)
    if first_links_count == second_links_count:
        return
    print('[i] Linkler kontrol ediliyor...')

    third_links = links[:]
    # Initial call to print 0% progress
    printProgressBar(0, len(third_links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    for i, link in enumerate(third_links):
        find_child_links(link)
        printProgressBar(i + 1, len(third_links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    print('[i] Toplam', len(links), 'adet alt link elde edildi.')


def find_emails():
    print('[i] Email\'ler aranıyor...')
    printProgressBar(0, len(links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    for i, link in enumerate(links):
        soup = get_soup(link)
        emails = re.findall(r"[\w\.-]+@[\w\.-]+", str(soup))
        if len(emails) > 0:
            for email in emails:
                if email not in total_emails:
                    total_emails.append(email)
        printProgressBar(i + 1, len(links), prefix = '[p] İlerleme:', suffix = 'Tamamlandı', length = 50)
    print('[i] Toplam', len(total_emails), 'adet mail bulundu.')

def main():
    global base_url
    base_url = input('[?] Arama yapmak istediğiniz domaini http(s)://www.example.com/ şekilinde giriniz: ')
    generate_links()
    find_emails()
    directory = base_url.split('.')[1]
    today = datetime.datetime.now().date()
    today_str = str(today).replace('-','')
    print('[i] Sonuçlar kaydediliyor...')
    project_result_dir = os.path.join(base_dir, directory, today_str)
    if not os.path.exists(project_result_dir):
        os.makedirs(project_result_dir)
    with open(os.path.join(project_result_dir, 'links.txt'), 'w') as f:
        links_str = '\n'.join(links)
        f.write(links_str)
    with open(os.path.join(project_result_dir, 'links_on_error.txt'), 'w') as f:
        links_on_error_str = '\n'.join(links_on_error)
        f.write(links_on_error_str)
    with open(os.path.join(project_result_dir, 'emails.txt'), 'w', encoding='utf-8') as f:
        total_emails_str = '; '.join(total_emails)
        f.write(total_emails_str)
    
    stop_or_continue = input('[?] Başka arama yapmak ister misiniz? (e/h): ')
    if stop_or_continue.lower() == 'e':
        clear_data()
        main()


if __name__ == "__main__":
    main()
