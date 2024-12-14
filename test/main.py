a = input()
s = int(input())
g = 0
for i in range(s):
    w = input()
    if a in w:
        g += 1
if g >= 3:
    print('МЫСЛЬ ЕСТЬ!')
else:
    print('ПОСИДИМ ЕЩЕ')
t = (s - g)
print((t / 100) * s)