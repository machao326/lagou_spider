# -*-coding:utf-8-*-


import requests
import xlwt


class Lagou_job(object):
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Mobile Safari/537.36',
            'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
            'Cookie': 'user_trace_token=20170921093258-cc8e4c13-9e6c-11e7-9d07-525400f775ce; LGUID=20170921093258-cc8e52b6-9e6c-11e7-9d07-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAACEBACDGD4C15CDA891A7242B76AA4F9B7450B8B; _gat=1; PRE_UTM=; PRE_HOST=www.sogou.com; PRE_SITE=https%3A%2F%2Fwww.sogou.com%2Flink%3Furl%3DhedJjaC291NlQquFD-D9iKfCABISWiMgDLW1Nx6fG3psqHL_zYlG_a3mlRzfPLR2; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2Fj75915.html; TG-TRACK-CODE=index_search; _gid=GA1.2.405703854.1505957562; _ga=GA1.2.1930895945.1505957562; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505957579,1505957596,1505957630,1505969456; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505969469; LGSID=20170921125112-7dcd03f6-9e88-11e7-9d2f-525400f775ce; LGRID=20170921125125-85aaed04-9e88-11e7-91fb-5254005c3644; SEARCH_ID=746090bf111a497aa55f7f1b8dabffd2'
        }

    def get_job_list(self, page):
        self.data = {
            'first': 'true',
            'pn': page,
            'kd': 'python'
        }
        res = requests.post(self.url, data=self.data, headers=self.headers)
        result = res.json()
        # print(result)  # debug
        jobs = result['content']['positionResult']['result']
        return jobs

    def make_els(self):
        excelTabel = xlwt.Workbook()  # 创建excel对象
        # 如果对一个单元格重复操作，会引发
        # returns error:
        # Exception: Attempt to overwrite cell:
        # sheetname=u'sheet 1' rowx=0 colx=0
        # 所以在打开时加cell_overwrite_ok=True 解决
        sheet_1 = excelTabel.add_sheet('lagouByLi', cell_overwrite_ok=True)
        sheet_1.write(0, 0, 'companyFullName')
        sheet_1.write(0, 1, 'city')
        sheet_1.write(0, 2, 'district')
        sheet_1.write(0, 3, 'jobNature')
        sheet_1.write(0, 4, 'positionName')
        sheet_1.write(0, 5, 'salary')
        sheet_1.write(0, 6, 'secondType')
        sheet_1.write(0, 7, 'workYear')
        sheet_1.write(0, 8, 'companySize')
        sheet_1.write(0, 9, 'education')
        n = 1
        for page in range(1, 31):  # 前30页
            for job in self.get_job_list(page=page):
                if '1-3' in job['workYear'] and '全职' in job['jobNature'] and '本科' in job['education']:
                    sheet_1.write(n, 0, job['companyFullName'])
                    sheet_1.write(n, 1, job['city'])
                    sheet_1.write(n, 2, job['district'])
                    sheet_1.write(n, 3, job['jobNature'])
                    sheet_1.write(n, 4, job['positionName'])
                    sheet_1.write(n, 5, job['salary'])
                    sheet_1.write(n, 6, job['secondType'])
                    sheet_1.write(n, 7, job['workYear'])
                    sheet_1.write(n, 8, job['companySize'])
                    sheet_1.write(n, 9, job['education'])
                    n += 1

        # 保存文件
        excelTabel.save('lagou_byLi.xls')


if __name__ == '__main__':
    lagou_job = Lagou_job()
    # lagou_job.get_job_list(1)  # debug
    lagou_job.make_els()
