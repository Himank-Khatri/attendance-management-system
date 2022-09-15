import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import filedialog
import pickle
import csv
from datetime import datetime
import pandas as pd

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


main = tk.Tk()

main.geometry(f'600x400')
main.title("Attendance Wizard")
main.resizable(False,False)

working_dir = r'D:\Python\project\data.bin'

try: 
    with open(working_dir, 'rb') as f:
        data_dictionary = pickle.load(f)    
        first_launch = data_dictionary['first_launch']

except:
    with open(working_dir, 'wb') as f:
        data_dictionary = {'first_launch':True, 'students':{}}
        pickle.dump(data_dictionary, f)
        first_launch = True

name_index = 0


def main_app_format():
    current_working_class = None
    current_working_section = None

    myFont = tkFont.Font(size=12)

    class_strength = tk.StringVar()
    class_strength.set('None')
    
    selected_section = tk.StringVar() 
    
    def select_class():

        def change_class():
            section_optionmenu.place_forget()
            select_class_button = ttk.Button(main, text='Select', command=select_class, width=7)
            select_class_button.place(x=130, y=20)


        def select_section():

            def change_section():
                select_class_button.place_forget()

                select_section_button = ttk.Button(main, text='Select', command=select_section, width=7)
                select_section_button.place(x=240, y=20)

            global current_working_class
            global current_working_section

            current_working_class = selected_class.get()
            current_working_section = selected_section.get()
            class_strength.set(len(data_dictionary['students'][f'{current_working_class}'][f'{current_working_section}']))

            change_section_button = ttk.Button(main, text='Change', command=change_section, width=7)
            change_section_button.place(x=240, y=20)
            
            print(current_working_class)
            print(current_working_section)
            

        select_class_button.place_forget()

        section_options = list(data_dictionary['students'][f'{selected_class.get()}'].keys())


        change_class_button = ttk.Button(main, text='Change', command=change_class, width=7)
        change_class_button.place(x=130, y=20)

        section_optionmenu = ttk.OptionMenu(main, selected_section, section_options[0], *section_options)
        section_optionmenu.place(x=190, y=20)

        select_section_button = ttk.Button(main, text='Select', command=select_section, width=7)
        select_section_button.place(x=240, y=20)



    today_date = datetime.now().strftime("%d-%m-%y")
    class_strength = tk.StringVar()
    class_strength.set('None')
    # len(data_dictionary['students'][f'{current_working_class}'][f'{current_working_section}'])



    class_options = list(data_dictionary['students'].keys())
    selected_class = tk.StringVar()


    class_label = ttk.Label(main, text='Class:', width=12, font=myFont)
    class_label.place(x=30, y=20)

    class_optionmenu = ttk.OptionMenu(main, selected_class, class_options[0], *class_options)
    class_optionmenu.place(x=80, y=20)

    select_class_button = ttk.Button(main, text='Select', command=select_class, width=7)
    select_class_button.place(x=130, y=20)


    date_label = ttk.Label(main, text='Date: ', font=myFont)
    date_label.place(x=30, y=55)

    date_field = ttk.Label(main, text=today_date, font=myFont)
    date_field.place(x=80, y=55)


    total_students_label = ttk.Label(main, text='Total students:', font=myFont)
    total_students_label.place(x=30, y=90)

    total_students_feild = ttk.Label(main, textvariable=class_strength, font=myFont)
    total_students_feild.place(x=140, y=90)

    

    def start_attendance():

        

        start_attendance_button.place_forget()

        curr_class_list = data_dictionary['students'][f'{selected_class.get()}'][f'{selected_section.get()}']
        curr_student = tk.StringVar()
        curr_student.set(f'{curr_class_list[name_index]}:')

        student_name_label = tk.Label(main, textvariable=curr_student, font=myFont)
        student_name_label.place(x=180, y=188)

        attendance_list = []
        def mark_present():

            global name_index

            attendance_list.append('Present')        

            name_index += 1  
            print(name_index)     
            if name_index < int(class_strength.get()):
                curr_student.set(f'{curr_class_list[name_index]}:')


            else:
                student_name_label.place_forget()
                present_button.place_forget()
                absent_button.place_forget()
                print(attendance_list)
                save_att.place(x=250, y=188)



        present_button = ttk.Button(main, text='Present', command=mark_present)
        present_button.place(x=260, y=188)


        def mark_absent():

            global name_index

            attendance_list.append('Absent')

            name_index += 1  
            print(name_index)     
            if name_index < int(class_strength.get()):
                curr_student.set(f'{curr_class_list[name_index]}:')
                

            else:
                student_name_label.place_forget()
                present_button.place_forget()
                absent_button.place_forget()
                print(attendance_list)
                save_att.place(x=250, y=188)
            

        absent_button = ttk.Button(main, text='Absent', command=mark_absent)
        absent_button.place(x=340, y=188)

        def save_att():

            try:
                df = pd.read_csv(f'{selected_class.get()}-{selected_section.get()}')
                df[today_date] = attendance_list
                print('tried,\n',df)
                df.to_csv(f'{selected_class.get()}-{selected_section.get()}')

            except:
                df = pd.DataFrame(curr_class_list)
                df[today_date] = attendance_list
                print('except,\n',df)
                df.to_csv(f'{selected_class.get()}-{selected_section.get()}')

            save_att.place_forget()


        save_att = ttk.Button(main, text='Save', command=save_att)



    start_attendance_button = ttk.Button(main, text='Start Attendance', width=20, command=start_attendance)
    start_attendance_button.place(x=233, y=188)


    # ttk.Separator(main, orient='horizontal').place(rely=0, relwidth=1)
    # ttk.Separator(main, orient='vertical').place(relx=0.5, relheight=1)
    # ttk.Separator(main, orient='horizontal').place(rely=0.5, relwidth=1)
    # ttk.Separator(main, orient='vertical').place(relx=0.33, relheight=1)
    # ttk.Separator(main, orient='vertical').place(relx=0.66, relheight=1)
    # ttk.Separator(main, orient='vertical').place(relx=0.25, relheight=1)
    # ttk.Separator(main, orient='vertical').place(relx=0.75, relheight=1)



