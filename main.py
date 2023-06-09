from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from recommendations import sim_distance, sim_pearson, getRecommendations,  topMatches

class GithubProjectRecommender(Frame):
    def __init__(self, parent):
        self.repositories = {}
        self.stars = {}
        self.users = {}

        Frame.__init__(self, parent)
        self.initUI(parent)
        

    def readUserData(self, filename, lst):
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip().lower().split(",")
                user_id = line[0]
                username = line[1]
                url = line[2]
                lst[user_id] = {'username': username, 'user_id': user_id, 'url': url}

    def readStarData(self, filename, lst):
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip().split("\t")
                user_id = int(line[0])
                stars = list(map(int, line[1].split(",")))
                lst[user_id] = {repo: 5.0 for repo in stars}
        print(lst)
    
    def readRepositoryData(self, filename, lst):
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip().split(",")
                repo_id = line[0]
                name = line[1]
                url = line[2]
                language = line[3]
                lst[repo_id] = {'repo_id': repo_id, 'name': name, 'url': url, 'language': language}
        print(lst)
            
    def chooseUserData(self):
        filename = filedialog.askopenfilename(initialdir="C:\\Users\\user\\Desktop\\pythonfinal", title="Select a File", filetypes=(("Txt files", ["*.txt"]),))
        self.readUserData(filename, self.users)

        self.repo_view.delete(*self.repo_view.get_children())
        sorted_users = sorted(self.users.values(), key=lambda x: x['username'])  

        for user_data in sorted_users:
            username = user_data['username']
            user_id = user_data['user_id']
            url = user_data['url']
            self.repo_view.insert("", "end", values=(username, user_id, url))
            
    def chooseStarData(self):
        filename = filedialog.askopenfilename(initialdir="C:\\Users\\user\\Desktop\\pythonfinal", title="Select a File", filetypes=(("Txt files", ["*.txt"]),))
        self.readStarData(filename, self.stars)

    def chooseRepositoryData(self):
        filename = filedialog.askopenfilename(initialdir="C:\\Users\\user\\Desktop\\pythonfinal", title="Select a File", filetypes=(("Txt files", ["*.txt"]),))
        self.readRepositoryData(filename, self.repositories)

        lang_names = set()
        lang_names = ["None"]        
        for repo_data in self.repositories.values():
            language = repo_data['language']
            if language not in lang_names:
                lang_names.append(language)

        self.combobox['values'] = list(lang_names)
        self.combobox.current(0)  
    
    def recommendedRepository(self):
        selected_user = self.repo_view.focus()
        selected_item = self.repo_view.item(selected_user)
        id = selected_item['values'][1]
        func = sim_pearson if self.person_chk_var.get() else sim_distance
        recommendation = getRecommendations(self.stars, id, func)
        
        self.reco_view.delete(*self.reco_view.get_children())
        for i in range(min(len(recommendation), 3 if not self.nmb_entry.get() else int(self.nmb_entry.get()))):
            
            repo_id = recommendation[i][1]
            repo_data = self.repositories.get(str(repo_id))
            repo_name = repo_data.get('name')
            repo_url = repo_data.get('url')
            score = recommendation[i][0]
            self.reco_view.insert("", "end", values=(repo_name, repo_url, score))
            
    def recommendedUser(self):
        selected_user = self.repo_view.focus()
        selected_item = self.repo_view.item(selected_user)

        user_id = selected_item['values'][1]  # Kullanıcı ID'si
        func = sim_pearson if self.person_chk_var.get() else sim_distance
        recommendation = topMatches(self.stars, 3 if not self.nmb_entry.get() else int(self.nmb_entry.get()) , user_id, func)
        
        self.reco_view.delete(*self.reco_view.get_children())
        for i in range(min(len(recommendation), 3 if not self.nmb_entry.get() else int(self.nmb_entry.get()))):
            similar_user_id = recommendation[i][1]
            user_data = self.users.get(str(similar_user_id))
            username = user_data.get('username')
            url = user_data.get('url')
            score = recommendation[i][0]
            self.reco_view.insert("", "end", values=(username, url, score))
        
    def checkbox1_selected(self):
        if self.person_chk_var.get():
            self.eucl_chk_var.set(False)  
        else:
            self.eucl_chk_var.set(True)  

    def checkbox2_selected(self):
        if self.eucl_chk_var.get():
            self.person_chk_var.set(False)
        else:
            self.person_chk_var.set(True) 
    
        
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
        self.person_chk_var = BooleanVar()
        self.person_chk_var.set(True)
        self.person_chk = Checkbutton(variable=self.person_chk_var, command= self.checkbox1_selected)
        
        self.eucl_chk_var = BooleanVar()
        self.eucl_chk = Checkbutton(variable=self.eucl_chk_var, command=self.checkbox2_selected) 
        
        
        #buttons
        self.upload_user_btn = Button(text="Upload User Data", height=2, command=self.chooseUserData)
        self.upload_repo_btn = Button(text="Upload Repository Data", height=2, command=self.chooseRepositoryData)
        self.upload_star_btn = Button(text="Upload Star Data", height=2, command=self.chooseStarData)
        self.reco_repo_btn  = Button(text="Recommend Repository", height=2, command= self.recommendedRepository)
        self.reco_git_btn = Button(text="Recommend Github User", height=2, command=self.recommendedUser)
        
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