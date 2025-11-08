def overlap(rec1, rec2):
    return rec1[0] < rec2[2] and rec2[0] < rec1[2] and rec1[1] < rec2[3] and rec2[1] < rec1[3]



def revrseY(r):
    t = 7
    r[1] = abs(r[1]-7)
    r[3] = abs(r[3]-7)
    return r

rec1 = [1,3,4,1]
rec2 = [5,4,9,2]
rec3 = [3,5,6,2]


print(overlap(revrseY(rec2) , revrseY(rec1)))