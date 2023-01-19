def diffList(newFolders,oldFolders):
    diff = list(set(newFolders) - set(oldFolders))
    diff_sorted = sorted(diff)
    return diff_sorted


A = ["D","DDD","A","AA","AB","CCC","C","AAAAA","AC","CAAA"]

A = sorted(A)
B = A.copy()
C = []

print(A)

for dir1 in A:
    print("List = " + dir1)
    for dir2 in B:        
        if dir1!=dir2 and dir1 in dir2:
            print("Found = "+dir2)
            C.append(dir2)
         
D = diffList(A,C)
print(D)

