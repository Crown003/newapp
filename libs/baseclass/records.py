from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu


unit_one_marks = [15,16,18,20,19]
unit_two_marks = [15,18,18,20,20]
unit_three_marks = [10,16,18,20,20]
student_attendance = 41
total_school_working_day = 88


class RecordArea(Screen):
	stud_attend = student_attendance
	total_school_working_dy = total_school_working_day
	user_attendence_percentage = f"{stud_attend}"
	user_Result_analysis = "A+"
	Xvalues = [1,2,3,4,5]	
	Barlabel = ["Math","Cs","Physic","Chemistry","English"]
	Yvalues = unit_one_marks
	def menu_box(self):
		self.a = self.ids.drop_btn
		self.menu_items = [
			{
			"text": f"Term {i} marks",
			"viewclass": "OneLineListItem",
			"on_release": lambda x=f"Term {i} marks": self.menu_callback(x),
			} for i in range(1,4)
			]
		self.menu = MDDropdownMenu(
			caller=self.a,
			items=self.menu_items,
			position="auto",
			background_color=(.9,.9,.9,1),
			opening_time=0,
			width_mult=4,
			)	
	def menu_callback(self, text_item):	
		def label_creator(data):
			"""creating y labels for bargraph"""
			label = []
			for i in data:
				b = str(i)+"/20"
				label.append(b)
			return label	
		self.menu.dismiss()
		self.ids.graph_title.text = f"{text_item}"
		list_text_item = text_item.split()
		chart_bar = self.ids.chart
		if int(list_text_item[1]) == 1:
			chart_bar.y_labels = label_creator(unit_one_marks)
			chart_bar.y_values = unit_one_marks
			
		elif int(list_text_item[1]) == 2:
			chart_bar.y_labels = label_creator(unit_two_marks)
			chart_bar.y_values = unit_two_marks
		
		elif int(list_text_item[1]) == 3:
			chart_bar.y_labels = label_creator(unit_three_marks)
			chart_bar.y_values = unit_three_marks
		else:
			pass
		chart_bar.update()