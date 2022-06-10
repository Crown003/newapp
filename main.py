from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window 
Window.softinput_mode = 'below_target'
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.toast import toast
from kivymd_extensions.akivymd.uix.badgelayout import AKBadgeLayout
from kivymd_extensions.akivymd.uix.charts import AKBarChart
from libs.Widget.sqrCard import Icons
from Modules.db import download_file,collection
from libs.root import Root
import threading
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image, CoreImage
import io
from PIL import Image

User_obj = ""
######
User = ""
Class = ""
Phone = ""
Email = ""
######

class Main(MDApp):
		data_updated = "0"
		profile_flag = "0"
		image = "assets/vidiya.png"	
		Username = f""
		User_profile = f""
		if User_profile == "":
			User_profile = f"assets/noprofile.png"
		else:
			pass
		UserClass = f""
		UserEmail = f""
		UserPhone = f""
		def build(self):
			self.theme_cls.primary_palette = "Pink"
			self.root = Root()
			self.root.load_screen("Home")
			self.root.load_screen("Profile")
		def on_start(self):
			try:
				with open("Modules//loginfo.txt","r+") as f:
					logged = f.read().split(",")
				if logged[0] == "logged" and logged[1].upper() == "STUDENT":
						#"Some error unable to load profile image...error for main.py")
					self.data_update()
					self.root.current = "Home"
				elif logged[0] == "logged" and logged[1].upper() == "TEACHER":
					self.root.set_current("Teachers_interface")
				else:
					self.root.load_screen("Teachers_interface")
					self.root.set_current("LoginPage")
			except FileNotFoundError:
				with open("Modules//loginfo.txt","x") as f:
					pass
				self.root.load_screen("Teachers_interface")
				self.root.set_current("LoginPage")			
		def data_update(self):	
			try:	
				with open("Modules//loginfo.txt","r+") as f:
					check = f.read().split(",")
					self.get_Profile_image(check[7],"./profile.png")
			except Exception as e:
				print("error from main data_update: ",e)
			try:
				Status,Role,name,class_,sec,phone,email,*args= check
				self.root.get_screen("Home").ids.Nlabel.text = name
				self.root.get_screen("Home").ids.Clabel.text = class_ + sec
				self.root.get_screen("Home").ids.main_page_profile.source = "./profile.png"
				#below changing the profile details
				self.root.get_screen("Profile").ids.name_field.text = name
				self.root.get_screen("Profile").ids.class_field.text = class_
				self.root.get_screen("Profile").ids.contact_field.text = phone
				self.root.get_screen("Profile").ids.email_field.text = email
				self.root.get_screen("Profile").ids.profile_image.source = "./profile.png"		
				self.data_updated = "1"
				self.reload_home_image()
			except Exception as e:
				print("from main",e)
		def show_dialog(self,*args):
			self.a = MDDialog(title="Logout of svm app ?",size_hint=(.9,.7),type="confirmation",buttons=[MDFlatButton(text="CANCEL",on_release=self.close_dialog_logout), MDRaisedButton(text="Log out",on_release=self.logout)])
			self.a.open()
		def close_dialog_logout(self,*args):
			self.a.dismiss()
		def show_About(self):
			print(self.root.screen_names)
			self.root.set_current("About_School")
		def show_user_profile(self,hit_from):
			if hit_from == "account":
				self.root.set_current("Profile")
				self.profile_flag = "RecordArea"
			elif hit_from == "settings":
				self.root.set_current("Profile")
				self.profile_flag = "Settings"
			elif hit_from == "account-circle":
				self.profile_flag = "nav"
				self.root.set_current("Profile")
			else:
				pass
		def back(self):
			if self.profile_flag == "nav":
				self.root.transition.direction = "right"
				self.root.current = "Home"
			elif self.profile_flag == "RecordArea":
				self.root.transition.direction = "right"
				self.root.current = "RecordArea"
			elif self.profile_flag == "Settings":
				self.root.transition.direction = "right"
				self.root.current = "Settings"
			else:
				pass
		def reload_home_image(self):
			self.root.get_screen("Home").ids.main_page_profile.reload()
			self.root.get_screen("Profile").ids.profile_image.reload()
		def get_Profile_image(self,enrollment_no,path):
			image = collection.find_one({"Enrollment":enrollment_no})
			pil_img = Image.open(io.BytesIO(image['ProfileImage']))
			profile_path = path
			pil_img.save(profile_path)		
		def main_down_file(self,name_of_file):
			threading.Thread(target=self.download_main_file(name_of_file)).start()
		def download_main_file(self,name_of_file):
			toast("dowloading file.")
			print("downloading: ",name_of_file)
			#download_file(name_of_file)
			toast("Dowloaded successfully.")		
		def logout(self,*args):
			self.data_updated = "0"
			with open("Modules//loginfo.txt","w") as f:
				f.write("loggedout")
			self.root.set_current("LoginPage")
			if "Teacher" not in User:
				self.close_dialog_logout()
			else:
				pass
		
	
if __name__ == "__main__":
	Main().run()
