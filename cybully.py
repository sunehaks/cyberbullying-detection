from __future__ import division
from nltk import *
from nltk.corpus import stopwords
import numpy as np
import xml.etree.ElementTree as ET
import pyexcel
import openpyxl
from openpyxl import Workbook
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors
from texttable import Texttable

def detect(fpath,lpath,fname):
	tree=ET.parse(fpath)		# tree generation for xml file
	root=tree.getroot()
	
	count=0
	for child in root:		# counting no. of children
		count=count+1
	
	i=0
	posts=[]						# extracting posts from xml file
	while i<count:
		posts.append(root[i][2].text)
		i=i+1
	
	posts=[x for x in posts if x!=None]
	
	i=0
	while i<len(posts):
		posts[i]=posts[i].encode("utf-8")
		i=i+1
		
	
	sw=stopwords.words('english')				# extracting common words like 'a','the' in english
	sw=[x.encode("utf-8") for x in sw]			# converting sw to utf-8 encoding
	
	bw=np.loadtxt('/home/suneha/Desktop/seminar stuff/badwords.txt',dtype=str)		# extracting bad words from txt file
	
	i=0
	bad=[]
	while i<len(posts):
		p=posts[i].split()					# converting individual posts to list of words
		p=[w for w in p if w.lower() not in sw]			# removing stopwords from the post
		b=[w for w in p if w.lower() in bw]			# retaining bad words in post if any
		
		bad.append(b)
		
		i=i+1
	
		
	i=0
	while i<len(posts):
		if len(bad[i])!=0:
			ans='Y'
			break
		i=i+1
		
	if i==len(posts):
		ans='N'
	
	#print "Is bullying present?\nprogram's answer:",ans
	
	dict=pyexcel.get_dict(file_name=lpath,start_row=2,column_limit=2,name_columns_by_row=-1, name_rows_by_column=0)
	
	fn=[]
	
	if fname[-1]=='.':
		fn=fname[:12]
		
	if fname[-1]=='0':
		fn=fname[:11]
		if fname[-2]=='0':
			fn=fname[:10]
			if fname[-3]=='0':
				fn=fname[:9]
				if fname[-4]=='0':
					fn=fname[:8]
	
	else:
		fn=fname
		
	ans1=dict[fn]
	ans1=str(ans1)[3:4]
	#print "actual scenario:",ans1
	
	res=[ans,ans1]
	return res
	

def gennumsev(fpath,fname,lpath):


	tree=ET.parse(fpath)		# tree generation for xml file
	root=tree.getroot()
	
	count=0
	for child in root:		# counting no. of children
		count=count+1
	
	i=0
	posts=[]						# extracting posts from xml file
	while i<count:
		posts.append(root[i][2].text)
		i=i+1
		
	posts=[x for x in posts if x!=None]	
		
	i=0
	while i<len(posts):
		posts[i]=posts[i].encode("utf-8")
		i=i+1
	
	sw=stopwords.words('english')				# extracting common words like 'a','the' in english
	sw=[x.encode("utf-8") for x in sw]			# converting sw to utf-8 encoding
	
	dict=pyexcel.get_dict(file_name=lpath,start_row=2,column_limit=2,name_columns_by_row=-1, name_rows_by_column=0)
	
	fn=[]
	
	if fname[-1]=='.':
		fn=fname[:12]
		
	if fname[-1]=='0':
		fn=fname[:11]
		if fname[-2]=='0':
			fn=fname[:10]
			if fname[-3]=='0':
				fn=fname[:9]
				if fname[-4]=='0':
					fn=fname[:8]
	
	else:
		fn=fname
		
	
	
	bw=pyexcel.get_dict(file_name='/home/suneha/Desktop/seminar stuff/badwords.xlsx',column_limit=2,name_columns_by_row=-1,name_rows_by_column=0)		


	i=0
	bad=[]
	while i<len(posts):
		p=posts[i].split()					# converting individual posts to list of words
		p=[w for w in p if w.lower() not in sw]			# removing stopwords from the post
		b=[w for w in p if w.lower() in bw]			# retaining bad words in post if any
		bad=[x for x in bad if x!=[]]
		bad.append(b)
		
		i=i+1
	
	i=1
	while i<len(bad):
	     k=0
	     while k<len(bad[i]):					#converting list of list of words to list of words
	             bad[0].append(bad[i][k])
	             k=k+1
	     i=i+1
 
	if len(bad)==0:							#differentiating empty lists from non empty ones
		NUM=0
		SEV=0
	else:
		bad1=bad[0]						#getting NUM and SEV for non empty word lists
		bad1=[x.lower() for x in bad1]
		
		NUM=len(bad1)
		SEV=0
		i=0
		while i<len(bad1):				#getting severity of each word and adding to get overall severity
		    SEV=SEV+int(bw[bad1[i]][0])
		    i=i+1	
	
	
	t=dict[fn][0]
	#book=openpyxl.load_workbook(opfile)
	#sheet=book.active
	t=str(t)
	row=[NUM,SEV,t]
	return row
	#sheet.append(row)
	
	#book.save(opfile)
	

