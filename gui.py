from tkinter import *
import customtkinter
from PIL import Image
from logic import WatchListManager
from tkinter import messagebox

menu_bgCOLOR = '#756f6a'
menu_button_hoverCOLOR = '#c3bab1'
main_bgCOLOR = '#484746'

class WatchListApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.user = None
        self.manager = WatchListManager()

        self.title('Watchlist Application')
        self.geometry("700x700")

        self.menuframe = Menu_Frame(self)

        self.mainframe = customtkinter.CTkFrame(self, fg_color=main_bgCOLOR)
        self.mainframe.pack(side=RIGHT, fill='both', expand=True)

        self.framelist = [HomePage(self.mainframe), MoviePage(self.mainframe), SeriesPage(self.mainframe), DataBasePage(self.mainframe)]
        for frame in self.framelist:
            frame.pack_forget()

        self.changeWindow(0)  # Show the home page initially

    def changeWindow(self, index):
        for i, frame in enumerate(self.framelist):
            if i == index:
                frame.pack(side=RIGHT, fill='both', expand=True)
            else:
                frame.pack_forget()

    def updateIndicator(self, indicator_label):
        self.menuframe.home_btn_indicator.configure(fg_color=menu_bgCOLOR)
        self.menuframe.movie_btn_indicator.configure(fg_color=menu_bgCOLOR)
        self.menuframe.series_btn_indicator.configure(fg_color=menu_bgCOLOR)
        self.menuframe.db_btn_indicator.configure(fg_color=menu_bgCOLOR)

        indicator_label.configure(fg_color=main_bgCOLOR)


class Menu_Frame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color=menu_bgCOLOR, width=250, corner_radius=10)
        self.pack(side=LEFT, fill='y')

        self.search_icon = customtkinter.CTkImage(light_image=Image.open('TrackWatch/icons/search.png'))
        self.home_icon = customtkinter.CTkImage(light_image=Image.open('TrackWatch/icons/home.png'))
        self.movie_icon = customtkinter.CTkImage(light_image=Image.open('TrackWatch/icons/film.png'))
        self.series_icon = customtkinter.CTkImage(light_image=Image.open('TrackWatch/icons/tv.png'))
        self.settings_icon = customtkinter.CTkImage(light_image=Image.open('TrackWatch/icons/setting.png'))

        self.home_button = customtkinter.CTkButton(self, text='Home', image=self.home_icon, fg_color=menu_bgCOLOR,
                                                   width=240, font=('Tahoma', 20), hover_color=menu_button_hoverCOLOR,
                                                   command=lambda: [parent.changeWindow(0), parent.updateIndicator(self.home_btn_indicator)])
        self.home_button.place(x=4, y=250)
        self.home_btn_indicator = customtkinter.CTkLabel(self, text='', fg_color=menu_bgCOLOR, width=10, height=31)
        self.home_btn_indicator.place(x=3, y=250)

        self.movie_button = customtkinter.CTkButton(self, text='Movie', image=self.movie_icon, fg_color=menu_bgCOLOR,
                                                    width=240, font=('Tahoma', 20), hover_color=menu_button_hoverCOLOR,
                                                    command=lambda: [parent.changeWindow(1), parent.updateIndicator(self.movie_btn_indicator)])
        self.movie_button.place(x=4, y=300)
        self.movie_btn_indicator = customtkinter.CTkLabel(self, text='', fg_color=menu_bgCOLOR, width=10, height=31)
        self.movie_btn_indicator.place(x=3, y=300)

        self.series_button = customtkinter.CTkButton(self, text='Series', image=self.series_icon, fg_color=menu_bgCOLOR,
                                                     width=240, font=('Tahoma', 20), hover_color=menu_button_hoverCOLOR,
                                                     command=lambda: [parent.changeWindow(2), parent.updateIndicator(self.series_btn_indicator)])
        self.series_button.place(x=4, y=350)
        self.series_btn_indicator = customtkinter.CTkLabel(self, text='', fg_color=menu_bgCOLOR, width=10, height=31)
        self.series_btn_indicator.place(x=3, y=350)

        self.db_button = customtkinter.CTkButton(self, text='DataBase', image=self.settings_icon, fg_color=menu_bgCOLOR,
                                                 width=240, font=('Tahoma', 20), hover_color=menu_button_hoverCOLOR,
                                                 command=lambda: [parent.changeWindow(3), parent.updateIndicator(self.db_btn_indicator)])
        self.db_button.place(x=4, y=400)
        self.db_btn_indicator = customtkinter.CTkLabel(self, text='', fg_color=menu_bgCOLOR, width=10, height=31)
        self.db_btn_indicator.place(x=3, y=400)


class HomePage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color=main_bgCOLOR, corner_radius=10)

        customtkinter.CTkLabel(self, text='HOME', font=('Helvetica', 50), text_color=menu_button_hoverCOLOR).pack(pady=30)

