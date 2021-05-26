def generateTF(self, start, end):
        database = {}

        print(f"Calculating TF for {start} and {end}")
        return
               
        
        for i in range(self.num):
            print(f'Indexing file {i}')
            f = open(f"rawText/{i}.json", "r")
            context = f.read()
            try:
                j = json.loads(context)
            except:
                continue
            
            title = []
            content = []
            push = []
            
            count = 0
            
            for keyword in self.keyword:
                if keyword in j['title']:
                    title.append(count)

                j_content = j['content'].split('※ 發信站: 批踢踢實業坊')[0]
                try:
                    j_push = j['content'].split('※ 發信站: 批踢踢實業坊')[1]
                except:
                    j_push = ''

                try:
                    j_title = j_content.split('\n')[1]
                    j_content = j_content.split(j_title)[1]
                except:
                    pass
                
                if keyword in j_content:
                    content.append(count + 500)
              
                if keyword in j_push:
                    push.append(count + 1000)

                count = count + 1
       

            title.extend(content)
            title.extend(push)
            database[i] = title

        f = open(f"index.json", "w")
        f.write(json.dumps(database))
        f.close()