def pktgen(pkt,lpath,opfile):
	files=[]
	file_paths=[]
	for root,dirs,fs in os.walk(pkt):			#walking through dir tree to get its files and file_paths
	     for filename in fs:
	             files.append(filename[:-4])
	             filepath=os.path.join(root,filename)
	             file_paths.append(filepath)
	             
	sw=stopwords.words('english')				# extracting common words like 'a','the' in english
	sw=[x.encode("utf-8") for x in sw]			# converting sw to utf-8 encoding
	
	bw=pyexcel.get_dict(file_name='/home/suneha/Desktop/seminar stuff/badwords.xlsx',column_limit=2,name_columns_by_row=-1,name_rows_by_column=0)		
	
	dict=pyexcel.get_dict(file_name=lpath,start_row=2,column_limit=2,name_columns_by_row=-1, name_rows_by_column=0)
	
	j=0
	while j<len(files):
		tree=ET.parse(file_paths[j])		# tree generation for xml file
		root=tree.getroot()
	
		count=0
		for child in root:			# counting no. of children
			count=count+1
	
		i=0
		posts=[]						# extracting posts from xml file
		while i<count:
			posts.append(root[i][2].text)
			i=i+1
		
		posts=[x for x in posts if x!=None]
		i=0
		
		while i<len(posts):
			posts[i]=posts[i].encode("utf-8")		#encoding posts from unicode to utf-8 str
			i=i+1
			
			
		
		
		i=0
		bad=[]
		fname=[]
		while i<len(posts):
			p=posts[i].split()					# converting individual posts to list of words
			p=[w for w in p if w.lower() not in sw]			# removing stopwords from the post
			b=[w for w in p if w.lower() in bw]			# retaining bad words in post if any
			bad.append(b)

			bad=[x for x in bad if x!=[]]				#removing empty values in bad
			i=i+1	
						
		i=1
		while i<len(bad):
		     k=0
		     while k<len(bad[i]):					#converting list of list of words to list of words
		             bad[0].append(bad[i][k])
		             k=k+1
		     i=i+1
 
		if len(bad)==0:							#differentiating empty lists from non empty ones
			NUM=0
			SEV=0
		else:
			bad1=bad[0]						#getting NUM and SEV for non empty word lists
			bad1=[x.lower() for x in bad1]
			NUM=len(bad1)
			SEV=0
			i=0
			while i<len(bad1):				#getting severity of each word and adding to get overall severity
			    SEV=SEV+int(bw[bad1[i]][0])
			    i=i+1
		
									#extracting human consensus of corresponding file
		t=0
		if dict[files[j]][0]=='Y':
			t=1
	    
		book=openpyxl.load_workbook(opfile)				# writing to an xlsx file
		sheet=book.active
	
		row=[files[j],NUM,SEV,t]
	
		sheet.append(row)
	
		book.save(opfile)
		
		j=j+1    
		
		
def knn1(ipfile,fpath,fname,lpath):

	X=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=1,column_limit=2))
	y=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=3,column_limit=1))
	y=np.ravel(y)
	l=len(X)
	Y=np.reshape(y,l)
	
	n_neighbors=1
	clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
	clf.fit(X,Y)		
	
	
	x=gennumsev(fpath,fname,lpath)
	label=x[2]
	xx=[x[:2]]
	
	Z=clf.predict(xx)
	
	if Z[0]==1:
		ans='Y'
	else:
		ans='N'
		
	#print "Is cyber bullying present?"
	#print "Answer from knn (k=1) approach:",ans
	#print "Actual scenario:",label
	res=[ans,label]
	return res
	
	
def knn15(ipfile,fpath,fname,lpath):

	X=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=1,column_limit=2))
	y=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=3,column_limit=1))
	y=np.ravel(y)
	l=len(X)
	Y=np.reshape(y,l)
	
	n_neighbors=15
	clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
	clf.fit(X,Y)		
	
	
	x=gennumsev(fpath,fname,lpath)
	label=x[2]
	xx=[x[:2]]
	
	Z=clf.predict(xx)
	
	if Z[0]==1:
		ans='Y'
	else:
		ans='N'
		
	#print "Is cyber bullying present?"
	#print "Answer from knn (k=15) approach:",ans
	#print "Actual scenario:",label
	res=[ans,label]
	return res
	
	
	
