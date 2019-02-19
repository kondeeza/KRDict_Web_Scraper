import requests
from bs4 import BeautifulSoup
import csv
import urllib.request

def testgetwebpage():
    page = requests.get("https://krdict.korean.go.kr/jpn/dicSearchDetail/searchDetailWordsResult?nation=jpn&nationCode=7&searchFlag=Y&sort=W&currentPage=1&ParaWordNo=&syllablePosition=&actCategoryList=&all_gubun=ALL&gubun=W&gubun=P&gubun=E&all_wordNativeCode=ALL&wordNativeCode=1&wordNativeCode=2&wordNativeCode=3&wordNativeCode=0&sp_code=14&all_imcnt=ALL&imcnt=1&imcnt=2&imcnt=3&imcnt=0&all_multimedia=ALL&multimedia=P&multimedia=I&multimedia=V&multimedia=A&multimedia=S&multimedia=N&searchSyllableStart=&searchSyllableEnd=&searchOp=AND&searchTarget=word&searchOrglanguage=-1&wordCondition=wordAll&query=&blockCount=100")
    print(page.status_code)

    "page.content"

    soup = BeautifulSoup(page.content, 'html.parser')

    print(soup.prettify())

    print(list(soup.children))




def savetocsv(fotmatted_defentries,mode):
    """
    :param fotmatted_defentries:
    :param mode:  either "w" or "a"  (overwrite and append)
    :return:
    """
    # open a csv file with append, so old data will not be erased

    with open("index.csv", mode, encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        if (mode=='w'):
            writer.writerow(['word', 'jp_defs','pos', 'hanja', 'jp_trans', 'kr_trans'])

        for defentry in fotmatted_defentries:
            "print(defentry)"
            "writer.writerow([defentry['word'], defentry['jp_defs'], defentry['pos'], defentry['hanja'], defentry['jp_trans'], defentry['kr_trans'] ])"
            writer.writerow([defentry['word'], defentry['jp_defs'], defentry['pos'], defentry['hanja'], defentry['jp_trans'] ])



def setJP_def(defentry_parent):
    """
    :param defentry_parent example:
    <li>
        <p>	<a href="{Omitted} title="詳細表示"><strong>-거나</strong></a> 	<em style="font-style:normal;margin-left:4px;margin-right:-1px;">「어미」</em>		</p>
        <ol>
            <li>
            <p class="manyLang7 theme1 " style="line-height: 30px;">
                <strong>1.</strong>
                <span class="transFont7">か。とか	</span>
            </p>
            <p class="sub_p1" style="line-height: 20px;">앞에 오는 말과 뒤에 오는 말 중에서 하나가 선택될 수 있음을 나타내는 연결 어미.</p>
            <p class="sub_p1 manyLang7 defFont7">前の言葉と後の言葉のうち、どちらかが選択されうるという意を表す「連結語尾」。 </p>
            </li>
        </ol>
    </li>
    """
    jpdefs = defentry_parent.find_all('p', {'class': 'manyLang7 theme1 '})
    formatted_jpdefs = ""
    if jpdefs:
        for jpdef in jpdefs:
            if formatted_jpdefs:
                formatted_jpdefs +=" "

            formatted_jpdefs += jpdef.get_text().replace('\n','').replace('\t','')

    return formatted_jpdefs

def setJP_translation(defentry_parent):
    jptranslations = defentry_parent.find_all('p', {'class': 'sub_p1 manyLang7 defFont7'})
    formatted_jptrans = ""
    if jptranslations:
        for jp_tran in jptranslations:
            if formatted_jptrans:
                formatted_jptrans +=" "
            formatted_jptrans += jp_tran.get_text().replace('\n','').replace('\t','')

    return formatted_jptrans

def setKR_translation(defentry_parent):
    krtranslations = defentry_parent.find_all('p', {'class': 'sub_p1'})
    formatted_krtrans = ""
    if krtranslations:

        for kr_tran in krtranslations:
            if kr_tran.has_attr('style'):
                if formatted_krtrans:
                    formatted_krtrans +=" "
                formatted_krtrans += kr_tran.get_text().replace('\n','').replace('\t','')

    return formatted_krtrans

def setHanja(defentry):
    if defentry.next_sibling:
        if len(defentry.next_sibling) > 1:
            return defentry.next_sibling.replace('\n','').replace('\t','').replace('(','').replace(')','').replace(' ','')
    return ""


def getDefFrom_localpage():
    soup = BeautifulSoup(open("KRDict_JP_All_Except_Noun_Verb_Eomi_PartOfSpeech_.htm", 'r', encoding="utf-8"), "html.parser")
    defdiv = soup.find('ul', {'class': 'search_list'})
    fotmatted_defentries = []
    defentries = soup.find_all('a', {'title': '詳細表示'})
    for defentry in defentries:
        defobj = {}
        defentry_parent = defentry.parent.parent
        defobj['word'] = defentry.get_text().replace('\t','').replace(' ','')
        defobj['hanja'] = setHanja(defentry)
        defobj['pos'] = defentry.find_next_sibling("em").get_text().replace('\t','') if defentry.find_next_sibling("em") else ""
        defobj['jp_defs'] = setJP_def(defentry_parent)
        defobj['jp_trans'] = setJP_translation(defentry_parent)
        defobj['kr_trans'] = setKR_translation(defentry_parent)


        fotmatted_defentries.append(defobj)
        "print(defobj)"

    for fotmatted_defentry in fotmatted_defentries:
        "print(fotmatted_defentry)"

    savetocsv(fotmatted_defentries,"w")

"getDefFrom_localpage()"