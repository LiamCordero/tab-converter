from requests_html import HTMLSession
import sound

start='wiki_tab'
end='*****'
url="https://tabs.ultimate-guitar.com/tab/metallica/nothing-else-matters-tabs-30154"

class Tab():

    def __init__(self):
        session=HTMLSession()
        r=session.get(url)
        r.html.render()
        text=r.html.text
        start_index=text.find('Download\nPlay\n')+14
        final_index=text[start_index:].find(end)+start_index
        self.tab=text[start_index:final_index]


        self.e_is_lowercase=True
        self.strings=self._find_strings()
        self.blocks=[]
        self._strip3()
        s=sound.Sound(self.blocks)
        tstring=self.tab_string()

    def _find_strings(self):
        self.e_is_lowercase=True
        estart=self.tab.find('e|')
        if(estart==-1):
            self.e_is_lowercase=False
            estart=self.tab.find('E|')

        e=''
        done=False
        temp=self.tab[estart+2:]
        while(not done):
            last=temp.find('B|')
            add=temp[:last-1]
            add=add[:add.rfind('|')+1]
            e=e+add
            temp=temp[last:]
            if(self.e_is_lowercase):
                next=temp.find('e|')
            else:
                next=temp.find('E|')
                next+=temp[next+1:].find('E|')+1

            temp=temp[2+next:]
            if(not self.e_is_lowercase and temp.count('E|')==0):
                done=True
            if(next<0):
                done=True

        b=''
        done=False
        bstart=self.tab.find('B|')
        temp=self.tab[bstart+2:]
        while(not done):
            last=temp.find('G|')
            add=temp[:last-1]
            add=add[:add.rfind('|')+1]
            b=b+add
            temp=temp[last:]
            next=temp.find('B|')
            temp=temp[2+next:]
            if(next==-1):
                done=True

        g=''
        done=False
        gstart=self.tab.find('G|')
        temp=self.tab[gstart+2:]
        while(not done):
            last=temp.find('D|')
            add=temp[:last-1]
            add=add[:add.rfind('|')+1]
            g=g+add
            temp=temp[last:]
            next=temp.find('G|')
            temp=temp[2+next:]
            if(next==-1):
                done=True

        d=''
        done=False
        dstart=self.tab.find('D|')
        temp=self.tab[dstart+2:]
        while(not done):
            last=temp.find('A|')
            add=temp[:last-1]
            add=add[:add.rfind('|')+1]
            d=d+add
            temp=temp[last:]
            next=temp.find('D|')
            temp=temp[2+next:]
            if(next==-1):
                done=True

        a=''
        done=False
        astart=self.tab.find('A|')
        temp=self.tab[astart+2:]
        while(not done):
            last=temp.find('E|')
            add=temp[:last-1]
            add=add[:add.rfind('|')+1]
            a=a+add
            temp=temp[last:]
            next=temp.find('A|')
            temp=temp[2+next:]
            if(next==-1):
                done=True

        ee=''
        done=False
        if(self.e_is_lowercase):
            eestart=self.tab[5:].find('E|')
        else:
            eestart=self.tab[5:].find('E|')
            eestart+=self.tab[5:][eestart+1:].find('E|')+1

        temp=self.tab[5:][eestart+2:]
        while(not done):
            if(self.e_is_lowercase):
                last=temp.find('e|')
            else:
                last=temp.find('E|')
            if(last==-1):
                ee+=temp
                done=True
            else:
                add=temp[:last-1]
                add=add[:add.rfind('|')+1]
                ee=ee+add
                temp=temp[last:]
                if(self.e_is_lowercase):
                    next=temp.find('E|')
                else:
                    next=temp.find('E|')
                    next+=temp[next+1:].find('E|')+1
                temp=temp[2+next:]
                if(next==-1):
                    done=True
        #ee=ee+temp[:temp.find('|')+1]
        return [e,b,g,d,a,ee]

    def _strip3(self):
        partitions=[]
        for i in range(len(self.strings)):
            partition=self._partition(self.strings[i])
            for part in partition:
                if '-' not in part:#or ' ' not in part
                    print(part)
                    partition.remove(part)

            partitions.append(partition)
        for i in range(len(partitions[0])):
            self.blocks.append([])

        for b in range(len(self.blocks)):
            for s in range(len(self.strings)):
                self.blocks[b].append('')
                self.blocks[b][s]=partitions[s][b]

    def _findall(self,string,sub):
        locations=[]
        done=False
        back=0
        while(not done):
            next=string.find(sub)
            if(next!=-1):
                locations.append(next+back)
            else:
                done=True
            back+=len(string[:next+1])
            string=string[next+1:]
        return locations

    def _partition(self,string):
        parts=[]
        locs=self._findall(string,'|')
        for l in range(len(locs)):
            if(l==0):
                parts.append(string[:locs[l]])
                parts.append(string[locs[l]+1:locs[l+1]])
            elif(l==len(locs)-2):
                parts.append(string[locs[l]+1:locs[l+1]])
            elif(l==len(locs)-1):
                pass
            else:
                parts.append(string[locs[l]+1:locs[l+1]])
        return parts

    def tab_string(self):
        q=[]
        for block in range(len(self.blocks)):
            q.append([])
            q[block].append(self.blocks[block][0]+'|')
            q[block].append(self.blocks[block][1]+'|')
            q[block].append(self.blocks[block][2]+'|')
            q[block].append(self.blocks[block][3]+'|')
            q[block].append(self.blocks[block][4]+'|')
            q[block].append(self.blocks[block][5]+'|')
        q[0][0]='e|'+q[0][0]
        q[0][1]='B|'+q[0][1]
        q[0][2]='G|'+q[0][2]
        q[0][3]='D|'+q[0][3]
        q[0][4]='A|'+q[0][4]
        q[0][5]='E|'+q[0][5]
        return q

    def length(self):
     return 12+ 6*len(self.blocks)

def main():
    tab=Tab()

if(__name__=='__main__'):
    main()
