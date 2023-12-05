import scipy.io
import matplotlib.pyplot as plt

mat = scipy.io.loadmat('../mask_files/santa.mat')

print(mat.keys())

for i in mat:
    if i == "landmark_points_array_mask":
        # plt.imshow(mat[i])
        # plt.axis('off')
        
        # plt.savefig("../../../Face-Augmentation/images/santa.png", bbox_inches='tight', pad_inches=0)

        x_coords = mat[i][0][0][0]
        y_coords = mat[i][0][0][1]

        coords = []
        for i in range(len(x_coords)):
            coords.append([x_coords[i], y_coords[i]])

        print(coords)
        

        plt.imshow(mat['Imask'])
        plt.scatter(x_coords, y_coords, color='red', marker='.')
        plt.show()


