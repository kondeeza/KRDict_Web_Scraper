import requests
from bs4 import BeautifulSoup


def testgetwebpage():
    page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
    print(page.status_code)

    "page.content"

    soup = BeautifulSoup(page.content, 'html.parser')

    print(soup.prettify())

    print(list(soup.children))


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
            if formatted_krtrans:
                formatted_krtrans +=" "
            formatted_krtrans += kr_tran.get_text().replace('\n','').replace('\t','')

    return formatted_krtrans

def setHanja(defentry):
    if defentry.next_sibling:
        if len(defentry.next_sibling) > 1:
            return defentry.next_sibling.replace('\n','').replace('\t','').replace('(','').replace(')','').replace(' ','')
    return ""


def testgetlocalpage():
    soup = BeautifulSoup(open("krdict_general_sample.htm", 'r', encoding="utf-8"), "html.parser")
    defdiv = soup.find('ul', {'class': 'search_list'})
    fotmatted_defentries = []
    defentries = soup.find_all('a', {'title': '詳細表示'})
    for defentry in defentries:
        defobj = {}
        defentry_parent = defentry.parent.parent
        defobj['word'] = defentry.get_text()
        defobj['hanja'] = setHanja(defentry)
        defobj['pos'] = defentry.find_next_sibling("em").get_text() if defentry.find_next_sibling("em") else ""
        defobj['jp_defs'] = setJP_def(defentry_parent)
        defobj['jp_trans'] = setJP_translation(defentry_parent)
        defobj['kr_trans'] = setKR_translation(defentry_parent)


        fotmatted_defentries.append(defobj)
        print(defobj)

    "print(defdiv.contents[3])"

testgetlocalpage()