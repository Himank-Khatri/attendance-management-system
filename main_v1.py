import tkinter as tk
from tkinter import ttk 
from tkinter import filedialog
import pickle
import os
from datetime import datetime
import csv


main = tk.Tk()
main.geometry('600x400')
main.resizable(False,False)

try:
	with open('wizarddata.bin', 'rb') as f:
		data_dict = pickle.load(f)
		first_launch = data_dict['first_launch']
		f.close()
except:
	with open('wizarddata.bin', 'wb') as f:
		data_dict = {'first_launch':True, 'students':[],'data_dir_changed':False, 'data_dir':''}
		pickle.dump(data_dict, f)
		first_launch = True


def main_app_format():

	date = tk.StringVar()
	date.set(datetime.now().strftime("%d-%m-%y"))

	data_dir = tk.StringVar()
	if data_dict['data_dir_changed'] == False:
		data_dict['data_dir'] = os.getcwd()
		data_dir.set(os.getcwd())

	def change_dir_func():
		selected_dir = filedialog.askdirectory()
		data_dir.set(selected_dir)
		data_dict['data_dir'] = selected_dir


	head_frame_main = ttk.Frame(main)
	head_frame_main.grid(row=0, column=0, padx=(20,528), pady=20)

	data_dir_label = ttk.Label(head_frame_main, text='Current Data Directory:')
	data_dir_label.grid(row=0, column=0, padx=(0,10), sticky='w')

	data_dir_field = ttk.Label(head_frame_main, textvariable=data_dir)
	data_dir_field.grid(row=0, column=1, padx=(0, 20))

	change_dir_button = ttk.Button(head_frame_main, text='Change', command=change_dir_func)
	change_dir_button.grid(row=0, column=2, padx=(0, 0))


	date_label = ttk.Label(head_frame_main, text='Date (DD-MM-YY): ')
	date_label.grid(row=1, column=0, sticky='w', pady=(5,0))

	date_field = tk.Label(head_frame_main, textvariable=date)
	date_field.grid(row=1, column=1, sticky='w', pady=(5,0))


	total_students_label = ttk.Label(head_frame_main, text='Total Students:')
	total_students_label.grid(row=2, column=0, sticky='w', pady=(5,0))

	total_students_label = ttk.Label(head_frame_main, text=f"{len(data_dict['students'])}")
	total_students_label.grid(row=2, column=1, sticky='w', pady=(5,0))


	average_attendance_label = ttk.Label(head_frame_main, text='Average Attendance: ')
	average_attendance_label.grid(row=3, column=0, sticky='w', pady=(5,0))

	average_attendance_field = ttk.Label(head_frame_main, text='')
	average_attendance_field.grid(row=3, column=1, sticky='w', pady=(5,0))


	main_app_separator = ttk.Separator(main, orient='horizontal')
	main_app_separator.grid(row=1, sticky='ew')


