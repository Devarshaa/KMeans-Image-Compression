from matplotlib import pyplot
import numpy
from PIL import Image
from os.path import splitext
import warnings

warnings.filterwarnings("ignore")
#Image to Array
def imgToArr(imageFileName):
    # image = Image.open(imageFileName)
    # return numpy.asarray(image)
    return pyplot.imread(imageFileName)

#Array to Image
def arrToImg(compressedImage):
    return Image.fromarray(compressedImage)

#Distance between 2 points in 3D(R, G, B) space
def distance3D(p1, p2):
    num = 0
    for i in range(3):
        num += pow(p1[i] - p2[i], 2)
    return numpy.sqrt(num)

#returns the cluster/ mean the point p belongs to
def bestMean(p, means):
    bestM = -1
    leastDistance = float("inf")
    for mean in means.keys():
        dist = distance3D(p, means[mean])
        if dist < leastDistance:
            leastDistance = dist
            bestM = mean
    return bestM

#Returns a 2d list with each item representing the cluster the corresponding pixel from the image belongs to
def cluster(image, means):
    rows = len(image)
    cols = len(image[0])
    clusters = []
    for row in range(rows):
        clusters.append([])
        for col in range(cols):
            pixel = image[row][col]
            clusters[row].append(bestMean(pixel, means))
    return clusters

#Returns new means dictionary for the new clusters
def newMeans(image, clusters, k):
    means = {i:[0,0,0] for i in range(1, k+1)}
    counts = [0 for _ in range(k + 1)]
    rows = len(clusters)
    cols = len(clusters[0])
    for row in range(rows):
        for col in range(cols):
            cluster = clusters[row][col]
            pixel = image[row][col]
            for c in range(3):
                means[cluster][c] += pixel[c]
            counts[cluster] += 1
    for mean in means.keys():
        if counts[mean] != 0:
            for i in range(3):
                means[mean][i] //= counts[mean]
    return means

#Returns compressed image pixel list
def kMeansCompression(image, k):
    #print(image[0], len(image))
    means = {i:image[0][i] for i in range(1, k+1)}
    iterations = int(input("Enter the Number of Iterations:"))
    for iteration in range(iterations):
        #print(iteration)
        clusters = cluster(image, means)
        means = newMeans(image, clusters, k)
    rows = len(clusters)
    cols = len(clusters[0])
    for row in range(rows):
        for col in range(cols):
            clusters[row][col] = means[clusters[row][col]]
    #print(clusters, means)
    return clusters

imageFileName = input("Enter the image to compress : ")
k = int(input("Enter the number of Colors(Clusters):"))
image = imgToArr(imageFileName)
compressed_image = kMeansCompression(image, k)
imgFile, extension = splitext(imageFileName)
compressed_image = numpy.array(compressed_image, dtype=numpy.uint8)
cImage = arrToImg(compressed_image)
iName = imgFile + str(k) + extension
cImage.save(iName)


