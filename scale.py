def main():
    skin_scale = [
        (244, 242, 245),
        (236, 235, 233),
        (250, 249, 247),
        (253, 251, 230),
        (253, 246, 230),
        (254, 247, 229),
        (250, 240, 239),
        (243, 234, 229),
        (244, 241, 234),
        (251, 252, 244),
        (252, 248, 237),
        (254, 246, 225),
        (255, 249, 225),
        (255, 249, 225),
        (241, 231, 195),
        (239, 226, 173),
        (224, 210, 147),
        (242, 226, 151),
        (235, 214, 159),
        (235, 217, 133),
        (227, 196, 103),
        (225, 193, 106),
        (223, 193, 123),
        (222, 184, 119),
        (199, 164, 100),
        (188, 151, 98),
        (156, 107, 67),
        (142, 88, 62),
        (121, 77, 48),
        (100, 49, 22),
        (101, 48, 32),
        (96, 49, 33),
        (87, 50, 41),
        (64, 32, 21),
        (49, 37, 41),
        (27, 28, 46),
    ]

    gaps = {
        'red': None,
        'green': None,
        'blue': None,
    }
    
    index = {
        'red': 0,
        'green': 1,
        'blue': 2
    }
    for key, gap in gaps.items():
        gaps[key] = [0] + [skin_scale[i][index[key]] - skin_scale[i+1][index[key]] for i in range(len(skin_scale[1:]))]
        
    import matplotlib.pyplot as plt
    import numpy as np
    total = np.array([
        gaps['red'], gaps['blue'], gaps['green']
    ])
    total = np.sum(total, axis=0)
    x_scale = np.arange(0, len(skin_scale), 1)
    #plt.plot(x_scale, gaps['red'], 'r--', x_scale, gaps['blue'], 'b--', x_scale, gaps['green'], 'g--', x_scale, total, 'k-')
    plt.plot(x_scale, gaps['red'], 'r--', x_scale, gaps['blue'], 'b--', x_scale, gaps['green'], 'g--')
    plt.xlabel('Scale value', labelpad=15, fontdict={'family': 'times new roman', 'color': 'k', 'weight': 'bold', 'size': 16})
    plt.ylabel('Gap(Signed)', labelpad=15, fontdict={'family': 'times new roman', 'color': 'k', 'weight': 'bold', 'size': 16})
    plt.title("Gaps of Von Luschan's chromatic scale", fontdict={'family': 'times new roman', 'color': 'k', 'weight': 'bold', 'size': 20})
    plt.grid(True, axis='x', alpha=0.5)
    plt.xticks(range(len(skin_scale)))
    plt.show()

if __name__ == "__main__":
    main()