if first_launch != True:

	student_added = tk.StringVar()
	combo_values = data_dict['students']

	def add_students():
		
		entry_mode = tk.StringVar()
		csv_file = tk.StringVar()
		csv_file.set('') #"Upload a .csv file with all the student name at once"

		root = tk.Toplevel()
		root.geometry('380x440')
		root.resizable(False,False)

		def erase_data():

			def yes_delete():

				if len(combo_values)!=0:
					combo_values.pop()
					students_combobox['values'] = combo_values
					root.destroy()


			root = tk.Toplevel()
			root.geometry('450x120')
			root.resizable(False,False)

			caution_label = ttk.Label(root, text='Are you sure you want to delete the last name?')
			caution_label.grid(padx=80, pady=20, sticky='ew')

			butt_frame = ttk.Frame(root)
			butt_frame.grid(row=1, columnspan=2,sticky='ew')

			yes_button = ttk.Button(butt_frame, text='Yes', command=yes_delete)
			yes_button.grid(row=0, column=0, padx=(115,0))

			cancel_button = ttk.Button(butt_frame, text='Cancel', command=root.destroy)
			cancel_button.grid(row=0, column=1, padx=46)	

			root.mainloop()


		def upload():
			filepath = filedialog.askopenfilename(
	                                          title = "Select a File",
	                                          filetypes = (("CSV files","*.csv*"),
	                                                       ("Excel FIles","*.xlsx*"),
	                                                       ("Text files","*.txt*")))

			csv_file.set(filepath.split('/')[-1])

			with open(filepath, 'r') as f:

				file_contents = csv.reader(f)
				data_dict['students'] = data_dict['students'].extend(list([i for i in file_contents][0]))

				combo_values.extend(list([i for i in file_contents]))
				students_combobox['values'] = combo_values


		def done():

			def proceed():
				data_dict['first_launch'] = False
				data_dict['students'] = combo_values

				with open('wizarddata.bin', 'wb') as f:
					pickle.dump(data_dict, f)

				add_students_button.grid_forget()
				head_separator.grid_forget()
				intro_info.grid_forget()

				main_app_format()
				done_root.destroy()
				root.destroy()

			done_root = tk.Toplevel()
			done_root.geometry('450x120')
			done_root.resizable(False,False)

			caution_label = ttk.Label(done_root, text='Are you sure you are done adding students? ')
			caution_label.grid(padx=80, pady=20, sticky='ew')

			butt_frame = ttk.Frame(done_root)
			butt_frame.grid(row=1, columnspan=2,sticky='ew')

			yes_button = ttk.Button(butt_frame, text='Yes', command=proceed)
			yes_button.grid(row=0, column=0, padx=(115,0))

			cancel_button = ttk.Button(butt_frame, text='Cancel', command=done_root.destroy)
			cancel_button.grid(row=0, column=1, padx=46)

			
		def bulk_disable():
			if entry_mode.get() == 'manual':
				upload_button.state(["disabled"])

				student_entry.state(["!disabled"])
				add_button.state(["!disabled"])
				erase_button.state(["!disabled"])
				students_combobox.state(["!disabled"])


		def manual_disable():
			if entry_mode.get() == 'bulk':
				student_entry.state(["disabled"])
				add_button.state(["disabled"])
				erase_button.state(["disabled"])
				students_combobox.state(["disabled"])
				upload_button.state(['!disabled'])

		def add_student_to_list():

			if student_added.get().strip() != '':
				global combo_values
				combo_values.append(student_added.get())
				students_combobox['values'] = combo_values
				student_added.set('')

		manual_frame = ttk.Frame(root)
		manual_frame.grid(padx=10, pady=10)

		manual_radio_frame = ttk.Frame(manual_frame)
		manual_radio_frame.grid(columnspan=2, sticky='ew')

		manual_radio = ttk.Radiobutton(manual_radio_frame, text='Manual Entry', variable=entry_mode, value='manual', command=bulk_disable)
		manual_radio.grid(row=0, column=0, padx=10, pady=(10,0))

		add_label = ttk.Label(manual_frame, text='Add:')
		add_label.grid(row=1, column=0, pady=15, padx=15)

		student_entry = ttk.Entry(manual_frame, textvariable=student_added, width=20)
		student_entry.grid(row=1, column=1, pady=15, padx=(0,15))

		add_button = ttk.Button(manual_frame, text='Add', command=add_student_to_list)
		add_button.grid(row=1, column=2, pady=15, padx=(0,20))

		manual_note = ttk.Label(manual_frame, text='Enter the name and press the add button.')
		manual_note.grid(row=2, padx=(45,0), sticky='ew', columnspan=3)

		students_combobox = ttk.Combobox(manual_frame, values=combo_values, state='readonly', width=16)
		students_combobox.set('Students Added')
		students_combobox.grid(row=3, columnspan=3, column=0, sticky='w', padx=(45,0))

		erase_button = ttk.Button(manual_frame, text='Erase last name', command=erase_data)
		erase_button.grid(row=3, sticky='e', columnspan=3, column=1, pady=10, padx=(0,30))




		manual_separator = ttk.Separator(root, orient='horizontal')
		manual_separator.grid(row=1, sticky='ew')


		bulk_frame = tk.Frame(root)
		bulk_frame.grid(row=3, padx=20, pady=20, columnspan=2, sticky='ew')

		bulk_radio = ttk.Radiobutton(bulk_frame, text='Bulk Entry', variable=entry_mode, value='bulk', command=manual_disable)
		bulk_radio.grid(row=1, column=0, columnspan=2, sticky='w')

		upload_button = ttk.Button(bulk_frame, text='Upload CSV file', command=upload)
		upload_button.state(["disabled"])
		upload_button.grid(row=2, column=2, columnspan=2, pady=20, padx=(24,0))

		bulk_note = ttk.Label(bulk_frame, textvariable=csv_file)
		bulk_note.grid(row=3, column=2, columnspan=2)


		bulk_separator = ttk.Separator(root, orient='horizontal')
		bulk_separator.grid(row=4, sticky='ew')


		done_button = ttk.Button(root, text='Done', command=done)
		done_button.grid(row=5, pady=30)

		root.mainloop()

	add_students_button = ttk.Button(main, text='+ Add Students', command=add_students)
	add_students_button.grid(row=0, padx=250, pady=30) #pack(side='top', expand='false', fill='none', padx=240, pady=30)

	head_separator = ttk.Separator(main, orient='horizontal')
	head_separator.grid(row=1, sticky='ew')

	intro_info = ttk.Label(main, text='Welcome to Attendance Wizard!')
	intro_info.grid(row=2, padx=200, pady=140) #pack(expand='true', fill='none')

else:
	main_app_format()

print(data_dict)

main.mainloop()

print(data_dict)