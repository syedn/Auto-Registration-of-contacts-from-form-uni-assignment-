import web
import matplotlib.pyplot as pygraph
urls = (
  '/form', 'Index'
)

app = web.application(urls, globals())

#render = web.template.render('/templates/')
#render = web.template.render('C:/Users/nazneen/Desktop/1 semester/intro to web/assignment/assignment4/DynamicWeb/templates')
render = web.template.render('../templates')

credentials_list = [
    ["Peter", "pete@gmail.com"],
    ["Korok", "sengupta@yahoo.com"],
    ["Stefan", "stef@gmail.com"],
    ["Mara", "mara@yahoo.com"],
    ["Jun", "jun@gmail.com"],
    ["Omar", "omar@uni-koblenz.com"],
    ["Claudia", "claudia@gmail.com"],
    ["Nina", "nina@airbnb.com"],
    ["Husam", "sam@gmail.com"],
    ["Rajesh", "raj@gmail.com"],
]
contactsFile = open('contacts.txt','r').read()
contactsList = []
transferList = []
contactSingle = []
#creating sub-lists within list to add to server and compare
for contact in contactsFile.split('\n'):
    for single in contact.split(','):
        contactSingle.append(single)
    contactSingle = ' '.join(contactSingle).split() #remove empty elements
    contactsList.append(contactSingle)
    contactSingle = [] # to create new sub list


class Index(object):
    def GET(self):
        return render.form() #web page in template forlder named form

    def POST(self):
        #for loop for each element 
        msg = ''
        list_size = 0
        count = 0
        response = ''
        success = 0
        fail = 0
        history = ''
        elements = []
        #repeat the process for each contact
        for registerContact in contactsList:
            count +=1
            if registerContact in credentials_list:
                msg = "Error! This contact is already in the list."
                list_size = len(credentials_list)
                elements.append(list_size) #for graph
                singleRegister = ' : '.join(registerContact) #make string to send to template
                response += '<div style="color:#ff0000"><p style="font-weight:bold">'+str(count)+') '+singleRegister+'</p>'+msg+'<p> List Size:'+str(list_size)+'</p>'
                fail += 1
                history += " Attempt: "+str(count)+" Number of elements "+str(list_size)+"\n"
            else:
                msg = "<p>Success! You have added a new contact to the list. </p>"
                credentials_list.append(registerContact)
                list_size = len(credentials_list)
                elements.append(list_size)
                singleRegister = ' : '.join(registerContact)
                response += '<div style="color:#009900"><p style="font-weight:bold">'+str(count)+') '+singleRegister+'</p>'+msg+'<p> List Size:'+str(list_size)+'</p>'
                success +=1
                history += " Attempt: "+str(count)+" Number of elements "+str(list_size)+"\n"
        #write attempts and number of elements on file
        historyFile = open('history.txt','w')
        historyFile.write(history)
        historyFile.close()
        #1) graphical representation of the successful and unsuccessful attempts
        fig, ax = pygraph.subplots()  # create figure & 1 axis
        pygraph.title("Successful and Unsuccessful attempts of registering")
        pygraph.ylabel('Attempts')
        pygraph.xlabel('Status')
        xtiks = range(2)
        ax.set_xticks(xtiks)
        ax.set_xticklabels(('Success', 'Fail'))
        numVal = range(2)
        ax.bar(numVal,[success,fail])
        pygraph.show()
        fig.savefig('static/statusCheckGraph.png')
        pygraph.close(fig) 
        img1 = "<img src='static/statusCheckGraph.png' />"
        #2) graphical representation of the successful and unsuccessful attempts
        fig, ax = pygraph.subplots()  # create figure & 1 axis
        pygraph.title("Attempts and Number of elements")
        pygraph.ylabel('Attempts')
        pygraph.xlabel('Number of elements in list')
        ax.set_xticks(range(len(elements)))
        ax.set_xticklabels(range(1,count+1))
        ax.set_yticks(range(list_size+1))
        ax.bar(range(len(elements)),elements)
        pygraph.show()
        fig.savefig('static/historyGraph.png')
        pygraph.close(fig) 
        img2 = "<img src='static/historyGraph.png' />"
        
        #web page in template forlder named index
        return render.index(response,fail,success,img1,img2)


if __name__ == "__main__":
    app.run()