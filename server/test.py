import classifier

classifier.load_model()

with open("./test_images/b64_courteney.txt") as file:
            image_data = file.read()


response = classifier.classify_image(image_data, None)

print(response)