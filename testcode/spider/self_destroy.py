class TestClass:
    def __init__(self, index):
        self.index = index
    
    def stop(self):
        self.__del__()
        

def main():
    test_len = 20
    total = []
    for i in range(test_len):
        ins = TestClass(index=i)
        total.append(ins)
    
    sample_len = 10
    import random
    for _ in range(sample_len):
        choice = random.randrange(0, len(total))
        total[choice].stop()
    
    print([x.index for x in total])

if __name__ == "__main__":
    main()