if first_launch:

    def add_classroom():

        def add_students():

            def manul_add_student():
                currrent_student = manual_student_added.get()
                data_dictionary['students'][f'{curr_class.get()}'][f'{curr_section.get()}'].append(currrent_student)
                print(data_dictionary)
                manual_student_added.set('')


            def bulk_upload():
                filepath = filedialog.askopenfilename(
                                                  title = "Select a File",
                                                  filetypes = (("CSV files","*.csv*"),
                                                               ("Excel FIles","*.xlsx*"),
                                                               ("Text files","*.txt*")))

                bulk_info_var.set(f"Current File: {filepath.split('/')[-1]}")
                bulk_info_label.place(x=80, y=90)


                with open(filepath, 'r') as f:

                    file_contents = csv.reader(f)
                    data_dictionary['students'][f'{curr_class.get()}'][f'{curr_section.get()}'] = list(file_contents)[0]
                
                print(data_dictionary)


            def done_button():

                def yes_fun():
                    warning_window.destroy()
                    data_dictionary['first_launch'] = False
                    with open(working_dir, 'wb') as f:
                        pickle.dump(data_dictionary, f)

                    root.destroy()
                    classroom_root.destroy()

                    get_started_button.place_forget()
                    mainpage_separator.place_forget()

                    main_app_format()  

                def add_another_fun():
                    warning_window.destroy()
                    root.destroy()
                    add_classroom()

                warning_window = tk.Toplevel()
                warning_window.geometry('400x150')

                done_label = ttk.Label(warning_window, text='Are you sure you want to exit to the main app?', font=tkFont.Font(size=11))
                done_label.place(x=45, y=30)

                yes_button = ttk.Button(warning_window, text='Yes', command=yes_fun, width=6)
                yes_button.place(x=60, y=70)

                add_another = ttk.Button(warning_window, text='Add another classroom', command=add_another_fun)
                add_another.place(x=120, y=70)

                no_button = ttk.Button(warning_window, text='No', command=warning_window.destroy, width=6)
                no_button.place(x=270, y=70)


                warning_window.mainloop()


            if curr_class.get() == '' or curr_section.get() == '':
                classroom_creation_status.set('Please enter the above information')
            else:
                classroom_root.destroy()


                if curr_class.get() in data_dictionary['students'].keys():
                    data_dictionary['students'][f'{curr_class.get()}'].update({f'{curr_section.get()}':[]})
                else:
                    data_dictionary['students'][f'{curr_class.get()}'] = {f'{curr_section.get()}':[]}


                root = tk.Toplevel()
                root.geometry('380x230')
                root.title(f'{curr_class.get()}-{curr_section.get()}1')
                myFont = tkFont.Font(size=14)

                manual_student_added = tk.StringVar()
                manual_info_var = tk.StringVar()
                manual_info_var.set('Enter the name and press add button.')

                bulk_info_var = tk.StringVar()
                bulk_info_var.set('Upload a CSV file.')

                tabs_section = ttk.Notebook(root)

                manual_tab = ttk.Frame(tabs_section)
                bulk_tab = ttk.Frame(tabs_section)

                tabs_section.add(manual_tab, text='Manual Entry')
                tabs_section.add(bulk_tab, text='Bulk Entry')

                tabs_section.place(relwidth=0.95, relheight=0.975, relx=0.025, rely=0.0125)

                manual_add_label = ttk.Label(manual_tab, text='Add:', font=myFont)
                manual_add_label.place(x=30, y=40)

                manual_student_entry = ttk.Entry(manual_tab, font=myFont, width=14, textvariable=manual_student_added)
                manual_student_entry.place(x=85, y=40)

                manual_student_add_button = ttk.Button(manual_tab, text='Add', command=manul_add_student)
                manual_student_add_button.place(x=250, y=40)

                manual_info_label = ttk.Label(manual_tab, textvariable=manual_info_var, font=tkFont.Font(size=11))
                manual_info_label.place(x=55, y=85)

                manual_done_button = ttk.Button(manual_tab, text='Done', command=done_button)
                manual_done_button.place(x=130, y=135)

                bulk_done_button = ttk.Button(bulk_tab, text='Done', command=done_button)
                bulk_done_button.place(x=130, y=135)


                bulk_upload_button = ttk.Button(bulk_tab, text='Upload', command=bulk_upload)
                bulk_upload_button.place(x=140, y=45)

                bulk_info_label = ttk.Label(bulk_tab, textvariable=bulk_info_var, font=tkFont.Font(size=11))
                bulk_info_label.place(x=130, y=90)



                # ttk.Separator(bulk_tab, orient='horizontal').place(rely=0, relwidth=1)
                # ttk.Separator(bulk_tab, orient='vertical').place(relx=0.5, relheight=1)
                # ttk.Separator(bulk_tab, orient='horizontal').place(rely=0.5, relwidth=1)
                # ttk.Separator(bulk_tab, orient='vertical').place(relx=0.33, relheight=1)
                # ttk.Separator(bulk_tab, orient='vertical').place(relx=0.66, relheight=1)


                root.mainloop()

        
        classroom_root = tk.Toplevel(main)
        classroom_root.geometry('400x230')

        myFont = tkFont.Font(size=20)

        # ttk.Separator(classroom_root, orient='horizontal').place(rely=0, relwidth=1)
        # ttk.Separator(classroom_root, orient='vertical').place(relx=0.5, relheight=1)
        # ttk.Separator(classroom_root, orient='horizontal').place(rely=0.5, relwidth=1)
        # ttk.Separator(classroom_root, orient='vertical').place(relx=0.33, relheight=1)
        # ttk.Separator(classroom_root, orient='vertical').place(relx=0.66, relheight=1)

        curr_class = tk.StringVar()
        curr_section = tk.StringVar()
        classroom_creation_status = tk.StringVar()
        classroom_creation_status.set('')

        class_label = ttk.Label(classroom_root, font=myFont, text='Class:')
        class_label.place(x=75, y=25)

        class_entry = ttk.Entry(classroom_root, font=myFont, width=10, textvariable=curr_class)
        class_entry.place(x=160, y=25)

        section_label = ttk.Label(classroom_root, font=myFont, text='Section:')
        section_label.place(x=95, y=90)

        section_entry = ttk.Entry(classroom_root, font=myFont, width=6, textvariable=curr_section)
        section_entry.place(x=205, y=90)

        create_classroom_button = ttk.Button(classroom_root, width=30, text='Create Classroom', command=add_students)
        create_classroom_button.place(x=105, y=150)

        classroom_created_label = ttk.Label(classroom_root, textvariable=classroom_creation_status)
        classroom_created_label.place(x=106, y=190)

        separator_one = ttk.Separator(classroom_root, orient='horizontal')


        classroom_root.mainloop()

    get_started_button = ttk.Button(main, text='Get Started', command=add_classroom)
    get_started_button.place(x=260, y=44)

    mainpage_separator = ttk.Separator(main, orient='horizontal')
    mainpage_separator.place(y=110, relwidth=0.95, relx=0.025)

    # ttk.Separator(main, orient='horizontal').place(rely=0, relwidth=1)
    # ttk.Separator(main, orient='vertical').place(relx=0.5, relheight=1)
    # ttk.Separator(main, orient='horizontal').place(rely=0.5, relwidth=1)

else:
    main_app_format()

main.mainloop()

print(data_dictionary)
