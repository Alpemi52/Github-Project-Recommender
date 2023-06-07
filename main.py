from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class GithubProjectRecommender(Frame):
    def __init__(self, parent):
        self.repositories = []
        self.stars = []
        self.users = []

        Frame.__init__(self, parent)
        self.initUI(parent)
        

    def readAllData(self, filename, arr):
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                arr.append(line.strip().lower().split(","))

    def chooseUserData(self):
        filename = filedialog.askopenfilename(initialdir="C:\\Users\\user\\Desktop\\pythonfinal", title="Select a File", filetypes=(("Txt files", ["*.txt"]),))
        self.readAllData(filename, self.users)
        
        self.users.sort(key=lambda user: user[1])
        for user in self.users:
                self.repo_view.insert("", "end", values=(user[1], user[0]))

    def chooseStarData(self):
        filename = filedialog.askopenfilename(initialdir="C:\\Users\\user\\Desktop\\pythonfinal", title="Select a File", filetypes=(("Txt files", ["*.txt"]),))
        self.readAllData(filename, self.stars)

    def chooseRepositoryData(self):
        filename = filedialog.askopenfilename(initialdir="C:\\Users\\user\\Desktop\\pythonfinal", title="Select a File", filetypes=(("Txt files", ["*.txt"]),))
        self.readAllData(filename, self.repositories)

        lang_names = ["None"]
        for repo in self.repositories:
            if repo[-1:] not in lang_names:
                lang_names.append(repo[-1:])
            
        self.combobox['values'] = lang_names
        self.combobox.current(0)
        
    def initUI(self, parent):
        
        #entry
        self.nmb_entry = Entry(width=3, font=('Arial', 14))
        
        #label
        self.title = Label(text="Github Project Recommender", bg="orange",font=('Arial', 24), width=61)
        self.recom_repo = Label(text="Recommend Repository For")
        self.recom = Label(text="Recommendations")
        self.filter = Label(text="Filter by programing language")
        self.distance = Label(text="Distance Algorithm:")
        self.person = Label(text="Person", padx=70)
        self.euclidean = Label(text="Euclidean", padx=15)
        self.nmb_reco = Label(text="Number of Recommendetaions:", font=("Arial", 8))
        
        #combobox
        self.combobox = ttk.Combobox()
        
        #checkbox
        self.person_chk = Checkbutton()
        self.eucl_chk = Checkbutton() 
        
        #buttons
        self.upload_user_btn = Button(text="Upload User Data", height=2, command=self.chooseUserData)
        self.upload_repo_btn = Button(text="Upload Repository Data", height=2, command=self.chooseRepositoryData)
        self.upload_star_btn = Button(text="Upload Star Data", height=2, command=self.chooseStarData)
        self.reco_repo_btn  = Button(text="Recommend Repository", height=2)
        self.reco_git_btn = Button(text="Recommend Github User", height=2)
        
        #trewiews
        self.repo_view = ttk.Treeview(columns=("Username", "Id"), show="headings")
        self.repo_view.column("# 1",width= 90)
        self.repo_view.column("# 2",width= 60)
        self.repo_view.heading('Username', text='Username')
        self.repo_view.heading('Id', text='Id')

        self.reco_view = ttk.Treeview(columns=("Name", "Url", "Score"), show="headings", height=25)
        self.reco_view.column("# 1", width=85)
        self.reco_view.column("# 2", width=200)
        self.reco_view.column("# 3", width=60)
        self.reco_view.heading("Name", text="Name")
        self.reco_view.heading("Url", text="Url")
        self.reco_view.heading("Score", text="Score")
        
        
        #Row 0
        self.title.grid(row=0, column=0, columnspan=5)
        
        #Row 1
        self.upload_user_btn.grid(row=1, column=0, pady= 20)
        self.upload_repo_btn.grid(row=1, column=2, pady= 20)
        self.upload_star_btn.grid(row=1, column=4, pady= 20)
        
        #Row 2
        
        self.recom.grid(row=2, column=4)
        self.reco_repo_btn.grid(row=2, column=1, sticky=S, rowspan=2, pady=45)
        
        
        #Row 3
        self.recom_repo.grid(row=3, column=0, sticky=N)
        self.reco_git_btn.grid(row=3, column=1, sticky=S)
        self.repo_view.grid(row=3, column=0, sticky=S)
        self.reco_view.grid(row=3, column=4, rowspan=6)

        #Row 4
        self.filter.grid(row=4, column=0, sticky=N)
        self.combobox.grid(row=4, column=0, pady=10)
        self.distance.grid(row=4, column=0, sticky=S)
        
        #Row 5
        self.person_chk.grid(row=5, column=0)
        self.person.grid(row=5, column=0, sticky=E)
        
        #Row 6
        self.eucl_chk.grid(row=6, column=0, sticky=N)
        self.euclidean.grid(row=6, column=0, sticky=NE, padx=40)
        
        #Row 7
        self.nmb_reco.grid(row=7, column=0,sticky=NW)
        self.nmb_entry.grid(row=7, column=0, sticky=NE, padx=50)
        
        #Row 8
def main():
    root = Tk()
    root.title("Github Repository Recommender")
    root.geometry("1150x700+385+110",)
    root.resizable(False, False)
    
    GithubProjectRecommender(root)
    root.mainloop()

main()