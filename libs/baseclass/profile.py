from kivy.core.window import Window 
Window.softinput_mode = 'below_target'
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
from Modules.db import collection
import io
from PIL import Image
from kivymd.uix.snackbar import Snackbar
from kivymd.toast import toast





class Profile(Screen):	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_keyboard=self.events)
		self.manager_open = False
		self.file_manager = MDFileManager(exit_manager=self.exit_manager,select_path=self.select_path,preview=True,)
	def file_manager_open(self):
		self.file_manager.show('/storage/emulated/0/')  # output manager to the screen
		self.manager_open = True		
	def select_path(self, path):
		self.exit_manager(path)
	def exit_manager(self, *args):
		self.manager_open = False
		with open("Modules//loginfo.txt","r") as f:
			logged = f.read().split(",")
		self.upload_image_details = [logged[7],args[0]]
		#self.upload_profile_photo(logged[7],args[0])
		self.file_manager.close()
		self.upload_profile_photo(self.upload_image_details[0],self.upload_image_details[1])
	def events(self, instance, keyboard, keycode, text, modifiers):
		if keyboard in (1001, 27):
			if self.manager_open:
				self.file_manager.back()
		return True
	def upload_profile_photo(self,enrollment,path):
		im = Image.open(path)
		image_bytes = io.BytesIO()
		im.save(image_bytes, format='PNG')
		try:
			collection.update_one({"Enrollment":enrollment},{"$set":{'ProfileImage': image_bytes.getvalue()}})
			self.get_Profile_image(enrollment)
		except Exception as e:
			print(e)
	def get_Profile_image(self,enrollment_no,path="./profile.png"):
		image = collection.find_one({"Enrollment":enrollment_no})
		pil_img = Image.open(io.BytesIO(image['ProfileImage']))
		profile_path = path
		pil_img.save(profile_path)
	def text_to_edit(self):
		self.ids.name_field.disabled = False
		self.ids.class_field.disabled = False
		self.ids.contact_field.disabled = False
		self.ids.email_field.disabled = False
		self.ids.name_field.icon_right = "pencil"
		self.ids.class_field.icon_right = "pencil"
		self.ids.contact_field.icon_right = "pencil"
		self.ids.email_field.icon_right = "pencil"
		self.ids.name_field.helper_text = "Your name"
		self.ids.class_field.helper_text = "Your class(write only integer. i.e 12)"
		self.ids.contact_field.helper_text= "Your phone no"
		self.ids.email_field.helper_text = "Your email"
		self.ids.camera.icon = "camera"
	def save_to_edit(self,Name,Class,Phone,Email):
		
		self.ids.name_field.disabled = True
		self.ids.class_field.disabled = True
		self.ids.contact_field.disabled = True
		self.ids.email_field.disabled = True
		self.manager.get_screen("Home").ids.Nlabel.text = Name.text
		self.ids.camera.icon = ""
		self.ids.name_field.icon_right = ""
		self.ids.class_field.icon_right = ""
		self.ids.contact_field.icon_right = ""
		self.ids.email_field.icon_right = ""
		self.ids.name_field.text = Name.text
		self.ids.class_field.text = Class.text
		self.ids.contact_field.text = Phone.text	
		self.ids.email_field.text = Email.text
		with open("Modules//loginfo.txt","r") as f:
			data = f.read().split(",")
		role = data[1]
		sec = data[4]
		phone = data[5]
		enrollment = data[7]
		query = {"Enrollment":data[7]}
		update_values = {"$set" : {"Username":Name.text,"Class":Class.text,"Phone":Phone.text,"Email":Email.text}}
		try:
			collection.update_one(query,update_values)
			User = Name.text
			Class = Class.text
			Phone = Phone.text
			Email = Email.text
			Sec = sec
			Role = role
			Phone = phone
			Enrollment_no = enrollment
			with open("Modules//loginfo.txt","w+") as f:
				f.write(f"logged,{Role},{User},{Class},{Sec},{Phone},{Email},{Enrollment_no}")
			toast(text="updated successfully",gravity=80)
			self.ids.pro_label.text = ""
		except Exception as e:
			a = Snackbar(text="Oops !  something wents wrong unable to update profile.")
			a.open()
			self.ids.pro_label.text = ""