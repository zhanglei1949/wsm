import web
import math
urls = (
    '/', 'index',
    '/s/', 's',
    '/image/(.*)', 'image',
    '/question/', 'question',
    )

app = web.application(urls,globals())
render=web.template.render('templates')

class index:
    def GET(self):
        return render.main()
class s:
    def GET(self):
        data = web.input()
        #return data
        query_text = data.query_text
        page_number = int(data.pg_number)
        items_per_page = 3
        # Load the search results from the backend
        query_res = [[1,2],[3,4], [5,6], [7,8] ,[9, 10], [11,12], [13,14]]
        last_page_number = int(math.ceil(float(len(query_res)) /items_per_page))
        start_page = max(1, page_number - 3)
        end_page = min(page_number+3, last_page_number) 
        start_item = max(0, (page_number-1)*items_per_page)
        end_item = min(len(query_res), start_item + items_per_page)
        return render.search_results(query_text, query_res, page_number, start_page, end_page, start_item, end_item, last_page_number)

class question:
    def GET(self):
        data = web.input()
        question_id = data.qid
        
        # get question data
        # title/content/answerlist/

        return render.question_page(...)
class image:
    def GET(self, filename):
        imageBinary = open('./templates/pics/' + filename, 'rb').read()
        return imageBinary
if __name__ == '__main__':
    app.run()