class MoviePage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.manager = WatchListManager()

        self.configure(fg_color=main_bgCOLOR, corner_radius=10)
        customtkinter.CTkLabel(self, text='MOVIE', font=('Helvetica', 50), text_color=menu_button_hoverCOLOR).pack(pady=20)

        self.current_selection = None
        self.card_frames = {}  
        self.current_frame = None  

        self.searchFrame = customtkinter.CTkFrame(self, fg_color=main_bgCOLOR, width=560, height=40)
        self.searchFrame.pack(pady=30)

        self.searchTitleENTRY = customtkinter.CTkEntry(self.searchFrame, placeholder_text='Enter Title', width=250, height=30)
        self.searchTitleENTRY.place(x=5, y=5)

        self.searchYearENTRY = customtkinter.CTkEntry(self.searchFrame, placeholder_text='Year (Optional)', width=120, height=30)
        self.searchYearENTRY.place(x=270, y=5)

        self.searchBUTTON = customtkinter.CTkButton(self.searchFrame, text='Search', width=150, height=35, command=self.perform_search)
        self.searchBUTTON.place(x=400, y=3)
        self.searchBUTTON.configure(state=customtkinter.DISABLED)

        self.frames = {}  

        self.switch_frame_buttons = customtkinter.CTkFrame(self, fg_color=main_bgCOLOR, width=800, height=120)
        self.switch_frame_buttons.pack(pady=10)

        self.toWatchBUTTON = customtkinter.CTkButton(self.switch_frame_buttons, fg_color=main_bgCOLOR,
                                                     text='To Watch', width=200, height=35, font=('Bold', 15), hover_color=menu_button_hoverCOLOR,
                                                     command=lambda: self.show_frame("to_watch", self.TWindicator))

        self.toWatchBUTTON.pack(side=customtkinter.LEFT, padx=10)
        self.TWindicator = customtkinter.CTkLabel(self.switch_frame_buttons, fg_color=main_bgCOLOR, text='', width=200)
        self.TWindicator.place(x=10, y=30)

        self.watchedBUTTON = customtkinter.CTkButton(self.switch_frame_buttons, fg_color=main_bgCOLOR,
                                                     text='Watched', width=200, height=35, font=('Bold', 15), hover_color=menu_button_hoverCOLOR,
                                                     command=lambda: self.show_frame("watched", self.WEDindicator))

        self.watchedBUTTON.pack(side=customtkinter.LEFT, padx=10)
        self.WEDindicator = customtkinter.CTkLabel(self.switch_frame_buttons, fg_color=main_bgCOLOR, text='', width=200)
        self.WEDindicator.place(x=231, y=30)

        self.watchingBUTTON = customtkinter.CTkButton(self.switch_frame_buttons, fg_color=main_bgCOLOR,
                                                      text='Watching', width=200, height=35, font=('Bold', 15), hover_color=menu_button_hoverCOLOR,
                                                      command=lambda: self.show_frame("watching", self.WINGindicator))

        self.watchingBUTTON.pack(side=customtkinter.LEFT, padx=10)
        self.WINGindicator = customtkinter.CTkLabel(self.switch_frame_buttons, fg_color=main_bgCOLOR, text='', width=200)
        self.WINGindicator.place(x=452, y=30)

    def perform_search(self):
        title = self.searchTitleENTRY.get()
        year = self.searchYearENTRY.get()
        print(f"Searching for {title} ({year}) under category: {self.current_selection}")

        results = self.manager.run(title, self.current_selection, year)
        if results:
            self.add_card(self.current_frame, results)
        else:
            messagebox.showinfo("Search Result", "No details found.")

    def add_card(self, parent, details):
        card_frame = customtkinter.CTkFrame(parent, fg_color='white')
        card_frame.pack(pady=10)

        for key, value in details.items():
            label = customtkinter.CTkLabel(card_frame, text=f"{key}: {value}")
            label.pack(pady=5)

        if self.current_selection not in self.card_frames:
            self.card_frames[self.current_selection] = []
        self.card_frames[self.current_selection].append(card_frame)

    def hide_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.pack_forget()

    def show_frame(self, selection, indicator):
        self.current_selection = selection
        self.searchBUTTON.configure(state=customtkinter.NORMAL)

        self.TWindicator.configure(fg_color=main_bgCOLOR)
        self.WEDindicator.configure(fg_color=main_bgCOLOR)
        self.WINGindicator.configure(fg_color=main_bgCOLOR)

        indicator.configure(fg_color=menu_bgCOLOR)

        self.hide_current_frame()
        if selection not in self.frames:
            frame = customtkinter.CTkScrollableFrame(self, fg_color=menu_bgCOLOR, height=560, width=1220)
            frame.pack()
            self.frames[selection] = frame
        else:
            frame = self.frames[selection]
            frame.pack()

        self.current_frame = frame

        if selection in self.card_frames:
            for card in self.card_frames[selection]:
                card.pack(pady=10)




