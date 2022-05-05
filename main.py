import asyncio
from os import chdir
from os.path import abspath, dirname

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("pip install beautifulsoup4")
try:
    from pyppeteer import launch
except ImportError:
    raise ImportError("pip install pyppeteer")
# スクショを格納するために、カレントディレクトリをこのファイルの実行場所にする
chdir(dirname(abspath(__file__)))
del abspath, chdir, dirname

# English -> japanese
en_word = """

ここに英語か、日本語を挿入してください。
insert here.
example:
English is a West Germanic language of the Indo-European language family, originally spoken by the inhabitants of early medieval England.
[3][4][5] It is named after the Angles, one of the ancient Germanic peoples that migrated from Anglia, a peninsula on the Baltic Sea (not to be confused with East Anglia), to the area of Great Britain later named after them: England.
The closest living relatives of English include Scots, followed by the Low Saxon and Frisian languages.
While English is genealogically West Germanic, its vocabulary is also distinctively influenced by Old Norman French and Latin, as well as by Old Norse (a North Germanic language).
[6][7][8] Speakers of English are called Anglophones.
(by english wiki)

"""


# headless mode: True or False
headless = False
######-------------------------------------------------------------------------------------------######
if len(en_word) > 5000:
    raise AttributeError(
        f"Word length over.Max 5000.{len(en_word)} characters detected.")


async def main():
    browser = await launch(headless=headless)
    page = await browser.newPage()
    res = await page.goto("https://www.deepl.com/translator")
    if res.status == 200:
        print(f"status code: {res.status}")
        await page.waitFor(2000)
        await page.type("#dl_translator > div.lmt__text > div.lmt__sides_container > section.lmt__side_container.lmt__side_container--source > div.lmt__textarea_container > div.lmt__inner_textarea_container > textarea", en_word)
        res = await _get_jpWord(page)
        print(f"trans text: {res}")

    else:
        await print(f"status code: {res.status} が返されたため、カットします。")
    await browser.close()


async def _get_jpWord(page, before_word=None):
    # htmlを解析し、和訳を抽出
    jp_word = str(BeautifulSoup(await page.content(), "html.parser").find(id="target-dummydiv").text)
    # ロード中か、更新があった場合に再起処理
    if not jp_word.strip() or jp_word != before_word:
        print("recursion: 再帰します。")
        await page.waitFor(3000)
        return await _get_jpWord(page, before_word=jp_word)
    # スクショを保存
    await page.screenshot({"path": "./EnglishToJapanese.png"})
    return jp_word


if __name__ == "__main__":
    asyncio.run(main())
