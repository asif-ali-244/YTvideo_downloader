from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from pytube import YouTube
import os


def path():
	global home
	home=os.path.expanduser('~')
	download_path=os.path.join(home, 'Downloads')
	return download_path

def newWindow():
	global newWin
	newWin=Toplevel(root)

	newWin.title("Download Quality")
	l1=Label(newWin,text="Select Download Quality:")
	l1.grid(row=1,column=0)
	b1=Button(newWin,text="Video",padx=20,pady=10,command=getVideoLink)
	b1.grid(row=2,column=0)
	b2=Button(newWin,text="Audio",padx=20,pady=10,command=getAudioLink)
	b2.grid(row=3,column=0)
	loadinglabel=ttk.Label(newWin,text="Downloading....")
	loadinglabel.grid(row=4,column=0,pady=10)

	global loadingPercent
	loadingPercent=Label(newWin,text="0",fg='green')
	loadingPercent.grid(row=5,column=0)
	global progressBar
	progressBar=ttk.Progressbar(newWin,orient='horizontal',length=500,mode='determinate')
	progressBar.grid(row=6,column=0)
	
def completeDownload():

	mb.showinfo("Download","Download Completed. File is saved to {}\Downloads".format(home))

def progress_function(stream,chunk,remaining):
	percent = (100*(file_size-remaining))/file_size
	loadingPercent['text']="{:00.0f}% downloaded".format(percent)
	progressBar['value']=percent
	newWin.update_idletasks()

def downloadVideo(link,flag) :
	try:
		yt=YouTube(link,on_progress_callback=progress_function)
	except:
		mb.showerror("Error","Not Connecting/Incorrect Link")
	# files=yt.streams.get_audio_only()
	if flag==0:
		files=yt.streams.get_audio_only()
	else:
		files=yt.streams.get_highest_resolution() 
	global file_size
	file_size=files.filesize
	file_name=yt.description
	if len(file_name)>15:
		file_name=file_name[:15]

	try:
		files.download(path(),file_name)
		completeDownload()
	except:
		mb.showerror("Error","Error downloading file!")
	

def getVideoLink():
	link=e.get()
	e.delete(0,END)
	downloadVideo(link,1)
def getAudioLink():
	link=e.get()
	e.delete(0,END)
	downloadVideo(link,0)

root=Tk()
#root.geometry("800x550") 
root.title("YouTube Downloader")

frame1=LabelFrame(root,text="YouTube video",padx=10,pady=10)
frame2=LabelFrame(root,text="YouTube Playlist",padx=10,pady=10)
frame1.grid(row=0,padx=10,pady=10)
frame2.grid(row=1,padx=10,pady=10)
button=Button(frame1, text="Download Video!", fg='blue',padx=10,command=newWindow)
button.grid(row=0,column=0,padx=20)
e=Entry(frame1, bd=3,width=100)
e.grid(row=0,column=1)#,columnspan=1)
button2=Button(frame2, text="Download Playlist!", fg='red',padx=10)
button2.grid(row=1,column=0,padx=20)
e2=Entry(frame2,bd=3,width=100)
e2.grid(row=1,column=1)


root.mainloop()