class SeriesPage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.manager = WatchListManager()

        self.configure(fg_color=main_bgCOLOR, corner_radius=10)
        customtkinter.CTkLabel(self, text='SERIES', font=('Helvetica', 50), text_color=menu_button_hoverCOLOR).pack(pady=20)

        self.current_selection = None

        self.searchFrame = customtkinter.CTkFrame(self, fg_color=main_bgCOLOR, width=560, height=40)
        self.searchFrame.pack(pady=30)

        self.searchTitleENTRY = customtkinter.CTkEntry(self.searchFrame, placeholder_text='Enter Title', width=250, height=30)
        self.searchTitleENTRY.place(x=5, y=5)

        self.searchYearENTRY = customtkinter.CTkEntry(self.searchFrame, placeholder_text='Year (Optional)', width=120, height=30)
        self.searchYearENTRY.place(x=270, y=5)

        self.searchBUTTON = customtkinter.CTkButton(self.searchFrame, text='Search', width=150, height=35, command= self.perform_search)
        self.searchBUTTON.place(x=400, y=3)
        self.searchBUTTON.configure(state=DISABLED)


        self.current_frame = None

        self.switch_frame_buttons = customtkinter.CTkFrame(self, fg_color=main_bgCOLOR, width=800, height=120)
        self.switch_frame_buttons.pack(pady=10)

        self.toWatchBUTTON = customtkinter.CTkButton(self.switch_frame_buttons, fg_color=main_bgCOLOR, 
                            text='To Watch', width=200, height=35, font=('Bold', 15), hover_color=menu_button_hoverCOLOR, 
                            command=lambda: self.towatch(self.TWindicator))
        
        self.toWatchBUTTON.pack(side=customtkinter.LEFT, padx=10)
        self.TWindicator = customtkinter.CTkLabel(self.switch_frame_buttons, fg_color=main_bgCOLOR, text='', width=200)
        self.TWindicator.place(x=10, y=30)


        self.watchedBUTTON = customtkinter.CTkButton(self.switch_frame_buttons, fg_color=main_bgCOLOR, 
                            text='Watched', width=200, height=35, font=('Bold', 15), hover_color=menu_button_hoverCOLOR, 
                            command=lambda: self.watched(self.WEDindicator))
        
        self.watchedBUTTON.pack(side=customtkinter.LEFT, padx=10)
        self.WEDindicator = customtkinter.CTkLabel(self.switch_frame_buttons, fg_color=main_bgCOLOR, text='', width=200)
        self.WEDindicator.place(x=231, y=30)


        self.watchingBUTTON = customtkinter.CTkButton(self.switch_frame_buttons, fg_color=main_bgCOLOR, 
                            text='Watching', width=200, height=35, font=('Bold', 15), hover_color=menu_button_hoverCOLOR, 
                            command=lambda: self.watching(self.WINGindicator))
                            
        self.watchingBUTTON.pack(side=customtkinter.LEFT, padx=10)
        self.WINGindicator = customtkinter.CTkLabel(self.switch_frame_buttons, fg_color=main_bgCOLOR, text='', width=200)
        self.WINGindicator.place(x=452, y=30)
    

    def perform_search(self):
        title = self.searchTitleENTRY.get()
        year = self.searchYearENTRY.get()
        print(f"Searching for {title} ({year}) under category: {self.current_selection}")
        self.manager.run(title, self.current_selection, year)
        
    def hide_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
            # self.current_frame.destroy()
            self.current_frame = None

    def towatch(self, indicator):
        self.current_selection = "to_watch"
        self.searchBUTTON.configure(state=NORMAL)

        self.TWindicator.configure(fg_color = main_bgCOLOR)
        self.WEDindicator.configure(fg_color = main_bgCOLOR)
        self.WINGindicator.configure(fg_color = main_bgCOLOR)

        indicator.configure(fg_color = menu_bgCOLOR)


        self.hide_current_frame()
        self.current_frame = customtkinter.CTkScrollableFrame(self, fg_color=menu_bgCOLOR, height=560, width=1220)
        self.current_frame.pack()


    def watched(self, indicator):
        self.current_selection = "watched"
        self.searchBUTTON.configure(state=NORMAL)
        self.TWindicator.configure(fg_color = main_bgCOLOR)
        self.WEDindicator.configure(fg_color = main_bgCOLOR)
        self.WINGindicator.configure(fg_color = main_bgCOLOR)

        indicator.configure(fg_color = menu_bgCOLOR)

        self.hide_current_frame()
        self.current_frame = customtkinter.CTkScrollableFrame(self, fg_color=menu_bgCOLOR, height=560, width=1220)
        self.current_frame.pack()



    def watching(self, indicator):
        self.current_selection = "watching"
        self.searchBUTTON.configure(state=NORMAL)

        self.TWindicator.configure(fg_color = main_bgCOLOR)
        self.WEDindicator.configure(fg_color = main_bgCOLOR)
        self.WINGindicator.configure(fg_color = main_bgCOLOR)

        indicator.configure(fg_color = menu_bgCOLOR)

        self.hide_current_frame()
        self.current_frame = customtkinter.CTkScrollableFrame(self, fg_color=menu_bgCOLOR, height=560, width=1220)
        self.current_frame.pack()


class DataBasePage(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(fg_color=main_bgCOLOR, corner_radius=10)

        customtkinter.CTkLabel(self, text='DATABASE', font=('Helvetica', 50), text_color=menu_button_hoverCOLOR).pack(pady=30)


# if __name__ == '__main__':
#     app = WatchListApp()
#     app.mainloop()
