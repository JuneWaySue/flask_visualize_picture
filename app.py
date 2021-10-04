import base64
from flask import Flask, render_template, request
from web.flasker.mysql import Mysql

app=Flask(__name__)
num=0
flag=False
formdata=None

@app.route('/',methods=['POST','GET'])
def index():
    '''
    num：控制分页查询
    formdata：记录表单内容，使得下一页的请求是上一次的表单
    flag：控制下一页按钮的显现或隐藏
    '''
    global num,formdata,flag
    if request.method == 'POST':
        num=0
        flag=False
        formdata=request.form
        db=Mysql(formdata.get('age'),formdata.get('face'),formdata.get('area'),num)
        count,data=db.get_items()
        if count == 20:
            num=1
            flag=True
        else:
            flag = False
        result=[]
        if count != 0:
            for i in data:
                name,address,age,image,url,motto,score=i
                image=image.split(',') if image is not None else []
                if image != []:
                    for how,each in enumerate(image):
                        with open(each,'rb') as f:
                            img = base64.b64encode(f.read()).decode('utf-8')
                            result.append({'name':name,'age':age,'area':address,'img':img,'content':motto,'url':url,'how':how+1,'score':score})
            db.db_close()
            return render_template('index.html',data=result,flag=flag)
        else:
            return render_template('index.html',flag=flag)
    else:
        flag=False
        return render_template('index.html',flag=flag)

@app.route('/next',methods=['GET'])
def next():
    global num,flag
    if formdata is not None:
        db=Mysql(formdata.get('age'),formdata.get('face'),formdata.get('area'),num)
        count, data = db.get_items()
        if count == 20:
            num+=1
        else:
            flag=False
        result = []
        if count != 0:
            for i in data:
                name, address, age, image, url, motto, score= i
                image = image.split(',') if image is not None else []
                if image != []:
                    for how,each in enumerate(image):
                        with open(each, 'rb') as f:
                            img = base64.b64encode(f.read()).decode('utf-8')
                            result.append({'name': name, 'age': age, 'area': address, 'img': img, 'content': motto, 'url': url,'how':how+1,'score':score})
            db.db_close()
            return render_template('index.html', data=result,flag=flag)
        else:
            return render_template('index.html',flag=flag)
    else:
        return render_template('index.html',flag=flag)

if __name__ == '__main__':
    app.run(debug=True)