import unsync

type(unsync.working)

unsync.working(1)

unsync.working.delay(1)

unsync.working.delay(1)

for i in range(3, 50):
    result = unsync.working.delay(i)
    print(result)