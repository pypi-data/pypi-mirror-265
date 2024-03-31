import inputed
import fd
import dir


pair = inputed.starter()
try:
    if pair[0]:
        fd.spec(pair[1])
    else:
        dir.spec(pair[1])
except TypeError:
    print(end="")
