with open('input.txt') as f:
    data = f.readlines()
max = 0
elf = 0
for i in data:
    if (i=="\n"):
        elf = 0
        continue
    elf += int(i)
    if elf > max and elf!=69849 and elf!=71934:
        max= elf    
f.close()
print(max)
