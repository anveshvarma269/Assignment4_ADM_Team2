import streamlit as st
import pickle
import cv2
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import manifold
import scipy as sc

class StreamlitApp:

	# @st.cache
	def __init__(self):
		self.image_style_embeddings = pickle.load(open("image_style_embeddings_subset.pickle","rb"))
		self.images = pickle.load(open("images.pickle","rb"))

		print(len(self.image_style_embeddings))
		print(len(self.images))


	@st.cache
	def load_image(self,image_file):
		img = Image.open(image_file)
		return img



	def search_by_style(self, reference_image, max_results):
		v0 = self.image_style_embeddings[reference_image]
		distances = {}
		for k,v in self.image_style_embeddings.items():
			d = sc.spatial.distance.cosine(v0, v)
			distances[k] = d

		sorted_neighbors = sorted(distances.items(), key=lambda x: x[1], reverse=False)
		print("sorted_neighbors ===",sorted_neighbors)
		# f, ax = plt.subplots(1, max_results, figsize=(16, 8))
		# for i, img in enumerate(sorted_neighbors[:max_results]):
		#     ax[i].imshow(images[img[0]])
		#     ax[i].set_axis_off()
		st.subheader("Similar Products you may want to buy")
		for i, img in enumerate(sorted_neighbors[:max_results]):

			st.image(self.images[img[0]], width=100)

	

	def asearch(self):
		st.title("Artistic Style Similarity Search Method")
		st.write("-------------------------------------------------------------------------------------------------")

		
		st.subheader("Upload an query image... : ")
		image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
		k = st.slider('How many similar images do you want to see?', 1, 10, 1)
		

		st.write("K value selected ===>"+str(k))
		if image_file is not None:

			# To See details
			file_details = {"filename":image_file.name, "filetype":image_file.type,
						  "filesize":image_file.size}
			st.write(file_details)
			img = self.load_image(image_file)
			# To View Uploaded Image
			st.image(img,width=250)
			self.search_by_style(image_file.name, k)


if __name__ == "__main__":
	
	obj  = StreamlitApp()
	# obj.load_embeddings()
	obj.asearch()