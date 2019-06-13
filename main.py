import web
import sys
import math
sys.path.append('./ccq/wsm/src')
from searchEngine import showQues,final,readCfg
#final(query_text, zone) = dict[key]
#showQeus(qid)
urls = (
    '/', 'index',
    '/s/', 's',
    '/image/(.*)', 'image',
    '/question/', 'question',
    )

app = web.application(urls,globals())
render=web.template.render('templates')
readCfg('cfg.txt')
class index:
    def GET(self):
        return render.main()
class s:
    def GET(self):
        data = web.input()
        #return data
        query_text = data.query_text
        if (query_text == ""):
            return render.main()
        page_number = int(data.pg_number)
        qType = data.qType
        chosen_tag = data.chose_tag
        items_per_page = 10
        # Load the search results from the backend
        if (qType == "tag" and chose_tag != None):
            query_res, recommended = final(query_text, zone=chosen_tag)
            print("tag"+ chosen_tag)
        else: 
            print("qtype %s"%(qType))
            query_res, recommended = final(query_text, zone=qType)
        res_list = []
        for key,value in query_res.items():
            #if (len(value) < 5):
            #    continue
            res_list.append([key]+value)
        print(len(res_list))

        rec_list = []
        for key, value in recommended.items():
            rec_list.append([key] + value)
            #qid, link, title

        recommended = rec_list
        query_res = res_list
        last_page_number = int(math.ceil(float(len(query_res)) /items_per_page))
        start_page = max(1, page_number - 3)
        end_page = min(page_number+3, last_page_number) 
        start_item = max(0, (page_number-1)*items_per_page)
        end_item = min(len(query_res), start_item + items_per_page)

        return render.search_results(query_text, res_list, page_number, start_page, end_page, start_item, end_item, last_page_number, qType, recommended, chosen_tag)

class question:
    def GET(self):
        data = web.input()
        question_id = data.qid
        
        # get question data
        # title/content/answerlist/
        # suppose answers are list
        results, rec = showQues(int(question_id))
        res_list = []
        for key,value in results.items():
            res_list.append([key] + value)
        print(len(res_list))
        print(res_list[0]) 
        rec_list = []
        for key,value in rec.items():
            rec_list.append([key] + value)
        print(len(rec_list))
        print(rec_list[0])

        recommended = rec_list
        res_list = res_list[0]
        title = res_list[1][1]
        url = res_list[1][0]
        numviews = res_list[1][3]
        content = res_list[1][6]
        question_date = res_list[1][8]
        questioner = res_list[1][9]
        answers = res_list[2:]
        return render.question_page(title, url, content, questioner, numviews, question_date, answers, recommended)
        
class image:
    def GET(self, filename):
        imageBinary = open('./templates/pics/' + filename, 'rb').read()
        return imageBinary
if __name__ == '__main__':
    app.run()



