
class insertionsort:
    
    def main(seq):
        '''
        insertion sort a list
        '''
        seqInt=[]
        for a in range(0,len(seq)):
            flag= False
            location=0
            x=0
            while   flag == False:
                if seq[a][x] == ' ':
                    location =x
                    flag =True
                x+=1
            
            seqInt.append(seq[a][:location])
            
        
        
      
        for i in range(1,len(seq)):
            v = seq[i]
            q = int(seqInt[i])
            j = i
        
            while j>0 and int(seqInt[j-1])>q:
                
                seq[j] = seq[j-1]
                seqInt[j] = seqInt[j-1]
                j -= 1
        
            seq[j]=v
            seqInt[j]=q
       
        return seq

if __name__ == "__main__":
    insertionsort.main()