def tab(pkt,lpath):

	files=[]
	file_paths=[]
	for root,dirs,fs in os.walk(pkt):
	     for filename in fs:
		     files.append(filename[:12])
		     filepath=os.path.join(root,filename)
		     file_paths.append(filepath)
		     
	
	#t.add_rows([['Algorithm', '% correctly labelled']])
	#lpath='Packet10Consensus.xlsx'
	i=0
	corr1=0
	while i<len(files):
	     ans=detect(file_paths[i],lpath,files[i])
	     if ans[0]==ans[1]:
		     corr1=corr1+1
	     i=i+1
	     
	per1=(corr1/len(files))*100
	#print per1
	#t.add_rows([['Simple search', per1]])
	
	i=0
	corr2=0
	while i<len(files):
	     ans=knn1('op3.xlsx',file_paths[i],files[i],lpath)
	     if ans[0]==ans[1]:
		     corr2=corr2+1
	     i=i+1
	     
	per2=(corr2/len(files))*100
	#print per2
	#t.add_rows([['KNN(k=1)', per2]])
	
	i=0
	corr3=0
	while i<len(files):
		ans=knn15('op3.xlsx',file_paths[i],files[i],lpath)
		if ans[0]==ans[1]:
			corr3=corr3+1
		i=i+1
	     
	per3=(corr3/len(files))*100
	#print per3
	#t.add_rows([['KNN(k=15)', per3]])
	t=Texttable()
	t.add_rows([['Algorithm', '% correctly labelled'],['Simple search', per1],['KNN(k=1)', per2],['KNN(k=15)', per3]])
	print t.draw()
	


def detectdemo(fpath,lpath,fname):
	tree=ET.parse(fpath)		# tree generation for xml file
	root=tree.getroot()
	
	count=0
	for child in root:		# counting no. of children
		count=count+1
	
	i=0
	posts=[]						# extracting posts from xml file
	while i<count:
		posts.append(root[i][2].text)
		i=i+1
	
	posts=[x for x in posts if x!=None]
	
	i=0
	while i<len(posts):
		posts[i]=posts[i].encode("utf-8")
		i=i+1
		
	
	sw=stopwords.words('english')				# extracting common words like 'a','the' in english
	sw=[x.encode("utf-8") for x in sw]			# converting sw to utf-8 encoding
	
	bw=np.loadtxt('/home/suneha/Desktop/seminar stuff/badwords.txt',dtype=str)		# extracting bad words from txt file
	
	i=0
	bad=[]
	while i<len(posts):
		p=posts[i].split()					# converting individual posts to list of words
		p=[w for w in p if w.lower() not in sw]			# removing stopwords from the post
		b=[w for w in p if w.lower() in bw]			# retaining bad words in post if any
		
		bad.append(b)
		
		i=i+1
	
		
	i=0
	while i<len(posts):
		if len(bad[i])!=0:
			ans='Y'
			break
		i=i+1
		
	if i==len(posts):
		ans='N'
	
	print "Is bullying present?\nprogram's answer:",ans
	
	dict=pyexcel.get_dict(file_name=lpath,start_row=2,column_limit=2,name_columns_by_row=-1, name_rows_by_column=0)
	
	fn=[]
	
	if fname[-1]=='.':
		fn=fname[:12]
		
	if fname[-1]=='0':
		fn=fname[:11]
		if fname[-2]=='0':
			fn=fname[:10]
			if fname[-3]=='0':
				fn=fname[:9]
				if fname[-4]=='0':
					fn=fname[:8]
	
	else:
		fn=fname
		
	ans1=dict[fn]
	ans1=str(ans1)[3:4]
	print "actual scenario:",ans1
	
	
	

def knn1demo(ipfile,fpath,fname,lpath):

	X=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=1,column_limit=2))
	y=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=3,column_limit=1))
	y=np.ravel(y)
	l=len(X)
	Y=np.reshape(y,l)
	
	n_neighbors=1
	clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
	clf.fit(X,Y)		
	
	
	x=gennumsev(fpath,fname,lpath)
	label=x[2]
	xx=[x[:2]]
	
	Z=clf.predict(xx)
	
	if Z[0]==1:
		ans='Y'
	else:
		ans='N'
		
	p=np.append(X,xx)
		
	print "Is cyber bullying present?"
	print "Answer from knn (k=1) approach:",ans
	print "Actual scenario:",label
	#res=[ans,label]
	#return res
	
	
def knn15demo(ipfile,fpath,fname,lpath):

	X=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=1,column_limit=2))
	y=np.array(pyexcel.get_array(file_name=ipfile,start_row=1,start_column=3,column_limit=1))
	y=np.ravel(y)
	l=len(X)
	Y=np.reshape(y,l)
	
	n_neighbors=15
	clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
	clf.fit(X,Y)		
	
	
	x=gennumsev(fpath,fname,lpath)
	label=x[2]
	x1=[x[:2]]
	
	Z=clf.predict(x1)
	
	if Z[0]==1:
		ans='Y'
	else:
		ans='N'
		
	print "Is cyber bullying present?"
	print "Answer from knn (k=15) approach:",ans
	print "Actual scenario:",label
	#res=[ans,label]
	#return res
	
	h=1
	cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
	x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
	plt.figure()
	plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                edgecolor='k', s=20)
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.title("yes or no classification (k = %i, weights = 'distances')"% (n_neighbors))
	
	
	plt.show()
