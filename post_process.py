import json
import os


def process_yt(url):
    return "https://www.youtube.com/watch?v=" + url.split('/')[-1].split('?')[0]


def process_content(content):
    try:
        mark = "</iframe><br>\n</div><br>\n"
        step = content.index(mark) + len(mark)
        content = content[step:]
        mark = "<div class=\"share wjs-window clearfix\">"
        step = content.index(mark)
        content = content[:step]
        content = content.replace("<b>", "").replace("</b>", "").replace("<br>", "").replace("</a>", "")
        content = content.replace("<i>", "").replace("</i>", "")
        content = content.replace("\n\n", "\n")
        mark = "<a href=\"http://voaspecialenglish."
        step = content.index(mark)
        mark2 = "\">VOA Learning English"
        step2 = content.index(mark2) + 2
        content = content.replace(content[step:step2], "")
        return content
    except:
        return None


def post_process(path):
    with open(path, 'r') as fn:
        data = json.loads(fn.read())
    new_data = []
    for item in data:
        content = process_content(item['content'])
        if content is None:
            continue
        new_item = {
            'url': process_yt(item['youtube']),
            'content': content,
            'thumbnail': item['thumbnail'],
            'title': item['title']
        }
        new_data.append(new_item)

    with open(path, 'w') as fn:
        json.dump(new_data, fn)


if __name__ == '__main__':
    pass
    # post_process('quote.json')
    # test_selenium()