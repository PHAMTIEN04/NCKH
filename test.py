def traodoi(text):
    dict_t = {'A':'B C','B':'A C F','C':'A B F','D':'E G','E':'D F G','F':'B C E G','G':'D E F'}
    return dict_t.get(text)
n = input('Nhập: ')
print(traodoi(n))