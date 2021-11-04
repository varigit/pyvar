from pyvar.ml.dataset.mnist import train_mnist_digit

foo = train_mnist_digit()

with open('mnist_digit.tflite', "wb") as model_file:
    model_file.write(foo[0])
    model_file.close()

print(f"Test loss: {foo[1]}")
print(f"Test accuracy: {foo[2]}")
