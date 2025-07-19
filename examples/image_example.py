from PIL import Image
import matplotlib.pyplot as plt

def image_proc():
    img = Image.new("RGB", (50,50), color="blue")
    img.save("blue.png")
    plt.plot([0,1,2],[0,1,0])
    plt.savefig("plot.png")
    print("Images created")

if __name__ == "__main__":
    image_proc()
