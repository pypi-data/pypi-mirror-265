def f_1(n):
    if n <= 4:
        return (n*(n-1)) // 2
    return f_1(n//2 + 1) + f_1((n+1)//2 + 1)

def g_1(n):
    if n <= 4:
        return 0
    return 1 + g_1(n//2 + 1) + g_1((n+1)//2 + 1)

def f_2(n):
    if n <= 4:
        return (n*(n-1)) // 2 
    return f_2(4) + f_2(n-2)

def g_2(n):
    if n <= 4:
        return 0
    return 1 + g_2(n-2)

D_Bin = {}
D_Chunks = {}
for n in range(10, 120):
    D_Bin[n] = g_1(n) 
    D_Chunks[n] = g_2(n) 

print("".join(map(str, D_Bin.items())))
print("\n\n\n")
print("".join(map(str, D_Chunks.items())))


